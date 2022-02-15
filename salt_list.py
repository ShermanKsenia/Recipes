import json
from termios import VT1
import pandas as pd

salt_list = [
    "Соль", "Сахар", "Оливковое масло", "Молотый черный перец", "Лимонный сок", 
    "Растительное масло", "Майонез", "Бальзамический уксус", "Уксус", "Петрушка",
    "Оливковое масло extra virgin", "Свежемолотый черный перец"]

from collections import Counter

columns = ['page', 'type', 'name', 'ingredient', 'measure']
data = pd.read_csv('recipies_new.csv', sep='\t', names=columns)

data2 = data.groupby("name").agg({"ingredient": list})

bigram_list = []
for element in data2["ingredient"]:
    work_list = []
    for i in range(len(element)):
        for j in range(len(element)):
            if element[i] not in salt_list and element[j] not in salt_list:
                bigram = (element[i], element[j])
                bigram = tuple(sorted(bigram))
                if element[i] != element[j] and bigram not in work_list:
                    work_list.append(bigram)
    bigram_list.extend(work_list)

bigram_count = Counter(bigram_list)
bigram_count = [{f'{v[0]} и {v[1]}': k} for v, k in bigram_count.most_common(50)]

with open('salt_list', 'w', encoding='utf-8') as f:
    f.write(json.dumps(bigram_count, ensure_ascii=False))