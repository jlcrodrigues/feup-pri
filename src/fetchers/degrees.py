import requests
from bs4 import BeautifulSoup
import time

baseUrl = "https://www.up.pt"
bachelorsListUrl = "/portal/pt/estudar/licenciaturas-e-mestrados-integrados/oferta-formativa"
mastersListUrl = "/portal/pt/estudar/mestrados/oferta-formativa"

class Degree:
    def __init__(self, title, description, exits, url):
        self.title = title
        self.description = description
        self.url = url
        self.exits = exits

    def toCsv(self):
        return f"{self.title}; {self.description}; {self.exits}; {self.url}"
    
def check_text(result_html):
    result = ""
    if len(result_html) > 0:
        result += result_html[0].text.replace('\n', ' ').replace(';', ',')
    return result


def parse_degree_page(degree):
    response = requests.get(baseUrl + degree)
    soup = BeautifulSoup(response.text, "html.parser")

    title_html = soup.select('.course-description > div > h3')
    title = check_text(title_html)

    description_html = soup.select('.description p')
    description = check_text(description_html)

    exits_html = soup.select('.exits p')
    exits = check_text(exits_html)

    sig_link = soup.select('.course-description > div > a')[0].get('href').strip()
    return Degree(title, description, exits, sig_link)


'''Gets the list of links to all UP degrees'''
def get_degrees(soup):
    a = soup.select('#facultyList a')
    a = [x.get('href') for x in a]
    return a


degrees = []
def fetch_degree_list(url):
    start = time.time()
    response = requests.get(baseUrl + url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        link_degrees = get_degrees(soup)

        for degree in link_degrees:
            degrees.append(parse_degree_page(degree))
            break
    else:
        print("Failed to fetch the web page. Status code:", response.status_code)
    end = time.time()
    print(f"Fetched {len(degrees)} degrees in {round(end - start, 1)}s.")

def __main__():
    fetch_degree_list(bachelorsListUrl)
    fetch_degree_list(mastersListUrl)

    with open('../data/degrees.csv', 'w') as my_file:
        my_file.write('title; description; exits; url\n')
        for degree in degrees:
            my_file.write(degree.toCsv() + '\n')

__main__()