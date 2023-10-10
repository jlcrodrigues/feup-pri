import requests
from bs4 import BeautifulSoup
import time

YEAR = 2023

def check_text(result_html):
    result = ""
    if len(result_html) > 0:
        result += result_html[0].text.replace('\n', ' ').replace(';', ',')
    return result

'''https://sigarra.up.pt/feup/pt/ucurr_geral.pesquisa_ocorr_ucs_list?pv_num_pag=1&pv_ano_lectivo=2023&pv_curso_id=454'''

'''
Uses SIGARRA uc search to list all the courses related to a degree.
'''
def get_course_list(degree_id, faculty):
    courses = []
    baseUrl = f"https://sigarra.up.pt/{faculty}/pt/ucurr_geral.pesquisa_ocorr_ucs_list"
    page = 1

    while (True):
        url = f"{baseUrl}?pv_num_pag={page}&pv_ano_lectivo={YEAR}&pv_curso_id={degree_id}"
        response = requests.get(url)
        if response.status_code != 200: raise Exception(f"Error {response.status_code} fetching page")
        soup = BeautifulSoup(response.text, "html.parser")

        tablesHtml = soup.select('#conteudoinner table') 
        if (len(tablesHtml) != 1):
            break

        body = tablesHtml[0]
        rows = body.findChildren()
        rows.pop(0) # header

        for row in rows:
            aHtml = row.findChildren("a" , recursive=False)
            if len(aHtml) > 0: courses.append(f"https://sigarra.up.pt/{faculty}/pt/" + aHtml[0].get('href').strip())

        page += 1

    return courses

'''def __main__():
    degree_id = 454
    courses = get_course_list(degree_id, 'feup')

    with open('../data/course_list.txt', 'w') as my_file:
        for course in courses:
            my_file.write(course + '\n')

    print(f"Fetched {len(courses)} curricular units.")

__main__()'''