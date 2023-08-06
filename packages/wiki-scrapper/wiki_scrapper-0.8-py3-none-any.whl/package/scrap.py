from bs4 import BeautifulSoup
import requests
from .section import Section

def scrapWikiPage (topic):
    ''' Extracts web page page and converts to beautiful soup format , if an error occurs return -1'''
    try:
        page = requests.get("https://en.wikipedia.org/wiki/" + topic)
    except:
        return -1 
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
        content = soup.select('div.mw-parser-output')[0]
        wikisection = organise(topic,content)
        return wikisection
    else:
        return -1

def organise(topic,soup):
    ''' Organises all text into section objects .Each subsection is determined by heading type at the beginning'''
    WikiSection = Section(topic,"",1)
    CurrentSection = WikiSection
    for elem in soup:

        if elem.name == "p" and elem.text != None:
            CurrentSection.addText(elem.text)

        elif elem.name != None and elem.name[0] == 'h':
            headinglevel = int(elem.name[1])

            if headinglevel > CurrentSection.headinglevel:
                NewSection = Section(elem.find('span').text,CurrentSection,headinglevel)
                CurrentSection.addSection(NewSection)
                CurrentSection = NewSection
            
            elif headinglevel <= CurrentSection.headinglevel:
                while CurrentSection.headinglevel != headinglevel :
                    CurrentSection = CurrentSection.parent
                NewSection = Section(elem.find('span').text,CurrentSection.parent,CurrentSection.headinglevel)
                CurrentSection.parent.addSection(NewSection)
                CurrentSection = NewSection 

    return WikiSection


