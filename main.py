from convokit import Corpus, download
corpus = Corpus(filename=download("switchboard-corpus"))

conv = corpus.random_conversation()

for utt in conv.iter_utterances():
    print(utt.id + ': ' + utt.text + '\nMeta: ' + utt.meta)

