simple_grammar = """
sentence => noun_phrase verb_phrase
noun_phrase => Article Adj* noun
Adj* => null | Adj Adj*
verb_phrase => verb noun_phrase
Article => 一个 | 这个
noun => 女人 |  篮球 | 桌子 | 小猫
verb => 看着 |  坐在 | 听着 | 看见 
Adj => 蓝色的 |  好看的 | 小小的
"""
#define list needed
header=['']*len(simple_grammar.splitlines())
value=['']*len(simple_grammar.splitlines())
words=[['']*1 for x in range(len(simple_grammar.splitlines()))]
result=[]

def split():  #to split the grammar
	i=0
	for line in simple_grammar.splitlines():
		if line.count('=>')>0:
			header[i]=line.split('=>')[0].strip()
			words[i]=line.split('=>')[1].split('|')
		for j in range(len(words[i])):
			words[i][j]=words[i][j].lstrip()
			words[i][j]=words[i][j].rstrip()
		#print(header[i],words[i])
		i+=1
	#print('---splitted---')

def rand(): #to randomize the options
	import random
	for i in range(len(simple_grammar.splitlines())):
		value[i]=words[i][random.randint(0,len(words[i])-1)].split(' ')
		#print(header[i],'=',value[i])
	#print('---randomized---')

def breakdown(result): #to breakdown the components
	for m in range(len(result)):
		for n in range(len(simple_grammar.splitlines())):
			if result[m]==header[n]:
				del result[m]
				for v in range(len(value[n])):
					result.insert(m+v,value[n][v])
				m=m+v
	#print(result)
	#print('---brokendown---')
	return result

def generator(input):
	print('Grammar Input is:')
	print(simple_grammar)
	split()
	rand()
	for i in range(len(simple_grammar.splitlines())):
		if input==header[i]:
			result=value[i]	
	exhaust=False
	cycle=0
	while exhaust!=True: #this is a repeat to exhaust components
		rand()
		breakdown(result)
		#print(cycle,' ',result)
		exhaust=True
		for m in range(len(result)):
			for n in range(len(simple_grammar.splitlines())):
				if result[m]==header[n]:
					#print(result[m],' is not exhausted')
					exhaust=False
					cycle+=1
					break
	i=0
	tail=False
	while tail!=True: #to remove null and repeated adj
		if i>0 and (result[i]==result[i-1] or result[i]=='null'):
			del result[i]
			i+=-1
		tail=i==len(result)-1
		i+=1
			
	print('Random Output is:')
	print(''.join(result))

generator('sentence')