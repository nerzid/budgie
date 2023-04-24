# we use MultiWoZ 2.4.
import json
import spacy
from spacy import displacy

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


if __name__ == '__main__':
    # print(read_file(5))

    text = "I'd like to eat a hamburger"
    tokens = nlp(text)
    # doc = nlp(text)

    for token in tokens:
        print("Text:" + token.text + " POSTag: " + token.pos_ + " Tag: " + token.tag_)
        print(
            f'{token.text:{8}} {token.pos_:{6}} {token.tag_:{6}} {token.dep_:{6}} {spacy.explain(token.pos_):{20}} {spacy.explain(token.tag_)}')
