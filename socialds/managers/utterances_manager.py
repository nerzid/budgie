from copy import deepcopy
from typing import List

from nltk import word_tokenize

from socialds.action.action import Action
from socialds.agent import Agent
from socialds.any.any_place import AnyPlace
from socialds.any.any_property import AnyProperty
from socialds.managers.utterance_matcher import get_relations_from_text
from socialds.other.dst_pronouns import DSTPronoun
from socialds.socialpractice.context.resource import Resource
from socialds.states.property import Property
from socialds.utterance import Utterance
from Levenshtein import ratio, jaro_winkler
from sentence_transformers import SentenceTransformer, models
import nltk
from nltk.corpus import stopwords
from scipy.spatial.distance import cosine

import spacy
from rdflib import Graph, URIRef, Literal, RDF, RDFS

# Load English language model in spaCy
nlp = spacy.load("en_core_web_lg")
model = SentenceTransformer('all-mpnet-base-v2')
nltk.download('stopwords')
nltk.download('punkt')
stop_words = stopwords.words('english') + ['<', '%', ':', '&']


def remove_stop_words_from_sentence(sentence):
    word_tokens = word_tokenize(sentence)
    # converts the words in word_tokens to lower case and then checks whether
    # they are present in stop_words or not
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    # with no lower case conversion
    filtered_sentence = ''

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence += w + ' '
    return filtered_sentence[:-1]


def print_ontology(input):
    # Extract concepts and relationships
    concepts, relationships = extract_concepts_and_relationships(input)

    # Convert concepts and relationships to RDF triples
    graph = concepts_and_relationships_to_rdf(concepts, relationships)
    # Serialize RDF graph to a file
    graph.serialize("ontology.ttl", format="turtle")


# Define a function to extract concepts and relationships from text
def extract_concepts_and_relationships(text):
    doc = nlp(text)
    concepts = set()
    relationships = []

    for token in doc:
        if token.pos_ == "NOUN" or token.pos_ == "PROPN":
            concepts.add(token.text)

    for ent in doc.ents:
        concepts.add(ent.text)

    for token in doc:
        if token.dep_ == "ROOT":
            subject = None
            for child in token.children:
                if child.pos_ == "NOUN" or child.pos_ == "PROPN" or child.dep_ == "compound":
                    subject = child.text
                    break
            if subject is None:
                continue

            for child in token.children:
                if child.pos_ == "ADJ":
                    relationships.append((subject, token.text, child.text))
                    break

    return concepts, relationships


# Define a function to convert concepts and relationships to RDF triples
def concepts_and_relationships_to_rdf(concepts, relationships):
    graph = Graph()

    for concept in concepts:
        graph.add((URIRef(concept), RDF.type, RDFS.Resource))
        graph.add((URIRef(concept), RDFS.label, Literal(concept)))

    for subject, predicate, obj in relationships:
        subject_uri = URIRef(subject)
        predicate_uri = URIRef(predicate)
        obj_uri = URIRef(obj)

        graph.add((subject_uri, predicate_uri, obj_uri))

    return graph


class UtterancesManager:

    def __init__(self, utterances: List[Utterance], resources: List[Resource], properties: List[Property]):
        self.utterances = utterances
        self.resources = resources
        self.properties = properties
        self.utts_with_embs = []
        for utt in self.utterances:
            self.utts_with_embs.append((utt, model.encode(remove_stop_words_from_sentence(utt.text))))

    def get_utterance_by_action(self, actions, checker: Agent):
        for utt in self.utterances:
            utt_match = True
            for action in actions:
                match = False

                action_count = 0
                for act in utt.actions:
                    if isinstance(act, Action):
                        action_count += 1

                if len(actions) != action_count:
                    utt_match = False
                    break

                for act in utt.actions:
                    if action.equals_with_pronouns(act, pronouns=checker.pronouns):
                        match = True
                if not match:
                    utt_match = False
                    break
            if utt_match:
                return utt
        return None

    def get_utterance_by_string_match(self, input: str, checker: Agent):
        if len(self.utterances) == 0:
            return
        best_match = (self.utterances[0], 0)
        for utt in self.utterances:
            for txt in utt.get_text_with_alternatives():
                ratio_score = jaro_winkler(input.lower(), txt.lower())
                if ratio_score > best_match[1]:
                    best_match = (utt, ratio_score)
        print(best_match)
        return best_match[0]

    def get_utterance_by_smart_string_match(self, input: str, checker: Agent):
        print_ontology(input)
        if len(self.utterances) == 0:
            return
        input_emb = model.encode(remove_stop_words_from_sentence(input))
        best_match = (self.utterances[0], 0)
        for utt_with_emb in self.utts_with_embs:
            score = cosine(input_emb, utt_with_emb[1])
            if score > best_match[1]:
                best_match = (utt_with_emb[0], score)
        return best_match[0]

    def get_utterance_by_relation_match(self, input: str, checker: Agent):
        relations = get_relations_from_text(input)
        for relation in relations:
            if relation is not None:
                rel = deepcopy(relation)
                for key, value in relation.items():
                    if isinstance(value, str):
                        rel[key] = self.change_pronoun_text_to_object(value, checker)
                    else:
                        rel[key] = value
                # action_name = relation['action_name']
                # del relation['action_name']

        else:
            return self.get_utterance_by_smart_string_match(input, checker)

    def insert_pronouns(self, text, checker: Agent):
        pronoun_added_text = text
        lowered_text = text.lower()
        if 'your' in lowered_text:
            pronoun_added_text = pronoun_added_text.replace('your', checker.pronouns[DSTPronoun.YOU].actor.name + "'s")
        elif 'my' in lowered_text:
            pronoun_added_text = pronoun_added_text.replace('my', checker.pronouns[DSTPronoun.I].actor.name + "'s")
        elif 'you' in lowered_text:
            pronoun_added_text = pronoun_added_text.replace('your', checker.pronouns[DSTPronoun.YOU].actor.name)
        elif 'i' in lowered_text or 'me' in lowered_text:
            pronoun_added_text = pronoun_added_text.replace('my', checker.pronouns[DSTPronoun.I].actor.name + "'s")
        return pronoun_added_text

    def insert_any_objects(self, text):
        lowered_text = text.lower()
        if lowered_text == 'what':
            return AnyProperty()
        elif lowered_text == 'where':
            return AnyPlace()
        else:
            return text

    def change_pronoun_text_to_resource(self, text: str, checker: Agent):
        pronoun_added_text = self.insert_pronouns(text, checker)
        for resource in self.resources:
            if pronoun_added_text.lower() == resource.name.lower():
                return resource
        return None

    def change_pronoun_text_to_property(self, text, checker: Agent):
        pronoun_added_text = self.insert_pronouns(text, checker)
        for property in self.properties:
            if pronoun_added_text.lower() == property.name.lower():
                return property
        return None

    def change_pronoun_text_to_object(self, text, checker: Agent):
        res = self.insert_any_objects(text)
        if not isinstance(res, str):  # this means that the text is one of the 'any objects',
            # therefore no reason to continue
            return res
        res = self.change_pronoun_text_to_resource(text, checker)
        if res:
            return res
        res = self.change_pronoun_text_to_property(text, checker)
        if res:
            return res
        return text
