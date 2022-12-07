# -*- coding: utf-8 -*-
# @Time    : 2021/9/14 16:08
# @Author  : ZhaoXiangPeng
# @File    : replace.py

from ReSpider.db.mongodb import AsyncMongoDB

file = open('../JS2/stringMap.txt', encoding='utf-8')
string = file.read()
stringList = string.split('>|<')
print(len(stringList))
stringMap = {}
for i in range(len(stringList)):
    stringMap[i] = stringList[i]

print(stringMap)
JSX = open('../JS2/jsx.js', encoding='utf-8').read()

JSX = JSX.replace('_$yJ', 'window').replace('var window = window', 'var _$yJ = window')  # 替换window
for k, v in stringMap.items():
    JSX = JSX.replace(f'_$Vm[{k}]', f'"{v}"')
f = open('../JS2/jsx_replace.js', 'w', encoding='utf-8')
f.write(JSX)
f.close()
