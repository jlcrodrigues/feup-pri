import spacy
import wikipediaapi

wiki = wikipediaapi.Wikipedia('Daniel Rodrigues', 'pt')
page = wiki.page('Engenharia Informática')
if page.exists():
    print(page.fullurl)
    print('\n')
        
