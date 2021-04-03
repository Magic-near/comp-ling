import json
import string
import jellyfish

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def find_word(word):
  min_dist = len(word)
  for d_word in dictionary:
    dist = jellyfish.levenshtein_distance(word, d_word)
    if dist < min_dist:
      correct = d_word
      min_dist = dist
  if min_dist == 0:
    print("Встречается в ", dictionary[word])
  else:
    print("Корректное слово: {0}, которое встречается в {1}".format(correct, dictionary[correct]))
    if min_dist > 2:
      print("(другое слово)")
    else:
      print("(опечатка)")
      

if __name__ == '__main__':
  word = input("Введите слово: ")

  with open('clean_corpus.json', 'r') as f:
    data = json.loads(f.readline())

  dictionary = {}
  corpus_without_punct = {}
  for post in data:
    tokens = word_tokenize(data[post]['post_text'])
    punct = string.punctuation + "—" + "«" + "»"
    tokens = [token.lower() for token in tokens if token not in punct]
    stopwords_list = stopwords.words("russian")
    wout_sw = [w for w in tokens if w not in stopwords_list]
    corpus_without_punct[post] = wout_sw
    for w in wout_sw:
      if dictionary.get(w) is None:
        dictionary[w] = [post]
      if post not in dictionary[w]:
        dictionary[w].append(post)

  with open("corpus_without_punct.json", "w") as f:
    json.dump(corpus_without_punct, f, ensure_ascii=False)

  find_word(word)
