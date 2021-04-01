import os
from snownlp import sentiment
import pandas as pd
import snownlp
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from word_cloud import word_cloud_creation, word_cloud_implementation, word_cloud_settings


def clean_data(data):
    """数据清洗"""
    df = data.dropna()  # 消除缺失数据 NaN为缺失数据
    df = pd.DataFrame(df.iloc[:, 0].unique())  # 数据去重
    return df
    # print('数据清洗后：', len(df))


def clean_repeat_word(raw_str, reverse=False):
    """去除评论中的重复使用的词汇"""
    if reverse:
        raw_str = raw_str[::-1]
    res_str = ''
    for i in raw_str:
        if i not in res_str:
            res_str += i
    if reverse:
        res_str = res_str[::-1]
    return res_str


def processed_data(file_name, to_file_name):
    """清洗完毕的数据，并保存"""
    # comment_data = pd.read_csv(file_name, encoding='gbk',
    #                            sep='\n', index_col=None)
    with open(file_name, 'rb') as f:
        comment_data = pd.read_csv(f, encoding='gbk',
                                   sep='\n', index_col=None)
    df = clean_data(comment_data)
    # ser1 = df.iloc[:, 0].apply(clean_repeat_word)
    # df2 = pd.DataFrame(ser1.apply(clean_repeat_word, reverse=True))
    df2 = pd.DataFrame(df)
    df2.to_csv(to_file_name, encoding='gbk', index_label=None, index=None)


def train(path):
    """训练正向和负向情感数据集，并保存训练模型"""
    sentiment.train(f'{path}/差评.csv', f'{path}/好评.csv')
    sentiment.save('./sentiment.marshal')


sentiment_list = []

res_list = []


def test(filename, to_filename):
    """商品评论-情感分析-测试"""
    with open(filename, 'r', encoding='gbk') as fr:
        for line in fr.readlines():
            s = snownlp.SnowNLP(line)
            if s.sentiments > 0.6:
                res = '喜欢'
                res_list.append(1)
            elif s.sentiments < 0.4:
                res = '不喜欢'
                res_list.append(-1)
            else:
                res = '一般'
                res_list.append(0)
            sent_dict = {
                '情感分析结果': s.sentiments,
                '评价倾向': res,
                '商品评论': line.replace('\n', '')
            }
            sentiment_list.append(sent_dict)
            print(sent_dict)
        df = pd.DataFrame(sentiment_list)
        df.to_csv(to_filename, index=None, encoding='gbk',
                  index_label=None, mode='w')


def data_virtualization(file_name, title):
    """分析结果可视化，以条形图为测试样例"""
    plt.figure()
    font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=14)
    likes = len([i for i in res_list if i == 1])
    common = len([i for i in res_list if i == 0])
    unlikes = len([i for i in res_list if i == -1])

    plt.bar([1], [likes], label='like')
    plt.bar([3], [common], label='common')
    plt.bar([5], [unlikes], label='unlike')

    plt.legend()
    plt.xlabel('result')
    plt.ylabel('value')
    plt.title(f'商品评论情感分析结果-条形图-{title}', FontProperties=font)
    plt.savefig(file_name)
    # plt.show()


def word_cloud_show(file_name, path, title):
    """将商品评论转为高频词汇的词云"""
    wl = word_cloud_creation(file_name)
    wc = word_cloud_settings()
    word_cloud_implementation(wl, wc, path, title)


def main():
    ids = [100008771754, 4217490, 100016285268]
    print(1)
    sc0 = {0: "全部",
           1: "差评",
           2: "中评",
           3: "好评"
           }
    for id in ids:
        print(2)
        path = f'./comment/{id}'
        to_path = f'{path}/清洗后'
        res_path = f'{path}/result'
        for p in [path, to_path, res_path]:
            print(3)
            if not os.path.exists(p):
                os.makedirs(p)
                return
        for score in range(1, 4):
            print(4)
            title = f"{sc0[score]}"
            file_name = f"{path}/{sc0[score]}.csv"
            to_file_name = f"{to_path}/{sc0[score]}.csv"
            res_file_name = f"{res_path}/{sc0[score]}.csv"
            fig_file_name = f"{res_path}/{sc0[score]}.png"
            processed_data(file_name, to_file_name)
            print(f"数据处理完毕，存为{to_file_name}")
            # train()  # 训练正负向商品评论数据集
            test(to_file_name, res_file_name)
            print(f"感情分析完毕，存为{res_file_name}")
            data_virtualization(fig_file_name, title)  # 数据可视化
            word_cloud_show(to_file_name, res_path, title)  # 高频词云


if __name__ == '__main__':
    main()
