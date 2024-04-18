import spacy
from spacy.matcher import DependencyMatcher
from spacy import displacy

# Load English tokenizer, tagger, parser, and NER
nlp = spacy.load("en_core_web_lg")
matcher = DependencyMatcher(nlp.vocab)

question_starters = ['is', 'are', 'was', 'were', 'will', 'do', 'did', 'does',
                     'what', 'when', 'where', 'who', 'why', 'how', 'can', 'would', 'should']

statement_pattern = [
    {
        "RIGHT_ID": "rtype",
        "RIGHT_ATTRS": {"lemma": "be"}
    },
    {
        "LEFT_ID": "rtype",
        "REL_OP": ">",
        "RIGHT_ID": "left",
        "RIGHT_ATTRS": {"DEP": "nsubj"}
    },
    {
        "LEFT_ID": "rtype",
        "REL_OP": ">",
        "RIGHT_ID": "right",
        "RIGHT_ATTRS": {"DEP": {"IN": ["acomp", "attr", "dobj"]}}
    }
]

statement_with_negation_pattern = [
    {
        "RIGHT_ID": "rtype",
        "RIGHT_ATTRS": {"lemma": "be"}
    },
    {
        "LEFT_ID": "rtype",
        "REL_OP": ">",
        "RIGHT_ID": "left",
        "RIGHT_ATTRS": {"DEP": "nsubj"}
    },
    {
        "LEFT_ID": "rtype",
        "REL_OP": ">",
        "RIGHT_ID": "right",
        "RIGHT_ATTRS": {"DEP": {"IN": ["acomp", "attr", "dobj"]}}
    },
    {
        "LEFT_ID": "rtype",
        "REL_OP": ">",
        "RIGHT_ID": "negation",
        "RIGHT_ATTRS": {"DEP": "neg"},
    },
]

request_information_pattern = [
    {
        "RIGHT_ID": "rtype",
        "RIGHT_ATTRS": {"lemma": "be"}
    },
    {
        "LEFT_ID": "rtype",
        "REL_OP": ">",
        "RIGHT_ID": "left",
        "RIGHT_ATTRS": {"DEP": "nsubj"}
    },
    {
        "LEFT_ID": "rtype",
        "REL_OP": ">",
        "RIGHT_ID": "right",
        "RIGHT_ATTRS": {"DEP": {"IN": ["acomp", "attr", "dobj"]}}
    },
    {
        "LEFT_ID": "rtype",
        "REL_OP": ">",
        "RIGHT_ID": "question_mark",
        "RIGHT_ATTRS": {"ORTH": "?"},
    },
]

request_information_with_negation_pattern = [
    {
        "RIGHT_ID": "rtype",
        "RIGHT_ATTRS": {"lemma": "be"}
    },
    {
        "LEFT_ID": "rtype",
        "REL_OP": ">",
        "RIGHT_ID": "left",
        "RIGHT_ATTRS": {"DEP": "nsubj"}
    },
    {
        "LEFT_ID": "rtype",
        "REL_OP": ">",
        "RIGHT_ID": "right",
        "RIGHT_ATTRS": {"DEP": {"IN": ["acomp", "attr", "dobj"]}}
    },
    {
        "LEFT_ID": "rtype",
        "REL_OP": ">",
        "RIGHT_ID": "question_mark",
        "RIGHT_ATTRS": {"ORTH": "?"},
    },
    {
        "LEFT_ID": "rtype",
        "REL_OP": ">",
        "RIGHT_ID": "negation",
        "RIGHT_ATTRS": {"DEP": "neg"},
    },
]

request_information2_pattern = [
    {
        "RIGHT_ID": "rtype",
        "RIGHT_ATTRS": {"lemma": "be"}
    },
    {
        "LEFT_ID": "rtype",
        "REL_OP": ">",
        "RIGHT_ID": "right",
        "RIGHT_ATTRS": {"DEP": {"IN": ["acomp", "attr", "dobj"]}}
    },
    {
        "LEFT_ID": "right",
        "REL_OP": ">",
        "RIGHT_ID": "left",
        "RIGHT_ATTRS": {"DEP": "nsubj"}
    },
    {
        "LEFT_ID": "rtype",
        "REL_OP": ">",
        "RIGHT_ID": "question_mark",
        "RIGHT_ATTRS": {"ORTH": "?"},
    },
]

request_information2_with_negation_pattern = [
    {
        "RIGHT_ID": "rtype",
        "RIGHT_ATTRS": {"lemma": "be"}
    },
    {
        "LEFT_ID": "rtype",
        "REL_OP": ">",
        "RIGHT_ID": "right",
        "RIGHT_ATTRS": {"DEP": {"IN": ["acomp", "attr", "dobj"]}}
    },
    {
        "LEFT_ID": "right",
        "REL_OP": ">",
        "RIGHT_ID": "left",
        "RIGHT_ATTRS": {"DEP": "nsubj"}
    },
    {
        "LEFT_ID": "rtype",
        "REL_OP": ">",
        "RIGHT_ID": "question_mark",
        "RIGHT_ATTRS": {"ORTH": "?"},
    },
    {
        "LEFT_ID": "rtype",
        "REL_OP": ">",
        "RIGHT_ID": "negation",
        "RIGHT_ATTRS": {"DEP": "neg"},
    },
]

action_names_to_intjs = {
    'Greet': ['hi', 'hey', 'hello', 'hej'],
    'Thank': ['thank'],
    'Backchannel': ['hmm'],
    'Affirm': ['yes', 'yeah', 'yeup', 'yup'],
    'Deny': ['no', 'nah', 'nej', 'nope']
}

question_patterns = {
    'RequestInfo$_pattern_with_negation': request_information_with_negation_pattern,
    'RequestInfo$_pattern': request_information_pattern,
    'RequestInfo$2_pattern_with_negation': request_information2_with_negation_pattern,
    'RequestInfo$2_pattern': request_information2_pattern,
}

general_patterns = {
    'Share$with_negation': statement_with_negation_pattern,
    'Share$': statement_pattern,
}

patterns = {

}


def _merge_phrases(doc_input):
    with doc_input.retokenize() as retokenizer:
        for np in list(doc_input.noun_chunks):
            attrs = {
                "tag": np.root.tag_,
                "lemma": np.root.lemma_,
                "ent_type": np.root.ent_type_,
            }
            retokenizer.merge(np, attrs=attrs)
    return doc_input


def _is_question(text: str):
    _ = text.lower()
    for q_starter in question_starters:
        if _.startswith(q_starter):
            return True
    return False


def _get_matching_action_names_by_intj(text: str):
    matched_actions = []
    _ = text.lower()
    for action_name, intjs in action_names_to_intjs.items():
        for intj in intjs:
            if intj in _:
                matched_actions.append(action_name)
    return matched_actions


def _get_tense_name_from_postag(postag):
    if postag == "VBD":  # Past tense
        return 'past'
    elif postag == "VBP" or postag == "VBZ":  # Present tense
        return 'present'
    elif postag == "MD":  # Future tense
        return 'future'


def _get_relation(match, pattern, doc, action_name):
    relation = {}

    match_id, token_ids = match
    negation = False
    for i in range(len(token_ids)):
        match_key = pattern[i]["RIGHT_ID"]
        match_text = doc[token_ids[i]].text
        match_lemma = doc[token_ids[i]].lemma_
        match_tag = doc[token_ids[i]].tag_
        token = doc[token_ids[i]]

        if match_key:
            if match_key == 'negation':
                negation = True
            elif match_key == 'rtype':
                if match_lemma == 'be':
                    relation[match_key] = 'is'
                if token.tag_ != 'VB':
                    tense = _get_tense_name_from_postag(token.tag_)
                    relation['tense'] = str(tense)
            elif match_key == 'optional_be_next_to_root_be':
                tense_arr = token.morph.get("Tense")
                if len(tense_arr) > 0:
                    relation['tense'] = str(tense_arr[0])
            elif match_tag == '.':
                pass
            else:
                relation[match_key] = match_text
    relation['negation'] = negation
    relation['action_name'] = action_name
    return relation


def _get_match(pattern_key, doc):
    matcher.add(pattern_key, [patterns[pattern_key]])
    matches = matcher(doc)
    if matches:
        return matches[0]


def get_relations_from_text(text):
    global patterns
    doc = nlp(text)
    doc = _merge_phrases(doc)
    patterns = {}

    if _is_question(text):
        patterns.update(question_patterns)
    else:
        patterns.update(general_patterns)

    relations = []

    matched_intj_action_names = _get_matching_action_names_by_intj(text)
    for action_name in matched_intj_action_names:
        relations.append({'left': 'I',
                          'rtype': 'action',
                          'tense': 'present',
                          'object': 'YOU',
                          'negation': 'false',
                          'action_name': action_name
                          })

    for pattern_key, pattern in patterns.items():
        match = _get_match(pattern_key, doc)
        if match:
            relations.append(_get_relation(match, pattern, doc, pattern_key.split('$')[0]))
    return relations


if __name__ == '__main__':
    sentence = 'Is your eye teary?'

    doc2 = nlp(sentence)
    doc2 = _merge_phrases(doc2)
    print(get_relations_from_text(sentence))

    # displacy.serve(doc, style='dep', options={'collapse_phrases': True, 'collapse_punct': False, 'add_lemma': True},
    #                host='[REDACTED_IP]', port=5001)
