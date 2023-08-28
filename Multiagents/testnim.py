def normalize(dic):
    tt=sum(dic.values())
    for i in dic.keys():
        dic[i]=dic[i]/tt

dic={'a':0.2,'b':0.3}
normalize(dic)
print(dic)
