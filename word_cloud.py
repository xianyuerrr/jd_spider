import json
from collections import Counter
import pandas as pd
from wordcloud import WordCloud
import jieba
import matplotlib.pyplot as plt
from nltk.corpus import stopwords


def word_cloud_creation(filename):
    """创建词云，并进行分词"""
    jieba.load_userdict("word_dicts.txt")
    with open(filename) as f:
        text = f.readlines()
    # word_list = jieba.cut(text, cut_all=False)
    word_list = text
    # 精确模式
    wl = ' '.join(word_list)
    # wl = Counter(word_list)
    # print(wl.most_common(10))
    return wl


def word_cloud_settings():
    """设置词云的属性"""
    stopwords = list(set(pd.read_csv("chineseStopWords.txt", index_col=False, quoting=3, sep="\t", names=['stopword'],
                            encoding='GBK')['stopword'].tolist()))
    # with open("./chineseStopWords.txt") as f:
    #     stopwords = f.readlines()
    wc = WordCloud(
        background_color='white',
        max_words=200,
        stopwords=stopwords,
        relative_scaling=.5,
        max_font_size=100,
        height=1200,
        width=1500,
        random_state=30,
        font_path='C:\Windows\Fonts\simfang.ttf',
        collocations=False
    )
    return wc


def word_cloud_implementation(wl, wc, path, title):
    """生成词云，并展示"""
    my_words = wc.generate(wl)
    sort = my_words.process_text(wl)
    sort = sorted(sort.items(), key=lambda e: e[1], reverse=True)
    with open(f"{path}/高频词-{title}.txt", 'w', encoding='utf-8') as f:
        f.write(json.dumps(sort, ensure_ascii=False))
    # my_words = wc.fit_words(wl)
    plt.figure()
    plt.imshow(my_words)
    plt.axis('off')
    wc.to_file(f'{path}/word_cloud-{title}.png')
    # plt.show()
