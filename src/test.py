
b=[]
c=''
for k in range(len(a)):
    b.append(a[k][0]+' '+a[k][1]+' '+a[k][2]+' ')

for k in range(0,len(b)):
    c = c+ b[k]
   
# remove last space
d = c[0:len(c)-1]
