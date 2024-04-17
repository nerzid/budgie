import spacy
from spacy.matcher import DependencyMatcher
from spacy import displacy

# Load English tokenizer, tagger, parser, and NER
nlp = spacy.load("en_core_web_lg")
matcher = DependencyMatcher(nlp.vocab)

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

patterns = {
    'Share$with_negation': statement_with_negation_pattern,
    'Share$': statement_pattern,
    'RequestInfo$_pattern_with_negation': request_information_with_negation_pattern,
    'RequestInfo$_pattern': request_information_pattern,
    'RequestInfo$2_pattern_with_negation': request_information2_with_negation_pattern,
    'RequestInfo$2_pattern': request_information2_pattern
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


def get_relation_from_text(text):
    doc = nlp(text)
    doc = _merge_phrases(doc)

    for pattern_key, pattern in patterns.items():
        match = _get_match(pattern_key, doc)
        if match:
            return _get_relation(match, pattern, doc, pattern_key.split('$')[0])
    return None


if __name__ == '__main__':
    sentence = 'Is your beautiful vision blurry?'

    print(get_relation_from_text(sentence))

    doc = nlp(sentence)
    doc = _merge_phrases(doc)
# displacy.serve(doc, style='dep', options={'collapse_phrases': True, 'collapse_punct': False, 'add_lemma': True})
