import pandas as pd
pd.set_option('display.max_columns', None)
import jieba
import jieba.posseg as pseg
import random
import string

#读取文章到列表
df = pd.read_csv('sqlResult_1558435.csv', header=0, encoding='gb18030')
#print(df.head(10))
print('shape is {}, column={}, rows={}'.format(df.shape,df.shape[1],df.shape[0]))
print(df.columns)

# 以下用来替代word2vec训练的结果，找出说的近似词，从同学作业中引用https://github.com/wangliangster/NLP-Course/blob/master/Project1.ipynb
shuo=['说','指出','声称','说道', '告诉', '认为', '相信', '宣称', '问', '写道', '反问', '表示', '提到', '觉得', '谈到', '断言', '看来', '确信', '答道', '谈及', '坚称', '猜测', '辩称', '并不认为', '透露', '指称', '称', '说出', '表明', '提及', '否认', '坦言', '坦承', '询问', '特别强调', '自述', '怀疑', '断定', '明确指出', '指责', '追问', '谈起', '推测', '坚信', '提过', '强调', '指控', '反驳', '阐述', '论及', '引用', '详述', '记述', '述及', '解释', '讲', '回忆起', '喊道', '透漏']

#数据预处理，拆分段落，拆分句子，删除全角空格
def get_sentence(start,count):
    all_sentence=[]
    for artNo in range(start, start+count, 1): #读取文章
        #print('Art No {}/{}'.format(artNo,df.shape[0]))
        if isinstance(df['content'][artNo],float): continue #排除float型空行
        pNo=0
        for paragraph1 in df['content'][artNo].split('\n'): #拆分段落
            if paragraph1=='': continue
            for paragraph2 in paragraph1.strip(u'\u3000').split('\r'): #删除全角空格，继续拆分段落
                if paragraph2 == '': continue
                in_between=False #判断是否在局部整体中
                for i in range(len(paragraph2)-1): #标记句子分割点
                    if paragraph2[i] in comb['s'] + comb['e']+quote['s']+quote['e']: in_between=not in_between #字符进入局部整体
                    if paragraph2[i] in ['。','？','！']and not in_between:
                        paragraph2=paragraph2.replace(paragraph2[:i + 1], paragraph2[:i + 1] + '||')
                #print(paragraph2)
                sNo=0
                for sentence in paragraph2.split('||'):
                    all_sentence.append(sentence)
                    #print('A{}.P{}.S{}={}'.format(artNo,pNo,sNo,sentence))
                    sNo+=1
                pNo+=1
    return all_sentence

#改变jieba分词对词性的定义
def replace_flag(words, flags, old_words,new_flag):
    for i in range(len(words)):
        if words[i] in old_words:
            flags[i]=new_flag
    return

#对于局部不可分割的整体，进行重新合并。比如括号内、引号内
def comb_flag(words,flags,flag_s,flag_e,new_flag):
    m=0
    while flag_s in flags and flag_e in flags:
        s,e=99999,99999
        if m>10: break
            #print(words)
            #print(flags)
        for i in range(len(words)): #寻找起止标记
            if flags[i] == flag_s: s = i
            if flags[i] == flag_e:
                e = i
                break
        if e-s<10: new_flag='comb'
        delete=0
        for i in range(s, e, 1):
            words[i - delete] = ''.join([words[i - delete], words[i - delete + 1]])
            del words[i - delete + 1]
            flags[i - delete] = new_flag
            del flags[i - delete + 1]
            delete += 1
            if i == e + s - 1: break
        m+=1


#废弃的程序
def group_right_n(word, flag, k):
    i=k
    output=[word[k]]
    while flag[i+1] in ['r','n','nr','ns','nt','nz','Gn']:
        output=output+[word[i + 1]]
        i+=1
    return output
#废弃的程序
def group_left_n(word, flag, k):
    i=k
    output=[word[k]]
    while flag[i-1] in ['r','n','nr','ns','nt','nz','Gn']:
        output=[word[i-1]]+output
        i-=1
    return output

#将连续出现的名词合并为整体
def group_n(words,flags,group,new_flag): #连续名词合并
    delete=0
    l=len(words)
    for i in range(l-1):
        if flags[i-delete] in group and flags[i-delete+1] in group:
            words[i-delete]=''.join([words[i-delete],words[i-delete+1]])
            del words[i-delete+1]
            flags[i-delete]=new_flag
            del flags[i-delete+1]
            delete+=1
        if i == l - delete - 1: return

#寻找主语方法一
def get_subject1(word,flag,k): #往前找标点
    start=0
    for i in range(k-1, -1, -1):
        if flag[i] in ['w', 'x']:
            start=i+1
            break
    return ''.join(word[start:k])

#寻找主语方法二
def get_subject2(word,flag,k): #往前找名词串 或代词
    for i in range(k-1, -1, -1):
        if flag[i] in Gn or flag[i]=='r' : return word[i]
    return 'unknown'

#寻找主语方法三
def get_subject3(word,flag,k): #往前找标点，再往后找名词
    start=0
    for i in range(k-1, -1, -1):
        if flag[i] in ['w', 'x']:
            start=i+1
            break
    for i in range(start,k,1):
        if flag[i] in Gn: return word[i]
    return 'unknown'

#寻找言论方法一
def get_arguement1(words,flags,k): #说的同义字往后找，如有quote则直接调取quote
    if 'quote' in flags: return ''.join(words[i] for i in range(len(words)) if flags[i]=='quote')
    elif k==len(words)-1: return 'unknown'
    elif flags[k+1]=='x': return ''.join(words[i] for i in range(k+2,len(words),1))
    else: return ''.join(words[i] for i in range(k+1, len(words), 1))


#提取人物言论的主程序
def get_opinion(sentence):
    output=[]
    sentence_cut = list(pseg.cut(sentence))
    words, flags = [], []
    for m, n in sentence_cut:
        words.append(m)
        flags.append(n)
    replace_flag(words, flags, ['·'], 'x_n')    #将·词性改变为名词性，用以连接前后名词为整体，比如“阿尔伯特·爱因斯坦”
    replace_flag(words, flags, comb['s'], 'comb_s') #识别不可分割名词串起点
    replace_flag(words, flags, comb['e'], 'comb_e') #识别不可分割名词串终点
    replace_flag(words, flags, quote['s'], 'quote_s') #识别不可分割言论起点
    replace_flag(words, flags, quote['e'], 'quote_e') #识别不可分割言论终点
    comb_flag(words, flags, 'comb_s', 'comb_e', 'comb') #重新合并不可分割的名词串
    comb_flag(words, flags, 'quote_s', 'quote_e', 'quote') #重新合并不可分割的言论
    group_n(words, flags,Gn,'Gn') #重新合并连续名词串
    for k in range(len(words)):
        if words[k] in shuo: #判断是否在说的同义词中
            #print(sentence)
            #print('{}'.format(words))
            #print('{}'.format(flags))
            #print('op1 {} {}'.format(get_subject1(words, flags, k), words[k]))
            #print('op2 {} {} {}'.format(get_subject2(words, flags, k), words[k], get_arguement1(words,flags,k)))
            #print('op3 {} {}'.format(get_subject3(words, flags, k), words[k]))
            output.append([get_subject2(words, flags, k),words[k],get_arguement1(words,flags,k)])
    #print(output)
    #print(output.head(3))
    return output


Gn=['n','nr','ns','nt','nz','nrt','Gn','x_n','comb'] #凡是连续出现这类词性，合并为'Gn'名词串
comb={'s':['（','【','{','《','(','[','{','<'],'e':['）','】','}','》',')',']','}','>']} #不可分割的名词串的起点和终点
quote={'s':['‘','“','"'],'e':['’','”','"']} #不可分割的言论起点和终点

#程序执行
all_output=pd.DataFrame(columns=('Subject','Expression','Content'))
for i in get_sentence(0,df.shape[0]):
    for j in get_opinion(i):
        if j[0]==j[2]: continue
        print(j)
        all_output=all_output.append(pd.DataFrame({'Subject':[j[0]],'Expression':[j[1]],'Content':[j[2]]}),ignore_index=True)
#print(all_output)
all_output.to_csv('all_comments.csv', header=True, index=False, encoding='utf-8-sig')  # utf-8被认为是没有BOM，虽然功能正常，但excel读取出来仍是乱码
print('saved!')








