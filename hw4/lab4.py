import pymorphy2
import json
import pandas as pd
import numpy as np

if __name__ == '__main__':
    with open('corpus_without_punct.json', 'r') as f:
        data = json.loads(f.readline())
    analyzer = pymorphy2.MorphAnalyzer()
    tagged_corpus, tag_sum = {}, []
    for post in data:
        text, post_counter = [], {}
        for word in data[post]:
            normalized = analyzer.parse(word)[0].normal_form
            tag = analyzer.parse(word)[0].tag.POS
            if tag != None:
                text.append((normalized, tag))
                if tag not in post_counter:
                    post_counter[tag] = 0
                post_counter[tag] += 1
        tagged_corpus[post] = text
        tag_sum.append(post_counter)

    general_sum = []
    for post in tag_sum:
        post_sum = 0
        for tag in post:
            post_sum += post.get(tag)
        general_sum.append(post_sum)

    tag_percent = {}
    for post in tag_sum:
        for i in range(len(tag_sum)):
            p = {}
            for tag in post:
                m = round(post[tag]/general_sum[i], 2)
                p[tag] = m
            tag_percent[i] = p
    
    df = pd.DataFrame.from_dict(tag_percent)

    result = []
    for post in tag_percent:
        for tag in tag_percent.get(post):
            if tag_percent.get(post)[tag] > 2 * np.std(df.loc[tag]):
                if post not in result:
                    result.append(post)
    print(result)

    with open("tagged_corpus.json", "w") as f:
        json.dump(tagged_corpus, f, ensure_ascii=False)
