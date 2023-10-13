# we use MultiWoZ 2.4.
import json
import spacy
from spacy import displacy
from spacy.matcher import DependencyMatcher

# data_path = 'C:/Users/eyildiz/Desktop/Datasets/MULTIWOZ2.4/data.json'
nlp = spacy.load('en_core_web_sm')


# def read_file(num_lines):
#     result = ""
#
#     f = open(data_path)
#     data = json.load(f)
#
#     for i in data["SNG01856.json"]["log"]:
#         tokens = nlp(i['text'])
#         print('Sentence: ' + str(i))
#         for token in tokens:
#             if str(token.tag_).startswith("VB"):
#                 print("Token:" + token.text + " POSTag: " + token.pos_ + " Tag: " + token.tag_ + " Morph:" + str(
#                     token.morph))
#         print('\n')

doer_finder_pattern = [
    {
        "RIGHT_ID": "AUX",
        "RIGHT_ATTRS": {"POS":"AUX"}
    },
    {
        "LEFT_ID": "AUX",
        "REL_OP": ">",
        "RIGHT_ID": "DOER",
        "RIGHT_ATTRS": {"DEP":"nsubj"}
    },
    {
        "LEFT_ID": "AUX",
        "REL_OP": ">",
        "RIGHT_ID": "STATE",
        "RIGHT_ATTRS":{"DEP":"acomp"}
    }
]
if __name__ == '__main__':
    # print(read_file(5))

    # text = "We also are indeed ready for departure."
    text = "I am looking for a place to stay that cheap price range and it should be in a type of hotel."
    doc = nlp(text)
    # doc = nlp(text)

    for token in doc:
        print("Text:" + token.text + " POSTag: " + token.pos_ + " Tag: " + token.tag_)
        print(
            f'{token.text:{8}} {token.pos_:{6}} {token.tag_:{6}} {token.dep_:{6}} {spacy.explain(token.pos_):{20}} {spacy.explain(token.tag_)}')
    matcher = DependencyMatcher(nlp.vocab)
    matcher.add("DOER FINDER", [doer_finder_pattern])
    matches = matcher(doc)
    # match_id, token_ids = matches[0]
    # for i in range(len(token_ids)):
    #     print(doer_finder_pattern[i]["RIGHT_ID"] + ":", doer_finder_pattern[token_ids[i]].text)
    displacy.serve(doc, style="dep", port=[REDACTED_PORT])
