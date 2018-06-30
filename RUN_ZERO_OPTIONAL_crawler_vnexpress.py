from bs4 import BeautifulSoup
import urllib2
import re
import codecs
import datetime
path='D:/IR2/dataset_crawl/'
url =  'https://vnexpress.net' #DO NOT CHANGE
#ONLY GET NEWS IN VNEXPRESS.NET/HOMEPAGE/HIGHLIGHT

print 'crawling, please wait'
def not_relative_uri(href):
	return re.compile('^https://').search(href) is  not  None
req = urllib2.Request(url)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page, 'html.parser')

new_feeds = soup.find('section', class_='featured container clearfix').\
    find_all('a', class_='', href=not_relative_uri)
count=0
for feed in new_feeds:
    url1 = feed.get('href')
    req1 = urllib2.Request(url1)
    page1 = urllib2.urlopen(req1)
    soup1 = BeautifulSoup(page1, 'html.parser')
    new_feeds1=soup1.find_all('p',class_="Normal")
    count+=1
    time=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    myfile = codecs.open (path+'VNE_'+time+str(count)+'.txt','w',"utf-16")
    myfile.write(soup1.find('h1').get_text())
    for feed1 in new_feeds1:
        myfile.write ('\n')
        myfile.write(feed1.get_text())    
    myfile.close()
print 'crawling completed'
        
        
        
        
        
        
        
        
        
        
        
        
        