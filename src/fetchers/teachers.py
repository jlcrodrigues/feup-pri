import requests
from bs4 import BeautifulSoup
import time

class Teacher:
    def __init__(self, name, personal_website, sigarra_website, abbreviation, status, code, email, phone, rank, personal_presentation, fields_of_interest):
        self.name = name
        self.personal_website = personal_website
        self.sigarra_website = sigarra_website
        self.abbreviation = abbreviation
        self.status = status
        self.code = code
        self.email = email
        self.phone = phone
        self.rank = rank
        self.personal_presentation = personal_presentation
        self.fields_of_interest = fields_of_interest

    def to_csv(self):
        return f"{self.name}; {self.personal_website}; {self.sigarra_website}; {self.abbreviation}; {self.status}; {self.code}; {self.email}; {self.phone}; {self.rank}; {self.personal_presentation}; {self.fields_of_interest}\n"
    
def parse_teacher_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Could not fetch teacher page")
    
    soup = BeautifulSoup(response.text, "html.parser")
    info_table = soup.find(class_="tabelasz")

    try:
        name = info_table.find_all("td")[1].find("b").text.strip()
    except:
        name = None

    try:
        personal_website = info_table.find_all("td")[1].find("a")['href'].strip()
    except:
        personal_website = None

    try:
        abbreviation = info_table.find_all("tr")[1].find_all("td")[1].find("b").text.strip()
    except:
        abbreviation = None

    try:
        status = info_table.find_all("tr")[2].find_all("td")[1].text.strip()
    except:
        status = None

    code = url.split("=")[1]

    try:
        email_parts = list(soup.find("td", string="Email Institucional:").find_next_sibling().find("a").stripped_strings)
        email = email_parts[0] + "@" + email_parts[1]
    except:
        email = None

    try:
        phone = soup.find("td", string="Telf.Alt.:").find_next_sibling().text.strip()
    except:
        phone = None

    try:
        rank = soup.find(class_="informacao-pessoal-funcoes").find_all("td")[2].text.strip()
    except:
        rank = None

    try:
        personal_presentation = soup.find(class_="informacao-pessoal-apresentacao").text.replace('\n', '').strip()
    except:
        personal_presentation = None
    
    try:
        fields_of_interest = soup.find(class_="informacao-pessoal-apresentacao").find("ol").text.strip()
    except:
        fields_of_interest = None

    return Teacher(name, personal_website, url, abbreviation, status, code, email, phone, rank, personal_presentation, fields_of_interest)


def get_teachers_csv(links):
    with open('../data/teachers.csv', 'w') as my_file:
        my_file.write("name; personal_website; sigarra_website; abbreviation; status; code; email; phone; rank; personal_presentation; fields_of_interest\n")
        for link in links:
            my_file.write(parse_teacher_page(link).to_csv())

def main():
    get_teachers_csv(['https://sigarra.up.pt/fcup/pt/FUNC_GERAL.FORMVIEW?p_codigo=202851'])

if __name__ == '__main__':
    main()
    