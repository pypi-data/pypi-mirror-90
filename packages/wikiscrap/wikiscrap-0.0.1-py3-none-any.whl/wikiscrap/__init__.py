import requests
from bs4 import BeautifulSoup
import re

inp = input('Enter name of Wikipedia page: ')
url = 'https://en.wikipedia.org/wiki/'+inp
r = requests.get(url)
htmlcontent = r.content
soup = BeautifulSoup(htmlcontent, 'html.parser')

#Finding Section from Wikipedia page (Check h2>span>text)
sections = []
subsections = []
h2s = soup.find_all('h2')
for h2 in h2s:
    if(h2.find('span')!=None):
        sections.append(h2.find('span').get_text())
    else:
        pass
print('Sections available are:')
print(sections)

#Searching for a section on a page and retrieveing its text and list of subsections
html = ''
key = input('Enter the section you are looking for: ')
for section in sections:
    if(section == key):
        for h2 in h2s:
            if(h2.find('span')!=None):
                if(h2.find('span').get_text()==section):
                    #print(h2.find_next_siblings('p'))
                    for tag in h2.next_siblings:
                        if tag.name == "h3":
                            break
                        else:
                            html += str(tag)
                else:
                    pass
section_html = BeautifulSoup(html,'html.parser')
print(section_html.get_text())

#Printing List Of Subsections
for item in soup.select("li.toclevel-1"):
    if(item.find_all_next(string=True)[2]==key):
        for i in item.find_next('ul').select('li'):
            subsections.append(i.find_all('span')[1].get_text())
print('Sub-sections available are:')
print(subsections)
            
#Printing Text from Selected Subsection
htmlsub = ''
keysub = input('Enter the sub-section you are looking for: ')
h3s = soup.find_all('h3')
for section in subsections:
    if(section == keysub):
        for h3 in h3s:
            if(h3.find('span')!=None):
                if(h3.find('span').get_text()==section):
                    for tag in h3.next_siblings:
                        if tag.name == "h3":
                            break
                        else:
                            htmlsub += str(tag)
                else:
                    pass
section_html_sub = BeautifulSoup(htmlsub,'html.parser')
print(section_html_sub.get_text())