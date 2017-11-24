from selenium import webdriver
import time
import pandas as pd
import sys
import unicodedata
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


def setup_selenium():
    driver = webdriver.Firefox(executable_path='/Users/harvey/Downloads/geckodriver')
    #driver = webdriver.Chrome(executable_path='/Users/harvey/Downloads/chromedriver')
    #driver = webdriver.Chrome(executable_path='/home/camila/Downloads/geckodriver')
    #driver = webdriver.Firefox(executable_path='/home/camila/Downloads/geckodriver')

    driver.implicitly_wait(5)

    return driver


def get_options(driver, level):
    time.sleep(0.5)

    wait = WebDriverWait(driver, 10)
    select_box = wait.until(ec.element_to_be_clickable((By.NAME, level)))

    options_list = [x for x in select_box.find_elements_by_tag_name("option")]

    return options_list


def string_fixer(s_object):
    return str(unicodedata.normalize('NFD', s_object).encode('ascii', 'ignore'))


def name_fixer(s_object):
    s_object = string_fixer(s_object)
    s_object = s_object.replace('.', '').replace(' ', '_')
    return s_object


def process_accordion(accordion, dict_mun):
    # time.sleep(1)
    for i in xrange(0, len(accordion), 3):
        l_row = accordion[i:i + 3]

        n_votos = float(l_row[1])

        dict_mun[string_fixer(l_row[0])] = n_votos

    return dict_mun


def get_mesa_info(driver, estado, mun, par, centro, mesa):
    wait = WebDriverWait(driver, 30)
    # time.sleep(1)
    mesa.click()

    dict_mun = {'estado': string_fixer(estado.text), 'municipio': string_fixer(mun.text),
                'parroquia': string_fixer(par.text), 'centro': string_fixer(centro.text),
                'mesa': mesa.text}

    print("mesa: " + str(mesa.text))
    # wait.until(ec.invisibility_of_element_located((By.CSS_SELECTOR, '#accordion > div:nth-child(2) > div.panel-heading.hoverDiv > h4 > a > div > div.col-sm-8.text-left > b > strong')))
    wait.until(ec.visibility_of_element_located((By.ID, 'accordion')))
    time.sleep(1)
    # wait.until(ec.visibility_of_element_located((By.TAG_NAME, 'tr')))

    accordion = [i.text for i in driver.find_elements_by_tag_name('b')]
    info = [x for x in driver.find_elements_by_tag_name('tr')]

    for row in info:
        l_row = row.text.rsplit(' ', 2)
        dict_mun[string_fixer(l_row[0])] = float(l_row[1])

    dict_mun = process_accordion(accordion, dict_mun)

    return dict_mun


def process_level(driver, level, element):
    print(element.text)

    element.click()

    options = get_options(driver, level)
    options.pop(0)

    return options


def main():
    base_url = 'http://www.cne.gob.ve/resultados_regionales2017/'

    driver = setup_selenium()
    driver.get(base_url)

    options_estado = get_options(driver, 'cod_edo')
    options_estado.pop(0)

    # ('EDO. ANZOATEGUI',     0)
    # ('EDO. APURE',          1)
    # ('EDO. ARAGUA',         2)
    # ('EDO. BARINAS',        3)
    # ('EDO. BOLIVAR',        4)
    # ('EDO. CARABOBO',       5)
    # ('EDO. COJEDES',        6)
    # ('EDO. FALCON',         7)
    # ('EDO. GUARICO',        8)
    # ('EDO. LARA',           9)
    # ('EDO. MERIDA',        10)
    # ('EDO. MIRANDA',       11)
    # ('EDO. MONAGAS',       12)
    # ('EDO. NVA.ESPARTA',   13)
    # ('EDO. PORTUGUESA',    14)
    # ('EDO. SUCRE',         15)
    # ('EDO. TACHIRA',       16)
    # ('EDO. TRUJILLO',      17)
    # ('EDO. YARACUY',       18)
    # ('EDO. ZULIA',         19)
    # ('EDO. AMAZONAS',      20)
    # ('EDO. DELTA AMACURO', 21)
    # ('EDO. VARGAS',        22)
    
    options_estado = [options_estado[11]]

    for estado in options_estado:
        options_mun = process_level(driver, 'cod_mun', estado)
        # options_mun = options_mun[9:]
        # Change this line if the code crashes or gets booted and only a subset of the munic. have been done.
        for mun in options_mun:
            l_dicts = []
            options_par = process_level(driver, 'cod_par', mun)

            for par in options_par:
                options_centro = process_level(driver, 'cod_centro', par)

                for centro in options_centro:
                    options_mesa = process_level(driver, 'cod_mesa', centro)

                    for mesa in options_mesa:
                        dict_mun = get_mesa_info(driver, estado, mun, par, centro, mesa)

                        l_dicts.append(dict_mun)

            df = pd.DataFrame(l_dicts)

            out_name = '../data/' + name_fixer(estado.text) + '-' + name_fixer(mun.text) + '.json'
            df.to_json(out_name, orient='records', lines=True)

    driver.close()


if __name__ == '__main__':
    main()
