x=int(input('input is '))

def stepcount(x):
	r=int(pow(x-1,0.5)/2+0.5)
	c=x-pow(2*r-1,2)
	n=abs(c%(2*r)-r)+r
	return n

print('steps needed back to square 1 is ',stepcount(x))