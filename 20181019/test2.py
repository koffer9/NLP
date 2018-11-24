# encoding=utf-8
import jieba


example='你们今天/明天/后天会不会到大学/中学/小学里去打球/滑冰/骑车呀？'
print('请输入一段包含不同选项的句子，各选项直接用分隔符/分开')
print('例句：',example)
print('或者直接回车：')
text=input()
if text=="":
    text=example
print('输入是:')
print(text) #把输入返回一次
seg_list = jieba.lcut(text)  # 默认是精确模式
l=len(seg_list) #拆词列表长度
n=0
ex_location=[]
ex_options=[]
seg_stat=[]

#识别拆词列表各部分的属性，判断出可选项起始位置和选项数量
for i in range(0,l):
    if ((i==0 and seg_list[1]=='/') or (i>0 and i<l-1 and seg_list[i-1]!='/' and seg_list[i+1]=='/')) and seg_list[i]!='/':
        ex_location.append(i)
        n+=1
        seg_stat.append('op_head') #可选项第一选项
    elif (i>0 and i<l-1 and seg_list[i-1]=='/' and seg_list[i+1]=='/') and seg_list[i]!='/':
        n+=1
        seg_stat.append('op_mid') #可选项中间选项
    elif ((i==l-1 and seg_list[i-1]=='/') or (i>0 and i<l-1 and seg_list[i-1]=='/' and seg_list[i+1]!='/')) and seg_list[i]!='/':
        n+=1
        ex_options.append(n)
        n=0
        seg_stat.append('op_tail') #可选项末尾选项
    elif ((i==0 and seg_list[1]!='/') or (i==l-1 and seg_list[i-1]!='/') or (i>0 and i<l-1 and seg_list[i-1]!='/' and seg_list[i+1]!='/')) and seg_list[i]!='/':
        n=0
        seg_stat.append('fixed') #固定部分
    else:
        seg_stat.append('separation') #分隔符
#print('found ex_location: ',ex_location) #识别可选项的起始位置
#print('found ex_options: ',ex_options) 识别可选项的选项数量
#print(seg_stat)拆解后各词组性质

#识别输出数量
total=1
for ex_option in ex_options:
    total=total*ex_option

#选择性输出部分
print('输出是：')
for i in range(0,total):
    ex_accumulate=[]
    ex_choice=[]
    for j in range(0,len(ex_options)): #计算出每个选项的累积乘数，根据累计乘数取余算出所有选项组合
        ex_choice.append(0)
        if j==0:
            ex_accumulate.append(ex_options[j])
            ex_choice[j]=i%ex_options[j]
        else:
            ex_accumulate.append(ex_accumulate[j-1]*ex_options[j])
            ex_choice[j]=int(i/ex_accumulate[j-1])%ex_options[j]
    #print(i,' ',ex_choice[0],' ',ex_choice[1],' ',ex_choice[2])
    sentence=[]
    for m in range(0,l): #从最初的拆词列表内选择输出需要的词组，组合输出
        if seg_stat[m]=='fixed':
            sentence.append(seg_list[m])
        else:
            for n in range(0,len(ex_options)):
                if m==ex_location[n]:
                    sentence.append(seg_list[ex_location[n]+2*ex_choice[n]])
    print(i+1,'：',"".join(sentence))




