import requests
from bs4 import BeautifulSoup

base_url = "https://sigarra.up.pt/feup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id="
professors_url = set()

class CourseUnit:
    def __init__(self, name, code, acronym, main_professor, tp_professors, t_professors, ot_professors, pl_professors, p_professors, s_professors, language, objectives, results, working_method, pre_requirements, program, evaluation_type, hours, passing_requirements):
        self.name = name
        self.code = code
        self.acronym = acronym
        self.main_professor = main_professor
        self.tp_professors = tp_professors,
        self.t_professors = t_professors,
        self.ot_professors = ot_professors,
        self.pl_professors = pl_professors, 
        self.p_professors = pl_professors, 
        self.s_professors = s_professors,
        self.language = language
        self.objectives = objectives
        self.results = results
        self.working_method = working_method
        self.pre_requirements = pre_requirements
        self.program = program
        self.evaluation_type = evaluation_type
        self.hours = hours
        self.passing_requirements = passing_requirements

    def to_csv(self):
        return f'{self.name}; {self.code}; {self.acronym}; {self.main_professor}; {self.tp_professors}; {self.t_professors}; {self.ot_professors}; {self.pl_professors}; {self.p_professors}; {self.s_professors}; {self.language}; {self.objectives}; {self.results}; {self.working_method}; {self.pre_requirements}; {self.program}; {self.evaluation_type}; {self.hours}; {self.passing_requirements}'

def parse_unit_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    info = soup.find(id='conteudoinner')

    name = info.find_all('h1')[1].text.strip()
    code = info.find_all('td')[1].text.strip()
    acronym = info.find_all('td')[4].text.strip()

    language_header = soup.find('h3', string='Língua de trabalho')
    language = get_text(language_header)

    objectives_header = soup.find('h3', string='Objetivos')
    objectives = get_text(objectives_header)

    results_header = soup.find('h3', string='Resultados de aprendizagem e competências')

    results = get_text(results_header)

    working_method_header = soup.find('h3', string='Modo de trabalho')
    working_method = get_text(working_method_header)

    pre_requirements_header = soup.find('h3', string='Pré-requisitos (conhecimentos prévios) e co-requisitos (conhecimentos simultâneos)')
    if pre_requirements_header:
        pre_requirements = get_text(pre_requirements_header)
    else:
        pre_requirements = 'Não tem pré-requisitos'

    evaluation_type_header = soup.find('h3', string='Tipo de avaliação')
    evaluation_type = get_text(evaluation_type_header)

    hours_header = soup.find('h3', string='Componentes de Ocupação')
    hours = hours_header.find_next_sibling().find(class_="totais").find(class_="n").text.strip()

    passing_requirements_header = soup.find('h3', string='Obtenção de frequência')
    passing_requirements = get_text(passing_requirements_header)

    tp_class = get_professor(soup, 'Teórico-Práticas')
    if (tp_class != -1):
        tp_professors = tp_class[0][1:]
        professors_url.union(tp_class[1])
    else:
        tp_class = get_professor(soup, 'Teorico-Prática')
        if (tp_class != -1):
            tp_professors = tp_class[0][1:]
            professors_url.union(tp_class[1])
        else:
            tp_professors = ''

    print(tp_professors)

    t_class = get_professor(soup, 'Teóricas')
    if (t_class != -1):
        t_professors = t_class[0][1:]
        professors_url.union(t_class[1])
    else:
        t_class = get_professor(soup, 'Teórica')
        if (t_class != -1):
            t_professors = t_class[0][1:]
            professors_url.union(t_class[1])
        else:
            t_professors = ''

    ot_class = get_professor(soup, 'Orientação Tutorial')
    if (ot_class != -1):
        ot_professors = ot_class[0][1:]
        professors_url.union(ot_class[1])
    else:
        ot_professors = ''

    pl_class = get_professor(soup, 'Práticas Laboratoriais')
    if (pl_class != -1):
        pl_professors = pl_class[0][1:]
        professors_url.union(pl_class[1])
    else:
        pl_professors = '' 

    p_class = get_professor(soup, 'Práticas')
    if (p_class != -1):
        p_professors = p_class[0][1:]
        professors_url.union(p_class[1])
    else:
        p_professors = '' 

    s_class = get_professor(soup, 'Seminários')  
    if (s_class != -1):
        s_professors = s_class[0][1:]
        professors_url.union(s_class[1])
    else:
        s_professors = ''

    # get_program(info)

    return CourseUnit(name, code, acronym, '', tp_professors, t_professors, ot_professors, pl_professors, p_professors, s_professors, language, objectives, results, working_method, pre_requirements, '', evaluation_type, hours, passing_requirements)

def get_text(header):
    text = header.find_next_sibling(string=True).text.strip()
    if text != '':
        return text
    return header.find_next_sibling().text.strip()

def get_professor(soup, type):
    professors_header = soup.find('h3', string='Docência - Horas')
    professors_table = professors_header.find_next_sibling(class_='dados')
    class_types = professors_table.find_all(class_='k t')

    professors_codes = ''
    professors_urls = set()
    for class_type in class_types:
        if (class_type.get_text() == type):
            professors_list = class_type.find_next_siblings(class_='d')
            for professor in professors_list:
                professor_info = professor.find('td', class_='t')
                code = professor_info.find('a', href=True)['href'].split('=')[1]
                url = professor_info.find('a', href=True)['href']
                professors_codes += ',' + code
                professors_urls.add(url)
            return (professors_codes, professors_urls)
    return -1

def get_program(soup):
    program_header = soup.find('h3', string='Programa')
    program = program_header.find_next_sibling(text=True).strip()

    print(program_header)
    print(program_header.find_next_sibling().contents)
    print(program_header.find_parent().contents)

    program = ''

    next_line = program_header.find_next_sibling()
    while next_line and next_line.name != 'h3':
        print(next_line)
        if next_line.name is None:
            program += next_line.text.strip()
        next_line = next_line.find_next_sibling()

    print(program)

def main():
    # parse_unit_page("https://sigarra.up.pt/feup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=519377")
    # parse_unit_page("https://sigarra.up.pt/feup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=519369")
    # parse_unit_page("https://sigarra.up.pt/feup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=520306")
    # parse_unit_page("https://sigarra.up.pt/feup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=520223")
    # parse_unit_page("https://sigarra.up.pt/feup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=520324")
    # parse_unit_page("https://sigarra.up.pt/flup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=518101")

    urls = ["https://sigarra.up.pt/feup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=519377", "https://sigarra.up.pt/feup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=519369", "https://sigarra.up.pt/flup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=518101"]
    with open('../data/course_units.csv', 'w', encoding="utf-8") as my_file:
        my_file.write('name; code; acronym; main_professor; tp_professors; t_professors; ot_professors; pl_professors; p_professors; s_professors; language; objectives; results; working_method; pre_requirements; program; evaluation_type; hours; passing_requirements\n')
        for url in urls:
            course_unit = parse_unit_page(url)
            my_file.write(course_unit.to_csv() + '\n')

if __name__ == '__main__':
    main()