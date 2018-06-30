import os
import numpy as np
import codecs
import os.path

path='D:/IR2/dataset/' #folder where store documents
path1='D:/IR2/cache/'#folder where store cache

from collections import defaultdict
myText=''
symbols=codecs.open('symbols.txt',encoding='utf_8').read()

####################################\
def create_html():
    global path1,path,myText,symbols 
    name=list()
    for filename in os.listdir(path):
        name.append(filename) 
    doc= defaultdict(list)
    cosine=list() # calculate using Angles
    query=myText
    query=set(query.translate({ord(i):None for i in symbols}).lower().split())
    remove_set=set()
    for term in query:
        if os.path.isfile(path1+term+'.txt'):
            myfile = open (path1+term+'.txt','r')
            text=myfile.readlines()
            for line in text:
                ele=line.split()
                doc[ele[0],term]=int(ele[1])
            myfile.close()
        else:
            remove_set.add(term)
    for i in remove_set:
        query.remove(i)      
    for i in name:
        upper=0.0
        lower1=0.0
        lower2=0.0
        for term in query:
            if doc[i,term]!=[]:
                upper+=int(doc[i,term])
                lower1+= np.square(doc[i,term])
                lower2+= 1
            else:
                upper+=0
                lower1+=0
                lower2+=1
        lower1=np.sqrt(lower1)
        lower2=np.sqrt(lower2)
        lower1=lower1*lower2
        if lower1!=0:
            cosine.append(upper/lower1)
        else:
            cosine.append(0)
##############################################
    name2=name
    cosine,name2=zip(*sorted(zip(cosine,name2),reverse=True))
    all_mid=''
    upper_set=set()
    for term in query:
        upper_set.add(term[0].upper()+term[1:])
        upper_set.add(term)
    tmp=0
    for i in range(len(cosine)):
        if cosine[i]==0:
            break
        tmp+=1
#    print tmp
    
    for i in range(max(min(15,len(name)),tmp+1)):
        myfile=codecs.open(path+name2[i],encoding='utf_16')
        data2=myfile.readlines()
        myfile.close()
        header=data2[0]
        k=0
        while header in ['\n', '\r\n']:
            k+=1
            header=data2[k]
        myfile=codecs.open(path+name2[i],encoding='utf_16')
        data3=myfile.read()
        myfile.close()
        myfile=codecs.open('mid_code1.html',encoding='utf_8')
        mid=myfile.read()
        myfile.close()
        pre='...'
        for term in upper_set:
            x=data3.find(term)
            if x!=-1:
                pre+=data3[max(0,x-50):min(x+200,len(data3))]
                break
        
        for term in upper_set:
            pre=pre.replace(term,'<em>'+term+'</em>' )

        pre+='...'
        mid=mid.replace('my_header',header)
        mid=mid.replace('my_preview',pre)
        mid=mid.replace('my_location',path+name2[i])
        mid=mid.replace('my_adress','file:///'+path+name2[i])
        all_mid+=mid
    
    myfile=codecs.open('top_code.html',encoding='utf_8')
    full_html=myfile.read()
    myfile.close() 
    full_html+=all_mid
    myfile=codecs.open('bottom_code.html',encoding='utf_8')
    full_html+=myfile.read()
    myfile.close()  
    myfile = codecs.open ('my_html.html','w',"utf-8") 
    myfile.write (full_html)
    myfile.close()
#################################################

import sys
from PyQt5 import QtCore, QtGui, uic,QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import * 
qtCreatorFile = "UIsearch.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class PrettyWidget(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self) 
        self.setWindowTitle('Tim kiem') 
        self.myButton.clicked.connect(lambda:self.clickButton())

    def clickButton(self):
        global myText,create_html
        myText = self.myTextEdit.toPlainText()
        create_html()
        self.myWeb.setHtml(open('my_html.html').read())
###############################################
def main2():
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    w = PrettyWidget()
    w.show()
    app.exec_()
##########################################
#####################################CODE RUN HERE
main2()

