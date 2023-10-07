import requests
from bs4 import BeautifulSoup

base_url = "https://sigarra.up.pt/feup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id="

class CourseUnit:
    def __init__(self, name, code, credits, main_professor, tp_professors, t_professors, ot_professors, pl_professors, p_professors, s_professors, language, objectives, results, working_method, pre_requirements, program, evaluation_type, passing_requirements):
        self.name = name
        self.code = code
        self.credits = credits
        self.main_professor = main_professor
        self.tp_professors = tp_professors,
        self.t_professors = t_professors,
        self.ot_professors = ot_professors,
        self.pl_professors = pl_professors, 
        self.p_professors = p_professors, 
        self.s_professors = s_professors,
        self.language = language
        self.objectives = objectives
        self.results = results
        self.working_method = working_method
        self.pre_requirements = pre_requirements
        self.program = program
        self.evaluation_type = evaluation_type
        self.passing_requirements = passing_requirements

    def to_csv(self):
        return f'{self.name}; {self.code}; {self.credits}; {self.main_professor}; {self.tp_professors}; {self.t_professors}; {self.ot_professors}; {self.pl_professors}; {self.p_professors}; {self.s_professors}; {self.language}; {self.objectives}; {self.results}; {self.working_method}; {self.pre_requirements}; {self.program}; {self.evaluation_type}; {self.passing_requirements}'

def parse_unit_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    info = soup.find(id='conteudoinner')

    name = info.find_all('h1')[1].text.strip()
    code = info.find_all('td')[1].text.strip()

    print('NAME: ' + name)
    print('CODE: ' + code)

    print('-----------------------')

    credits_header = soup.find('h3', string='Ciclos de Estudo/Cursos')
    credits_table = credits_header.find_next_sibling(class_='dados')
    credits = credits_table.find('tr', class_='d').find_all('td', class_='n', rowspan='1')[1].text

    print('CREDITS: ' + credits)
    print('-----------------------')

    language_header = soup.find('h3', string='Língua de trabalho')
    language = get_text(language_header)

    print('LANGUAGE: ' + language)
    print('-----------------------')

    objectives_header = soup.find('h3', string='Objetivos')
    objectives = get_text(objectives_header)

    print('OBJECTIVES: ' + objectives)
    print('-----------------------')

    results_header = soup.find('h3', string='Resultados de aprendizagem e competências')
    results = get_text(results_header)

    print('RESULTS: ' + results)
    print('-----------------------')

    working_method_header = soup.find('h3', string='Modo de trabalho')
    working_method = get_text(working_method_header)

    print('WORKING METHODS: ' + working_method)
    print('-----------------------')

    pre_requirements_header = soup.find('h3', string='Pré-requisitos (conhecimentos prévios) e co-requisitos (conhecimentos simultâneos)')
    if pre_requirements_header:
        pre_requirements = get_text(pre_requirements_header)
    else:
        pre_requirements = ''

    print('PRE REQUIREMENTS: ' + pre_requirements)
    print('-----------------------')

    evaluation_type_header = soup.find('h3', string='Tipo de avaliação')
    evaluation_type = get_text(evaluation_type_header)

    print('EVAL TYPES: ' + evaluation_type)
    print('-----------------------')

    # hours_header = soup.find('h3', string='Componentes de Ocupação')
    # hours = hours_header.find_next_sibling().find(class_="totais").find(class_="n").text.strip()

    passing_requirements_header = soup.find('h3', string='Obtenção de frequência')
    passing_requirements = get_text(passing_requirements_header)

    print('PASSING REQUIREMENTS: ' + passing_requirements)
    print('-----------------------')

    main_professors = []
    main_professor_section = soup.find(class_='responsabilidades')
    main_professor_sections = main_professor_section.find(class_='dados').find_all('tr', class_='d')
    for section in main_professor_sections:
        main_professor = section.find('a')['href']
        main_professors.append(main_professor)

    tp_class = get_professor(soup, 'Teórico-Práticas')
    if (tp_class != -1):
        tp_professors = tp_class
    else:
        tp_class = get_professor(soup, 'Teorico-Prática')
        if (tp_class != -1):
            tp_professors = tp_class
        else:
            tp_professors = ''

    print('TP: ')
    print_list(tp_professors)
    print('-----------------------')

    t_class = get_professor(soup, 'Teóricas')
    if (t_class != -1):
        t_professors = t_class
    else:
        t_class = get_professor(soup, 'Teórica')
        if (t_class != -1):
            t_professors = t_class
        else:
            t_professors = ''

    print('T: ')
    print_list(t_professors)
    print('-----------------------')

    ot_class = get_professor(soup, 'Orientação Tutorial')
    if (ot_class != -1):
        ot_professors = ot_class
    else:
        ot_professors = ''

    print('OT: ') 
    print(ot_professors)
    print('-----------------------')

    pl_class = get_professor(soup, 'Práticas Laboratoriais')
    if (pl_class != -1):
        pl_professors = pl_class
    else:
        pl_professors = '' 

    print('PL: ')
    print(pl_professors)
    print('-----------------------')

    p_class = get_professor(soup, 'Práticas')
    if (p_class != -1):
        p_professors = p_class
    else:
        p_professors = '' 

    print('P: ')
    print(p_professors)
    print('-----------------------')

    s_class = get_professor(soup, 'Seminários')  
    if (s_class != -1):
        s_professors = s_class
    else:
        s_professors = ''

    print('S: ')
    print(s_professors)
    print('-----------------------')

    program = get_program(info)

    print('PROGRAM: ' + program)

    return CourseUnit(name, code, credits, main_professors, tp_professors, t_professors, ot_professors, pl_professors, p_professors, s_professors, language, objectives, results, working_method, pre_requirements, program, evaluation_type, passing_requirements)

def print_list(list):
    for x in range(len(list)):  
        print (list[x])

def get_text(header):
    text = header.find_next_sibling(string=True).text.strip()
    if text != '':
        return text
    return header.find_next_sibling().text.strip()

def get_professor(soup, type):
    professors_header = soup.find('h3', string='Docência - Horas')
    professors_table = professors_header.find_next_sibling(class_='dados')
    class_types = professors_table.find_all(class_='k t')

    professors_urls = []
    for class_type in class_types:
        if (class_type.get_text() == type):
            professors_list = class_type.find_next_siblings(class_='d')
            for professor in professors_list:
                professor_info = professor.find('td', class_='t')
                url = professor_info.find('a', href=True)['href']
                professors_urls.append(url)
            return professors_urls
    return -1

def get_program(soup):
    sections = soup.find_all('h3', string='Programa')

    text = ''
    for section in sections:
        if(section.text.strip() == 'Programa'):
            siblings = section.find_next_siblings()
            for sibling in siblings:
                if(sibling.name == 'h3'):
                    return text
                text += sibling.text.strip() + '\n'
    return text

def main():
    # parse_unit_page("https://sigarra.up.pt/feup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=519377")
    # parse_unit_page("https://sigarra.up.pt/feup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=519369")
    # parse_unit_page("https://sigarra.up.pt/feup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=520306")
    # parse_unit_page("https://sigarra.up.pt/feup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=520223")
    # parse_unit_page("https://sigarra.up.pt/feup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=520324")
    # parse_unit_page("https://sigarra.up.pt/flup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=518101")
    # https://sigarra.up.pt/icbas/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=520513

    urls = ["https://sigarra.up.pt/feup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=520223"]
    with open('../data/course_units.csv', 'w', encoding="utf-8") as my_file:
        my_file.write('name; code; acronym; main_professor; tp_professors; t_professors; ot_professors; pl_professors; p_professors; s_professors; language; objectives; results; working_method; pre_requirements; program; evaluation_type; hours; passing_requirements\n')
        for url in urls:
            course_unit = parse_unit_page(url)
            # my_file.write(course_unit.to_csv() + '\n')

if __name__ == '__main__':
    main()