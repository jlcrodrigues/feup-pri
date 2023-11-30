import requests
from bs4 import BeautifulSoup
import time

baseUrl = "https://sigarra.up.pt/feup/pt/cur_geral.cur_view?pv_curso_id="
ids = ["22801","22802","22902","738","22803","22863","22823","22841","22882","22903"]

class Course:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        # self.plan = plan

    def toCsv(self):
        return f"{self.name}; {self.description}"


def check_text(result_html):
    result = ""
    if len(result_html) > 0:
        result += result_html[0].text.replace('\n', ' ').replace(';', ',')
    return result


def extract_child_info(element):
    global course_description
    course_description.append(element.text)

    next_element = element.find_next_sibling()
    if next_element is not None and next_element.name != 'h3':
        extract_child_info(next_element)

def parse_course_page(courseId):
    response = requests.get(baseUrl + courseId)
    soup = BeautifulSoup(response.text, "html.parser")
    
    title_html = soup.select('.ecra + h1')
    title = check_text(title_html)
    
    global course_description
    course_description = []
    for h3 in soup.find_all('h3'):
        extract_child_info(h3)
    
    description = ' '.join(course_description).replace('\t', '').replace('\n', '').replace('\r','').replace(";",",")
    return Course(title, description)


courses = []
course_description = []
def __main__():
    start = time.time()
    for courseId in ids:
        response = requests.get(baseUrl + courseId)
        if response.status_code == 200:
            courses.append(parse_course_page(courseId))
        else:
            print("Failed to fetch the web page. Status code:", response.status_code)
    end = time.time()
    print(f"Fetched {len(ids)} courses in {round(end - start, 1)}s.")

    with open('../data/courses.csv', 'w', encoding="utf-8") as my_file:
        my_file.write('title; description\n')
        for course in courses:
            my_file.write(course.toCsv() + '\n')


__main__()