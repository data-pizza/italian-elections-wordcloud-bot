
#Script per la generazione di un'unica lista di stop words, a partire da quelle fornite dalle maggiori librerie Python

import spacy
import nltk
from stop_words import get_stop_words
from nltk.corpus import stopwords
nlp = spacy.load('it_core_news_lg')

print(len(stopwords.words("italian")))
print(len(get_stop_words("italian")))
print(len(nlp.Defaults.stop_words))

STOP = set(stopwords.words("italian")) | set(get_stop_words("italian")) | set(nlp.Defaults.stop_words)
print(len(STOP))
with open("STOP.txt", "w") as f:
    for word in STOP:
        f.write(word+",")