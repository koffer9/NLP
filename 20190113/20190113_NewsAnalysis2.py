import pandas as pd
pd.set_option('display.max_columns', None)
import json
import jieba
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
#https://www.jianshu.com/p/4bc7fbdafdeb
#https://blog.csdn.net/laobai1015/article/details/80451371
#https://www.jianshu.com/p/c7e2771eccaa
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.externals import joblib

#for test use
'''
corpus = [
    'This is the first document.',
    'This is the second second document.',
    'And the third one.',
    'Is this the first document?',
]
'''

def cut(string): return ' '.join(jieba.cut(string))

def get_corpus(n):
    for artNo in range(n):
        if isinstance(df['content'][artNo], float): # 排除float型空行
            corpus.append('')
            sources.append('x')
            continue
        corpus.append(cut(df['content'][artNo].replace('\n','').replace('\r','').replace(u'\u3000','')))
        if 'site' in df['feature'][artNo]: sources.append(json.loads(df['feature'][artNo])['site'])
        else: sources.append(json.loads('{"site":"x"}')['site'])

def get_tfidf_array(corpus):
    vectorizer = TfidfVectorizer() #tf-idf的特征矩阵
    tfidf = vectorizer.fit_transform(corpus) #将文本corpus输入， 得到tf-idf矩阵，稀疏矩阵表示法
    words = vectorizer.get_feature_names() #词汇表
    tfidf_array = tfidf.toarray() #每个词汇在每句话中的tfidf权值矩阵，越高表示越重要，0表示在该句中未出现
    #transposed_tfidf = tfidf.transpose()
    #transposed_tfidf_array = transposed_tfidf.toarray()
    #print('vocabulary is {}'.format(vectorizer.vocabulary_))#每个词汇在矩阵中的列位置
    #print('words are {}'.format(vectorizer.get_feature_names()))
    #print('tfidf array is {}'.format(tfidf_array))
    #print('min is {}'.format(min(vectorizer.vocabulary_.values())))
    #print('max is {}'.format(max(vectorizer.vocabulary_.values())))#总词汇对应的最大列数n，含0列则总共为n+1列，也是n+1个词汇
    #print('tfidf array shape is {}'.format(tfidf_array.shape))#每个词汇在每句话中的tfidf权值矩阵尺寸
    #print('transposed tfidf array is {}'.format(transposed_tfidf_array))#transposed后矩阵
    #print('transposed tfidf array shape is {}'.format(transposed_tfidf_array.shape))#transposed后矩阵尺寸
    return tfidf_array

'''
n = 3 #提取前3位关键词
for (sentence, source, weigh) in zip(test_corpus, sources, tfidf_array):
    print('sentence = {}'.format(sentence))
    print('source = {}'.format(source))
    print('weigh = {}'.format(weigh))
    loc = np.argsort(-weigh)
    for i in range(n):
        print('-{}: {} {}'.format(str(i + 1), words[loc[i]], weigh[loc[i]]))
    print('\n')
'''

def output(algorism,predict_label):
    hit=0
    for i in range(len(predict_label)):
        if predict_label[i]==sources[train_size+i]: hit+=1
    print(algorism + ':')
    print('predict_labels are {}'.format(predict_label))
    print('Actual__labels are {}'.format(sources[train_size:]))
    print('{} Successful rate, with {}/{} hits\n'.format(round(hit/len(predict_label),2),hit,len(predict_label)))
    return

def by_logisticregression(train_X, train_Y,sample_X):
    clf = LogisticRegression()
    clf.fit(train_X, train_Y)
    joblib.dump(clf, 'LogisticRegression_model.m')
    #clf = joblib.load('LogisticRegression_model.m')
    predict_label = clf.predict(sample_X)
    return predict_label

def by_knn(train_X, train_Y,sample_X):
    neigh = KNeighborsClassifier()
    neigh.fit(train_X, train_Y)
    joblib.dump(neigh, 'KNN_model.m')
    #neigh = joblib.load('KNN_model.m')
    predict_label = neigh.predict(sample_X)
    return predict_label

def by_svm(train_X, train_Y,sample_X):
    clf = svm.SVC()
    clf.fit(train_X, train_Y)
    joblib.dump(clf, 'SVM_model.m')
    #clf = joblib.load('SVM_model.m')
    predict_label = clf.predict(sample_X)
    return predict_label

def by_bayes(train_X, train_Y,sample_X):
    clf = GaussianNB()
    clf.fit(train_X, train_Y)
    joblib.dump(clf, 'Bayes_model.m')
    #clf = joblib.load('Bayes_model.m')
    predict_label = clf.predict(sample_X)
    return predict_label

def by_decisiontree(train_X, train_Y,sample_X):
    clf = tree.DecisionTreeClassifier()
    clf.fit(train_X, train_Y)
    joblib.dump(clf, 'DecisionTree_model.m')
    #clf = joblib.load('DecisionTree_model.m')
    predict_label = clf.predict(sample_X)
    return predict_label


#读取文章到列表和数据预处理
df = pd.read_csv('sqlResult_1558435.csv', header=0, encoding='gb18030')
print('shape is {}, column={}, rows={}'.format(df.shape,df.shape[1],df.shape[0]))
print(df.columns)
corpus,sources=[],[]
n=1000 #数据集大小
get_corpus(n)
train_size=int(0.95*n) # 训练数据和测试数据比例
#print(corpus)
#print(sources)
tfidf_array = get_tfidf_array(corpus)

output('Logistic Regression',by_logisticregression(tfidf_array[:train_size], sources[:train_size],tfidf_array[train_size:]))
output('K-Nearest-Neighbors',by_knn(tfidf_array[:train_size], sources[:train_size],tfidf_array[train_size:]))
output('Support Vector Machine',by_svm(tfidf_array[:train_size], sources[:train_size],tfidf_array[train_size:]))
output('Bayes - Gaussian',by_bayes(tfidf_array[:train_size], sources[:train_size],tfidf_array[train_size:]))
output('Decision Tree',by_decisiontree(tfidf_array[:train_size], sources[:train_size],tfidf_array[train_size:]))





