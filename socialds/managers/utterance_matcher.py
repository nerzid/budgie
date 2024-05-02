# from copy import deepcopy

# import spacy
# from spacy.matcher import DependencyMatcher
# from spacy import displacy

# # Load English tokenizer, tagger, parser, and NER
# nlp = spacy.load("en_core_web_lg")
# matcher = DependencyMatcher(nlp.vocab)

# question_starters = ['is', 'are', 'was', 'were', 'will', 'do', 'did', 'does',
#                      'what', 'when', 'where', 'who', 'why', 'how', 'can', 'would', 'should']

# possible_action_names = []

# statement_pattern = [
#     {
#         "RIGHT_ID": "rtype",
#         "RIGHT_ATTRS": {"lemma": "be"}
#     },
#     {
#         "LEFT_ID": "rtype",
#         "REL_OP": ">",
#         "RIGHT_ID": "left",
#         "RIGHT_ATTRS": {"DEP": "nsubj"}
#     },
#     {
#         "LEFT_ID": "rtype",
#         "REL_OP": ">",
#         "RIGHT_ID": "right",
#         "RIGHT_ATTRS": {"DEP": {"IN": ["acomp", "attr", "dobj"]}}
#     }
# ]

# statement_with_negation_pattern = [
#     {
#         "RIGHT_ID": "rtype",
#         "RIGHT_ATTRS": {"lemma": "be"}
#     },
#     {
#         "LEFT_ID": "rtype",
#         "REL_OP": ">",
#         "RIGHT_ID": "left",
#         "RIGHT_ATTRS": {"DEP": "nsubj"}
#     },
#     {
#         "LEFT_ID": "rtype",
#         "REL_OP": ">",
#         "RIGHT_ID": "right",
#         "RIGHT_ATTRS": {"DEP": {"IN": ["acomp", "attr", "dobj"]}}
#     },
#     {
#         "LEFT_ID": "rtype",
#         "REL_OP": ">",
#         "RIGHT_ID": "negation",
#         "RIGHT_ATTRS": {"DEP": "neg"},
#     },
# ]

# request_confirmation_pattern = [
#     {
#         "RIGHT_ID": "rtype",
#         "RIGHT_ATTRS": {"lemma": "be"}
#     },
#     {
#         "LEFT_ID": "rtype",
#         "REL_OP": ">",
#         "RIGHT_ID": "left",
#         "RIGHT_ATTRS": {"DEP": "nsubj"}
#     },
#     {
#         "LEFT_ID": "rtype",
#         "REL_OP": ">",
#         "RIGHT_ID": "right",
#         "RIGHT_ATTRS": {"DEP": {"IN": ["acomp", "attr", "dobj"]}}
#     },
#     {
#         "LEFT_ID": "rtype",
#         "REL_OP": ">",
#         "RIGHT_ID": "question_mark",
#         "RIGHT_ATTRS": {"ORTH": "?"},
#     },
# ]

# request_confirmation_with_negation_pattern = [
#     {
#         "RIGHT_ID": "rtype",
#         "RIGHT_ATTRS": {"lemma": "be"}
#     },
#     {
#         "LEFT_ID": "rtype",
#         "REL_OP": ">",
#         "RIGHT_ID": "left",
#         "RIGHT_ATTRS": {"DEP": "nsubj"}
#     },
#     {
#         "LEFT_ID": "rtype",
#         "REL_OP": ">",
#         "RIGHT_ID": "right",
#         "RIGHT_ATTRS": {"DEP": {"IN": ["acomp", "attr", "dobj"]}}
#     },
#     {
#         "LEFT_ID": "rtype",
#         "REL_OP": ">",
#         "RIGHT_ID": "question_mark",
#         "RIGHT_ATTRS": {"ORTH": "?"},
#     },
#     {
#         "LEFT_ID": "rtype",
#         "REL_OP": ">",
#         "RIGHT_ID": "negation",
#         "RIGHT_ATTRS": {"DEP": "neg"},
#     },
# ]

# request_confirmation2_pattern = [
#     {
#         "RIGHT_ID": "rtype",
#         "RIGHT_ATTRS": {"lemma": "be"}
#     },
#     {
#         "LEFT_ID": "rtype",
#         "REL_OP": ">",
#         "RIGHT_ID": "right",
#         "RIGHT_ATTRS": {"DEP": {"IN": ["acomp", "attr", "dobj"]}}
#     },
#     {
#         "LEFT_ID": "right",
#         "REL_OP": ">",
#         "RIGHT_ID": "left",
#         "RIGHT_ATTRS": {"DEP": "nsubj"}
#     },
#     {
#         "LEFT_ID": "rtype",
#         "REL_OP": ">",
#         "RIGHT_ID": "question_mark",
#         "RIGHT_ATTRS": {"ORTH": "?"},
#     },
# ]

# request_confirmation2_with_negation_pattern = [
#     {
#         "RIGHT_ID": "rtype",
#         "RIGHT_ATTRS": {"lemma": "be"}
#     },
#     {
#         "LEFT_ID": "rtype",
#         "REL_OP": ">",
#         "RIGHT_ID": "right",
#         "RIGHT_ATTRS": {"DEP": {"IN": ["acomp", "attr", "dobj"]}}
#     },
#     {
#         "LEFT_ID": "right",
#         "REL_OP": ">",
#         "RIGHT_ID": "left",
#         "RIGHT_ATTRS": {"DEP": "nsubj"}
#     },
#     {
#         "LEFT_ID": "rtype",
#         "REL_OP": ">",
#         "RIGHT_ID": "question_mark",
#         "RIGHT_ATTRS": {"ORTH": "?"},
#     },
#     {
#         "LEFT_ID": "rtype",
#         "REL_OP": ">",
#         "RIGHT_ID": "negation",
#         "RIGHT_ATTRS": {"DEP": "neg"},
#     },
# ]

# action_names_to_intjs = {
#     'Greet': ['hi', 'hey', 'hello', 'hej'],
#     'Thank': ['thank'],
#     'Backchannel': ['hmm'],
#     'Affirm': ['yes', 'yeah', 'yeup', 'yup'],
#     'Deny': ['no', 'nah', 'nej', 'nope']
# }

# request_information_with_negation_pattern = {

# }

# request_information_pattern = {
#     # {
#     #     "RIGHT_ID": "rtype",
#     #     "RIGHT_ATTRS": {"lemma": "be"}
#     # },
#     # {
#     #     "LEFT_ID": "rtype",
#     #     "REL_OP": ">",
#     #     "RIGHT_ID": "left",
#     #     "RIGHT_ATTRS": {"DEP": "nsubj"}
#     # },
#     # {
#     #     "LEFT_ID": "rtype",
#     #     "REL_OP": ">",
#     #     "RIGHT_ID": "right",
#     #     "RIGHT_ATTRS": {"DEP": {"IN": ["acomp", "attr", "dobj"]}}
#     # },
#     # {
#     #     "LEFT_ID": "rtype",
#     #     "REL_OP": ">",
#     #     "RIGHT_ID": "question_mark",
#     #     "RIGHT_ATTRS": {"ORTH": "?"},
#     # },
# }

# request_action_with_negation_pattern = {

# }

# request_action_pattern = {

# }

# question_patterns = {
#     'RequestConfirmation$_pattern_with_negation': request_confirmation_with_negation_pattern,
#     'RequestConfirmation$_pattern': request_confirmation_pattern,
#     'RequestConfirmation$2_pattern_with_negation': request_confirmation2_with_negation_pattern,
#     'RequestConfirmation$2_pattern': request_confirmation2_pattern,
#     # 'RequestInfo$_pattern_with_negation': request_information_with_negation_pattern,
#     # 'RequestInfo$_pattern': request_information_pattern,
#     # 'RequestAction$_pattern_with_negation': request_action_with_negation_pattern,
#     # 'RequestAction$_pattern': request_action_pattern
# }

# request_confirmation_patterns = {
#     'RequestConfirmation$_pattern_with_negation': request_confirmation_with_negation_pattern,
#     'RequestConfirmation$_pattern': request_confirmation_pattern,
#     'RequestConfirmation$2_pattern_with_negation': request_confirmation2_with_negation_pattern,
#     'RequestConfirmation$2_pattern': request_confirmation2_pattern,
# }

# request_info_patterns = {
#     'RequestInfo$_pattern_with_negation': request_information_with_negation_pattern,
#     'RequestInfo$_pattern': request_information_pattern,
# }

# request_action_patterns = {
#     'RequestAction$_pattern_with_negation': request_action_with_negation_pattern,
#     'RequestAction$_pattern': request_action_pattern
# }

# general_patterns = {
#     'Share$with_negation': statement_with_negation_pattern,
#     'Share$': statement_pattern,
# }

# patterns = {

# }


# def _merge_phrases(doc_input):
#     with doc_input.retokenize() as retokenizer:
#         for np in list(doc_input.noun_chunks):
#             attrs = {
#                 "tag": np.root.tag_,
#                 "lemma": np.root.lemma_,
#                 "ent_type": np.root.ent_type_,
#             }
#             retokenizer.merge(np, attrs=attrs)
#     return doc_input


# def _is_question(text: str):
#     _ = text.lower()
#     for q_starter in question_starters:
#         if _.startswith(q_starter):
#             return True
#     return False


# def _get_matching_action_names_by_intj(text: str):
#     matched_actions = []
#     _ = text.lower()
#     for action_name, intjs in action_names_to_intjs.items():
#         for intj in intjs:
#             if intj in _:
#                 matched_actions.append(action_name)
#     return matched_actions


# def _get_tense_name_from_postag(postag):
#     if postag == "VBD":  # Past tense
#         return 'past'
#     elif postag == "VBP" or postag == "VBZ":  # Present tense
#         return 'present'
#     elif postag == "MD":  # Future tense
#         return 'future'


# def _get_relations(match, pattern, doc):
#     relation = {}
#     relations = []
#     match_id, token_ids = match
#     negation = False
#     for i in range(len(token_ids)):
#         match_key = pattern[i]["RIGHT_ID"]
#         match_text = doc[token_ids[i]].text
#         match_lemma = doc[token_ids[i]].lemma_
#         match_tag = doc[token_ids[i]].tag_
#         token = doc[token_ids[i]]

#         if match_key:
#             if match_key == 'negation':
#                 negation = True
#             elif match_key == 'rtype':
#                 if match_lemma == 'be':
#                     relation[match_key] = 'is'
#                 if token.tag_ != 'VB':
#                     tense = _get_tense_name_from_postag(token.tag_)
#                     relation['tense'] = str(tense)
#             elif match_key == 'optional_be_next_to_root_be':
#                 tense_arr = token.morph.get("Tense")
#                 if len(tense_arr) > 0:
#                     relation['tense'] = str(tense_arr[0])
#             elif match_tag == '.':
#                 pass
#             else:
#                 relation[match_key] = match_text
#     relation['negation'] = negation
#     for possible_action_name in possible_action_names:
#         rel = deepcopy(relation)
#         rel['action_name'] = possible_action_name
#         relations.append(rel)
#     return relations


# def _get_match(pattern_key, doc):
#     matcher.add(pattern_key, [patterns[pattern_key]])
#     matches = matcher(doc)
#     matcher.remove(pattern_key)
#     if matches:
#         return matches[0]


# def get_relations_from_text(text):
#     global patterns, possible_action_names
#     doc = nlp(text)
#     doc = _merge_phrases(doc)
#     patterns = {}

#     possible_action_names = []

#     if _is_question(text):
#         if str(text).lower().startswith(('is', 'was', 'will', 'were', 'am', 'are')):
#             possible_action_names.append('RequestConfirmation')
#             patterns.update(request_confirmation_patterns)
#         elif str(text).lower().startswith(('what', 'how', 'when', 'where')):
#             possible_action_names.append('RequestInfo')
#             patterns.update(request_confirmation_patterns)
#         elif str(text).lower().startswith(('can', 'could', 'would')):
#             possible_action_names.append('RequestAction')
#             patterns.update(request_confirmation_patterns)
#         # patterns.update(question_patterns)
#     else:
#         patterns.update(general_patterns)

#     relations = []

#     matched_intj_action_names = _get_matching_action_names_by_intj(text)
#     if len(matched_intj_action_names) > 0:
#         relations.append({'left': 'I',
#                           'rtype': 'action',
#                           'tense': 'present',
#                           'object': 'YOU',
#                           'negation': False,
#                           'action_name': matched_intj_action_names
#                           })

#     for pattern_key, pattern in patterns.items():
#         match = _get_match(pattern_key, doc)
#         if match:
#             relations.extend(_get_relations(match, pattern, doc))
#     return relations


# if __name__ == '__main__':
#     sentence = 'What is your problem?'
#     relations = get_relations_from_text(sentence)
#     for relation in relations:
#         print(relation)

#     #
#     # doc2 = nlp(sentence)
#     # doc2 = _merge_phrases(doc2)
#     # displacy.serve(doc2, style='dep', options={'collapse_phrases': True, 'collapse_punct': False, 'add_lemma': True},
#     #                host='[REDACTED_IP]', port=5001)
