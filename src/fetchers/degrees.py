import requests
from bs4 import BeautifulSoup
import time


class Degree:
    def __init__(self, title, description, exits, url, course_type, duration):
        self.title = title
        self.description = description
        self.url = url
        self.exits = exits
        self.course_type = course_type
        self.duration = duration

    def toCsv(self):
        return f"{self.title}; {self.description}; {self.exits}; {self.url}; {self.course_type}; {self.duration}"


def check_text(result_html):
    result = ""
    if len(result_html) > 0:
        result += result_html[0].text.replace("\n", " ").replace(";", ",")
    return result


def parse_degree_page(degree, baseUrl):
    response = requests.get(baseUrl + degree)
    soup = BeautifulSoup(response.text, "html.parser")

    title_html = soup.select(".course-description > div > h3")
    title = check_text(title_html)

    description_html = soup.select(".description p")
    description = check_text(description_html)

    exits_html = soup.select(".exits p")
    exits = check_text(exits_html)

    course_type= soup.find(string="Tipo de Curso").find_next('dd').text
    duration= soup.find(string="Duração").find_next('dd').text

    sig_link = soup.select(".course-description > div > a")[0].get("href").strip()
    return Degree(title, description, exits, sig_link, course_type, duration)


"""Gets the list of links to all UP degrees"""
def get_degrees(soup):
    a = soup.select("#facultyList a")
    a = [x.get("href") for x in a]
    return a


def fetch_degree_list(url, baseUrl):
    degrees = []
    start = time.time()
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        link_degrees = get_degrees(soup)

        for degree in link_degrees:
            degrees.append(parse_degree_page(degree, baseUrl))
    else:
        print("Failed to fetch the web page. Status code:", response.status_code)
    end = time.time()
    print(f"Fetched {len(degrees)} degrees in {round(end - start, 1)}s.")
    return degrees


def fetch_degrees(urls, baseUrl):
    degrees = []
    for url in urls:
        try:
            degrees += fetch_degree_list(url, baseUrl)
        except Exception as e:
            print("Failed to fetch the web page: ", e)
            continue

    return degrees