from copy import Error
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time
import re

from models import Sumario

START_URL = "https://paco.ua.pt/aulas"
TURMAS_URL = "https://paco.ua.pt/disciplinas/suporte/lista_turmas_docente.asp"
GERE_TURMAS_URL = lambda tp_code: "https://paco.ua.pt/disciplinas/suporte/gere_turmas.asp?idturma=" + tp_code
SUMARIO_NOVO_URL = lambda tp_code: "https://paco.ua.pt/disciplinas/suporte/lancar_sumario.asp?idturma=" + tp_code
LISTA_SUMARIOS_URL = lambda tp_code: "https://paco.ua.pt/disciplinas/suporte/lista_sumarios.asp?idturma=" + tp_code

class PACO_UC():

    def __init__(self, uc_code, tp_code, username=None, password=None, dry_run=False):
        self.uc_code = str(uc_code)
        self.tp_code = str(tp_code)
        self.username = username if username else None   #empty username becomes None
        self.password = password if password else None   #empty password becomes None
        self.dry_run = dry_run

    def __enter__(self):
        self.driver = webdriver.Firefox()
        self._start_n_login(self.username, self.password)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._leave()

    def _start_n_login(self, username, password):
        self.driver.get(START_URL)

        usernameElement = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        if username is not None:
            usernameElement.send_keys(username)

        passwordElement = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        if password is not None:
            if passwordElement.get_attribute("type") == "password":
                passwordElement.send_keys(password)

        #Click the submit button
        if username is not None and password is not None:
            self.driver.find_element(By.ID, "btnLogin").click()

        #Wait util either this previous input automation 
        # or the user autenticates...
        WebDriverWait(self.driver, 3000).until(EC.url_contains("paco.ua.pt"))

        ##We are In!

        if False:
            #Wait for button "Lista de Turmas"
            aElement = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Lista Turmas"))
            )

            # Im not clicking because there are two "Lista Turmas" - feeling lazy on this.
            aElement.click()
        else:
            self.driver.get(TURMAS_URL)

        #Wait for a dummy element
        WebDriverWait(self.driver, 10).until( EC.presence_of_element_located((By.LINK_TEXT, "Visualizar o Horário Completo do Docente")))

        ##We are in the view that lists the UCs and turmas assigned to the current semester

        #import code;code.interact(local=locals())

        #Sacar os vários das várias UC, filtrar a que tem o tp_code e extrair da lista
        elems_with_link_sumarios_g = ( elem for elem in self.driver.find_elements(By.PARTIAL_LINK_TEXT, "Gerir Turma") if elem.get_attribute("href") )

        if self.tp_code:
            elems_with_link_sumarios_g = (elem for elem in elems_with_link_sumarios_g if self.tp_code in elem.get_attribute("href") )

        elems_with_link_sumarios = list(elems_with_link_sumarios_g)

        #Check for error or inconsistency
        if not self.tp_code or len(elems_with_link_sumarios)!=1 :

            print (" ########### Error ###########")
            if not self.tp_code:
                print ("TP Code is empty!")
            elif len(elems_with_link_sumarios) == 0:
                print ("TP Code ({}) not found:".format(self.tp_code))
            else:
                print ("Found TP Code ({}) in more than one Turma".format(self.tp_code))

            ##### List the UCs and codes found in PACO

            #Print the available Turmas
            #I'm piggybacking on the links to "Lista de Docentes na Turma" - they have tp_code and uc_code
            elems_g = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "Lista de Docentes na Turma")
            elems_g = ( elem for elem in elems_g if elem.get_attribute("href") )

            #Filter href
            #javascript:docentes(2021,1,28011,'Teórico-Prática',133344);

            turmas_str = [ re.match(r".*docentes(.*);", elem.get_attribute("href")).group(1) for elem in elems_g ]
            turmas_tup = list(map(eval, turmas_str)) #Tuples:(2021,1,28011,'Teórico-Prática',133344)
            

            #Getting the titles for each UC: Hoping for a generally static layout
            #The title sits on the only tr/td[@style]
            turmas_title = [ elem.text for elem in 
                self.driver.find_elements(By.XPATH, "//*[@class='table_cell_impar' or @class='table_cell_par']//td[@style]")
            ]

            #binding titles and codes...
            ucs_to_print = [ { "UC name": z_tup[1], "UC code": z_tup[0][2], "TP code": z_tup[0][4] } for z_tup in zip(turmas_tup, turmas_title) ]

            for uc in ucs_to_print:
                print (uc)

            quit()


        #Follow the link to "Gerir Sumários"
        elems_with_link_sumarios[0].click()

        #Wait on "Lançar um novo"
        lançarElement = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Lançar um novo"))
        )

        #lançarElement.click()

    def _leave(self):
        self.driver.quit()

    def adicionar_sumario(self, sumario:Sumario ):

        if sumario.hora == 1: d = '1 h 00 m'
        elif sumario.hora == 1.5: d = '1 h 30 m'
        elif sumario.hora == 2: d = '2 h 00 m'
        elif sumario.hora == 2.5: d = '2 h 30 m'
        elif sumario.hora == 3: d = '3 h 00 m'
        elif sumario.hora == 3.5: d = '3 h 30 m'
        elif sumario.hora == 4: d = '4 h 00 m'
        elif sumario.hora == 4.5: d = '4 h 30 m'
        elif sumario.hora == 5: d = '5 h 00 m'
        elif sumario.hora == 5.5: d = '5 h 30 m'
        elif sumario.hora == 6: d = '6 h 00 m'
        elif sumario.hora == 6.5: d = '6 h 30 m'
        elif sumario.hora == 7: d = '7 h 00 m'
        elif sumario.hora == 7.5: d = '7 h 30 m'
        else:
            raise Exception("Could not parse this class duration. ", sumario.hora)        

        self.adicionar_sumario_manual(
            sala=sumario.sala,
            sumario_txt=sumario.sumario,
            bibliografia_txt=sumario.bibliografia,
            duracao=d,
            data=sumario.date,
            attendance_mec_lst=sumario.presencas_mec
        )

    def contar_sumarios(self):
        get_sumarios_list_tr = lambda wd: wd.find_elements(By.XPATH, "//*[@class='table_cell_impar' or @class='table_cell_par']")

        self.driver.get(LISTA_SUMARIOS_URL(self.tp_code))
        footer = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table_footer"))
        )

        # To get the number of Sumários I could parse footer.text ("6 Sumários")
        # but I'll count the table rows
        return len(get_sumarios_list_tr(self.driver))

    def adicionar_sumario_manual(self, sala, data, sumario_txt, bibliografia_txt, duracao='2 h 00 m', attendance_mec_lst=[]):

        get_students_list_tr = lambda wd: wd.find_elements(By.XPATH, "//*[@class='table_cell_impar' or @class='table_cell_par']")

        get_students_size = lambda wd: int(wd.find_element(By.ID, "LotacaoAlunos").get_attribute("value"))

        def testStudentsLoaded(wd):
            num_alunos = get_students_size(wd)
            alunos = get_students_list_tr(wd)
            return len(alunos) == num_alunos

        def testStudentsLoaded(wd):
            wd.find_element(By.ID, "LotacaoAlunos")

        def write_in_iframe_richtext(wd, ifr_id, text):
            iframe_app = wd.find_element(By.ID, ifr_id)
            wd.switch_to.frame(iframe_app)
            content = WebDriverWait(wd, 10).until(EC.visibility_of_element_located((By.ID, "tinymce")))
            content.clear()
            content.send_keys(text)
            wd.switch_to.default_content()

        self.driver.get(SUMARIO_NOVO_URL(self.tp_code))

        #Wait for loading Sumario form page
        #Two page kinds may result:
        #   - Per student absent check (in UCs where attendance is mandatory)
        #   - Global number of students

        WebDriverWait(self.driver, 10).until( lambda wd: testStudentsLoaded(wd) or wd.find_elements(By.ID,"presencas") is not None )

        # Sala
        input_sala = self.driver.find_element(By.ID, "sala")
        input_sala.clear()
        input_sala.send_keys(sala)

        # Duração
        #'1 h 00 m'
        Select(self.driver.find_element(By.ID, "duracao")).select_by_visible_text(duracao)

        # Data
        input_data = self.driver.find_element(By.ID, "data")
        input_data.clear()
        input_data.send_keys(data)

        # Marcar faltas
        inputs_presencas_em_sala = self.driver.find_elements(By.ID, "presencas")
        if inputs_presencas_em_sala:
            #Just fill in the number of students in class
            inputs_presencas_em_sala[0].clear()
            inputs_presencas_em_sala[0].send_keys(len(attendance_mec_lst))
        else:
            #Check absence for each student
            for student_tr in get_students_list_tr(self.driver):
                checkbox = student_tr.find_element(By.TAG_NAME, "input")

                if checkbox.get_attribute("value").strip() not in attendance_mec_lst:
                    checkbox.click()

        if sumario_txt is not None:
            write_in_iframe_richtext(self.driver, "sumario_ifr", sumario_txt)

        if bibliografia_txt is not None:
            write_in_iframe_richtext(self.driver, "bibliografia_ifr", bibliografia_txt)

        if not self.dry_run:
            #Click submeter
            self.driver.find_element(By.ID, "submeter").click()
            #Wait jump to suporte/lista_sumarios.asp
            time.sleep(1)
        else:
            #Click go back
            # Wait jump to suporte/gere_turmas.asp
            self.driver.find_element(By.LINK_TEXT, "Cancelar, Voltar à Gestão da Turma").click()
            #self.driver.get(GERE_TURMAS_URL(self.tp_code))
            aElement = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Lista Turmas"))
            )
            time.sleep(1)
