import os
import numpy as np
import codecs
import os.path

path='D:/IR2/dataset/' #folder where store documents
path1='D:/IR2/cache/'#folder where store cache

from collections import defaultdict
data=list() 
name=list()

symbols=codecs.open('symbols.txt',encoding='utf_8').read()

def read_data_test():
    global data,name
    symbols=codecs.open('symbols.txt',encoding='utf_8').read()
    for filename in os.listdir(path):
        myfile=codecs.open(path+filename,encoding='utf_16')
        data2=myfile.read().\
                   translate({ord(i):None for i in symbols}).\
                    lower().split()
        data.append(data2)
        name.append(filename)
        myfile.close() 
############################################
def create_cache():
    global path1,data,name
    stopwords=set(codecs.open('vietnamese-stopwords.txt',encoding='utf-8').read().split())
    total=set()
    for data2 in data:
        total.update(set(data2))
    total=total.difference(stopwords)  
    for term in total:
        for j in range(len(data)):
            tmp=0
            for i in data[j]:
                if i == term:
                    tmp+=1
            if tmp!=0:
                try:
                    myfile = open (path1+term+'.txt','a')
                except:
                    pass
                else:
                    tmp=int(np.log2(tmp))+1 
                    myfile.write (name[j])
                    myfile.write (' ')
                    myfile.write (str(tmp))
                    myfile.write ('\n')
                    myfile.close()  
####################################CODE RUN HERE
print 'indexing, please wait'
read_data_test()
create_cache()
print 'indexing completed'





