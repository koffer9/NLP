
file_base = './test'
import os
import jieba
import re
import sys
import chardet
import codecs

def cut(string): return ' '.join(jieba.cut(string))
print('total database files are {}'.format(len(os.listdir(file_base))))

corpus = [
    cut(open(os.path.join(file_base, f),'r',encoding='utf-8').read()) for f in os.listdir(file_base)
]
#print(corpus[0:5])

#for text use
'''
corpus = [
    'This is the first document.',
    'This is the second second document.',
    'And the third one.',
    'Is this the first document?',
]
'''

from sklearn.feature_extraction.text import TfidfVectorizer
#https://www.jianshu.com/p/4bc7fbdafdeb
#https://blog.csdn.net/laobai1015/article/details/80451371
#https://www.jianshu.com/p/c7e2771eccaa
vectorizer = TfidfVectorizer() #tf-idf的特征矩阵
tfidf = vectorizer.fit_transform(corpus) #将文本corpus输入， 得到tf-idf矩阵，稀疏矩阵表示法
tfidf_array = tfidf.toarray()
transposed_tfidf = tfidf.transpose()
transposed_tfidf_array = transposed_tfidf.toarray()
#print('vocabulary is {}'.format(vectorizer.vocabulary_))#每个词汇在矩阵中的列位置
print('min is {}'.format(min(vectorizer.vocabulary_.values())))
print('max is {}'.format(max(vectorizer.vocabulary_.values())))#总词汇对应的最大列数n，含0列则总共为n+1列，也是n+1个词汇
#print('tfidf array is {}'.format(tfidf_array))#每个词汇在每句话中的tfidf权值矩阵，越高表示越重要，0表示在该句中未出现
print('tfidf array shape is {}'.format(tfidf_array.shape))#每个词汇在每句话中的tfidf权值矩阵尺寸
#print('transposed tfidf array is {}'.format(transposed_tfidf_array))#transposed后矩阵
print('transposed tfidf array shape is {}'.format(transposed_tfidf_array.shape))#transposed后矩阵尺寸

import numpy as np
#print('condition is {}'.format(transposed_tfidf_array[6]))
#print('np.where is {}'.format(np.where(transposed_tfidf_array[6])))

def get_word_id(word): #获得输入单词在tfidf权值矩阵内的列数
    return vectorizer.vocabulary_.get(word, None)
#print('get_word_id is {}'.format(get_word_id('this')))

from functools import reduce
from operator import and_
from scipy.spatial.distance import cosine

def get_candidates_ids(input_string): #获得输入句子各个单词在tfidf权值矩阵内的各个列数
    return [get_word_id(c) for c in cut(input_string).split()]
#print('get_candidate_ids is {}'.format(get_candidates_ids('this is a car')))

def get_candidates_pat(input_string): #获得输入句子切词后的结果，用|分隔
    return '({})'.format('|'.join(cut(input_string).split()))
#print('get_candidate_pat is {}'.format(get_candidates_pat('this is a car')))

def search_enginer(query):
    candidates_ids = get_candidates_ids(query)#获得切词后各词在tfidf权值矩阵中的列数的列表
    print('candidates_ids is {}'.format(candidates_ids))
    v1 = vectorizer.transform([cut(query)]).toarray()[0]#获得query的词在语料的tfidf矩阵中的出现的情况，取该矩阵第一行[0]
    #print('v1 is {}'.format(v1))
    candidates = [set(np.where(transposed_tfidf_array[_id])[0]) for _id in candidates_ids]#获得每个query词在预料中出现的列数
    print('candidates are {}'.format(candidates))
    merged_candidates = reduce(and_, candidates)#获得每个query词在语料中都出现的交集
    print('merged_candidates are {}'.format(merged_candidates))
    pat = re.compile(get_candidates_pat(query))
    #print('pat is {}'.format(pat))
    vector_with_id = [(tfidf[i], i) for i in merged_candidates]
    sorted_vector_with_ids = sorted(vector_with_id, key=lambda x: cosine(x[0].toarray(), v1))
    sorted_ids = [i for v, i in sorted_vector_with_ids]
    print('sorted ids is {}'.format(sorted_ids))
    for c in sorted_ids:
        #output = pat.sub(repl='** \g<1> ** ', string=corpus[c])
        output = corpus[c]
        yield ''.join(output.split())

query='原油 油价'

with open('sz_result.txt', 'w', encoding='utf-8') as f:
    for i, document in enumerate(search_enginer(query)):
        f.write('## search result {}\n'.format(i+1))
        f.write(document + '\n')


print('{} results found!'.format(i+1))
