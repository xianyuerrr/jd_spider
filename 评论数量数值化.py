import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os

from string_to_yuan import string_to_yuan

print(os.getcwd())

path = "./data.csv"
table = pd.read_csv(path, header=0)

pinglun = table["评论数量"].apply(lambda x: x.strip('\n').strip('\t').strip('\n').strip('+'))

table["评论数量"] = pinglun.apply(string_to_yuan)
table.sort_values("评论数量", inplace=True, ascending=False)
table.to_csv("data-评论数值化.csv", encoding="utf_8_sig", index=False)
