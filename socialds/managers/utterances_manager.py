from typing import List

# from nltk import word_tokenize

from socialds.action.action import Action
from socialds.agent import Agent

# from socialds.managers.utterance_matcher import get_relations_from_text
from socialds.scenarios.scenario import Scenario
from socialds.utterance import Utterance
from Levenshtein import ratio, jaro_winkler
from ollama import Client

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

# LLM_URL = 'http://[REDACTED_IP]:[REDACTED_PORT]'


LLM_URL = 'http://[REDACTED_IP]:[REDACTED_PORT]'


class UtterancesManager:

    def __init__(self, scenario: Scenario):
        self.utterances = scenario.utterances
        self.llm_messages = []
        self.client = Client(host=LLM_URL)
        self.send_initial_prompt_to_llm()
        self.utts_with_embs = []
        # for utt in self.utterances:
        #     self.utts_with_embs.append((utt, model.encode(remove_stop_words_from_sentence(utt.text))))

    def send_initial_prompt_to_llm(self):
        prompt = ('When you receive a sentence, do the followings in order: '
                  '1- Extract the actions from the sentence '
                  '2- Based on the extracted actions, choose a sentence from the PREDEFINED UTTERANCES LIST that contains the extracted actions. '
                  '3- If there is no good match, then ask for a rephrase by saying "Could you please rephrase your request or provide a new sentence?" '
                  '4- If there is a match, then provide the sentence and actions. Dont suggest or ask anything. '
                  'The format for utterances is as follows: utterance_string (actions) Use the format when responding. '
                  'Explanations for some actions and when to extract them: '
                  'If the utterance asks for a confirmation such as "Is your eye red?" use RequestConfirmation action. '
                  'If the utterance ask for an action such as "Can you sit down, please?" use RequestAction action. '
                  'If the utterance asks for an information such as "What is your problem?" or "tell me about your problem" use RequestInfo action. '
                  'Note that the utterance doesnt have to be in question form to request an information. '
                  'For example, "tell me about your problem" doesnt have a question format and instead it is an invitation to receive information, '
                  'therefore it has the action RequestInfo. '
                  'If the utterance shares a certain information in a statement such as "My eye is red", or "I have a headache", use Share action. '
                  'If the utterance have affirmation such as "Yes", "Yeah", "Yup", use Affirm. If the utterance have rejection such as "No", "Nope, use Deny PREDEFINED UTTERANCES LIST:')

        prompt += str(self.utterances)
        self.llm_messages.append({
            'role': 'user',
            'content': str(prompt),
        })
        response = self.client.chat(model='lowtemp-llama3', messages=self.llm_messages)
        self.llm_messages.append({
            'role': 'assistant',
            'content': response['message']['content'],
        })

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

    def get_utterance_from_llm(self, input: str, checker: Agent):
        if len(self.utterances) == 0:
            return
        print(self.utterances)
        # client = Client(host='http://[REDACTED_IP]:[REDACTED_PORT]')
        self.llm_messages.append({
            'role': 'user',
            'content': input,
        })
        response = self.client.chat(model='lowtemp-llama3', messages=self.llm_messages)
        # self.llm_messages.pop()
        self.llm_messages.append({
            'role': 'assistant',
            'content': response['message']['content']
        })
        utterance_text = response['message']['content']
        for utt in self.utterances:
            if str(utt) == utterance_text:
                return utt
        return None

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
