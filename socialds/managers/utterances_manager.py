from typing import List

# from nltk import word_tokenize

from socialds.action.action import Action
from socialds.agent import Agent
from socialds.managers.utterance_matcher import get_relations_from_text
from socialds.utterance import Utterance
from Levenshtein import ratio, jaro_winkler
# # from sentence_transformers import SentenceTransformer, models
# import nltk
# from nltk.corpus import stopwords
# from scipy.spatial.distance import cosine
#
# # import spacy
# from rdflib import Graph, URIRef, Literal, RDF, RDFS

# # Load English language model in spaCy
# nlp = spacy.load("en_core_web_lg")
# # model = SentenceTransformer('all-mpnet-base-v2')
# nltk.download('stopwords')
# nltk.download('punkt')
# stop_words = stopwords.words('english') + ['<', '%', ':', '&']


# def remove_stop_words_from_sentence(sentence):
#     word_tokens = word_tokenize(sentence)
#     # converts the words in word_tokens to lower case and then checks whether
#     # they are present in stop_words or not
#     filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
#     # with no lower case conversion
#     filtered_sentence = ''
#
#     for w in word_tokens:
#         if w not in stop_words:
#             filtered_sentence += w + ' '
#     return filtered_sentence[:-1]


class UtterancesManager:

    def __init__(self, utterances: List[Utterance]):
        self.utterances = utterances
        self.utts_with_embs = []
        # for utt in self.utterances:
        #     self.utts_with_embs.append((utt, model.encode(remove_stop_words_from_sentence(utt.text))))

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
            ratio_score = jaro_winkler(input.lower(), utt.text.lower())
            if ratio_score > best_match[1]:
                best_match = (utt, ratio_score)
        print(best_match)
        return best_match[0]

    def get_utterance_by_smart_string_match(self, input: str, checker: Agent):
        pass
        # print_ontology(input)
        # if len(self.utterances) == 0:
        #     return
        # input_emb = model.encode(remove_stop_words_from_sentence(input))
        # best_match = (self.utterances[0], 0)
        # for utt_with_emb in self.utts_with_embs:
        #     score = cosine(input_emb, utt_with_emb[1])
        #     if score > best_match[1]:
        #         best_match = (utt_with_emb[0], score)
        # return best_match[0]

    # def get_utterance_by_relation_match(self, input: str, checker: Agent):
    #     relations = get_relations_from_text(input)
    #     for relation in relations:
    #         if relation is not None:
    #             action_name = relation['action_name']
    #             del relation['action_name']
    #
    #     else:
    #         return self.get_utterance_by_smart_string_match(input, checker)
