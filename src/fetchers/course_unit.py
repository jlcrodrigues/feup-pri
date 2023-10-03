import requests
from bs4 import BeautifulSoup

base_url = "https://sigarra.up.pt/feup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id="

class CourseUnit:
    def _init_(self, name, code, acronym, main_professor, lecturer, practical_professor, language, objectives, results, working_method, pre_requirements, program, evaluation_type, hours, passing_requirements):
        self.name = name
        self.code = code
        self.acronym = acronym
        self.main_professor = main_professor
        self.lecturer = lecturer
        self.practical_professor = practical_professor
        self.language = language
        self.objectives = objectives
        self.results = results
        self.working_method = working_method
        self.pre_requirements = pre_requirements
        self.program = program
        self.evaluation_type = evaluation_type
        self.hours = hours
        self.passing_requirements = passing_requirements

    def toCsv(self):
        return f"{self.name}; {self.code}; {self.acronym}; {self.main_professor}; {self.lecturer}; {self.practical_professor}; {self.language}; {self.objectives}; {self.results}; {self.working_method}; {self.pre_requirements}; {self.program}; {self.evaluation_type}; {self.hours}; {self.passing_requirements}"

def parse_unit_page(id):
    response = requests.get(base_url + id)
    soup = BeautifulSoup(response.text, "html.parser")

    # print(soup)

    info = soup.find(id='conteudoinner')

    name = info.find_all('h1')[1].text.strip()
    code = info.find_all('td')[1].text.strip()
    acronym = info.find_all('td')[4].text.strip()

    print(name + ', ' + code + ', ' + acronym)

    print('-------------')

    language_header = soup.find('h3', string='Língua de trabalho')
    language = get_text(language_header)

    print(language)

    print('-------------')

    objectives_header = soup.find('h3', string='Objetivos')
    objectives = get_section_text(objectives_header)

    print(objectives)

    print('-------------')

    results_header = soup.find('h3', string='Resultados de aprendizagem e competências')
    results = get_section_text(results_header)

    print(results)

    print('-------------')

    working_method_header = soup.find('h3', string='Modo de trabalho')
    working_method = get_text(working_method_header)

    print(working_method)

    print('-------------')

    pre_requirements_header = soup.find('h3', string='Pré-requisitos (conhecimentos prévios) e co-requisitos (conhecimentos simultâneos)')
    if pre_requirements_header:
        pre_requirements = get_section_text(pre_requirements_header)
    else:
        pre_requirements = 'Não tem pré-requisitos'

    print(pre_requirements)

    print('-------------')

    evaluation_type_header = soup.find('h3', string='Tipo de avaliação')
    evaluation_type = get_text(evaluation_type_header)

    print(evaluation_type)

    print('-------------')

    hours_header = soup.find('h3', string='Componentes de Ocupação')
    hours = hours_header.find_next_sibling().find(class_="totais").find(class_="n").text.strip()

    print(hours)

    print('-------------')

    passing_requirements_header = soup.find('h3', string='Obtenção de frequência')
    passing_requirements = get_section_text(passing_requirements_header)

    print(passing_requirements)

    print('-------------')

    # program_header = soup.find('h3', string='Programa')
    #program = program_header.find_next_sibling(text=True).strip()

    # print(program_header)
    # print(program_header.find_next_sibling().contents)

    # program = ''

    # next_line = program_header.find_next_sibling()
    # while next_line and next_line.name != 'h3':
    #     print(next_line)
    #     if next_line.name is None:
    #         program += next_line.text.strip()
    #     next_line = next_line.find_next_sibling()

    # print(program)

    # return CourseUnit(name, code, acronym, main_professor, lecturer, practical_professor, language, objectives, results, working_method, pre_requirements, program, evaluation_type, hours, passing_requirements)

def get_section_text(header):
    return header.find_next_sibling().text.strip()

def get_text(header):
    return header.find_next_sibling(string=True).text.strip()

def main():
    # parse_unit_page("519377")
    # parse_unit_page("519369")
    # parse_unit_page("520306")
    # parse_unit_page("520223")
    parse_unit_page("520324")

if __name__ == '__main__':
    main()