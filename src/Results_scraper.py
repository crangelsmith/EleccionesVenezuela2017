import time
import unicodedata
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def setup_selenium():
    # driver = webdriver.Firefox(executable_path='/Users/harvey/Downloads/geckodriver')
    driver = webdriver.Chrome(executable_path='/Users/harvey/Downloads/chromedriver')
    # driver = webdriver.Chrome(executable_path='/home/camila/Downloads/geckodriver')
    # driver = webdriver.Firefox(executable_path='/home/camila/Downloads/geckodriver')

    driver.implicitly_wait(30)

    return driver


def get_options(driver, level):
    time.sleep(0.5)

    wait = WebDriverWait(driver, 10)
    select_box = wait.until(ec.element_to_be_clickable((By.NAME, level)))

    options_list = [x for x in select_box.find_elements_by_tag_name("option")]
    time.sleep(0.5)
    return options_list


def string_fixer(s_object):
    return str(unicodedata.normalize('NFD', s_object).encode('ascii', 'ignore'))


def name_fixer(s_object):
    s_object = string_fixer(s_object)
    s_object = s_object.replace('.', '').replace(' ', '_')
    return s_object


def process_accordion(accordion, dict_mun):
    for i in xrange(0, len(accordion), 3):
        l_row = accordion[i:i + 3]

        n_votos = int(l_row[1])

        dict_mun[string_fixer(l_row[0])] = n_votos

    return dict_mun


def get_mesa_info(driver, estado, mun, par, centro, mesa, null_mesa):
    mesa.click()
    dict_mun = {'estado': string_fixer(estado.text), 'municipio': string_fixer(mun.text),
                'parroquia': string_fixer(par.text), 'centro': string_fixer(centro.text),
                'mesa': mesa.text}

    print("mesa: " + str(mesa.text))

    try:
        WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'accordion')))
    except:
        re_click(mesa, null_mesa)
        WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'accordion')))

    time.sleep(1)

    try:
        accordion = [i.text for i in driver.find_elements_by_tag_name('b')]
    except:
        re_click(mesa, null_mesa)
        accordion = [i.text for i in driver.find_elements_by_tag_name('b')]
    try:
        info = [x for x in driver.find_elements_by_tag_name('tr')]
    except:
        re_click(mesa, null_mesa)
        info = [x for x in driver.find_elements_by_tag_name('tr')]

    for row in info:
        try:
            l_row = row.text.rsplit(' ', 2)
            dict_mun[string_fixer(l_row[0])] = int(l_row[1])
        except:
            re_click(mesa, null_mesa)
            l_row = row.text.rsplit(' ', 2)
            dict_mun[string_fixer(l_row[0])] = int(l_row[1])
    try:
        dict_mun = process_accordion(accordion, dict_mun)
    except:
        re_click(mesa, null_mesa)
        accordion = [i.text for i in driver.find_elements_by_tag_name('b')]
        dict_mun = process_accordion(accordion, dict_mun)

    return dict_mun


def process_level(driver, level, element):
    print(element.text)

    element.click()

    options = get_options(driver, level)
    if level == 'cod_mesa':
        null_mesa = options.pop(0)
        return options, null_mesa
    else:
        print(options.pop(0).text)
        time.sleep(0.5)

    return options


def re_click(element, null_mesa):
    time.sleep(1.5)
    null_mesa.click()
    time.sleep(2)
    element.click()
    time.sleep(1.5)


def main():
    base_url = 'http://www.cne.gob.ve/resultados_regionales2017/'

    driver = setup_selenium()
    driver.get(base_url)

    options_estado = get_options(driver, 'cod_edo')
    options_estado.pop(0)

    # ('EDO. ANZOATEGUI',     0) DONE.
    # ('EDO. APURE',          1) DONE.
    # ('EDO. ARAGUA',         2) DONE.
    # ('EDO. BARINAS',        3) DONE.
    # ('EDO. BOLIVAR',        4) Done.
    # ('EDO. CARABOBO',       5) Done.
    # ('EDO. COJEDES',        6) Done.
    # ('EDO. FALCON',         7) Done.
    # ('EDO. GUARICO',        8) Done.
    # ('EDO. LARA',           9)
    # ('EDO. MERIDA',        10) Done.
    # ('EDO. MIRANDA',       11) Done.
    # ('EDO. MONAGAS',       12) Done.
    # ('EDO. NVA.ESPARTA',   13)
    # ('EDO. PORTUGUESA',    14)
    # ('EDO. SUCRE',         15)
    # ('EDO. TACHIRA',       16)
    # ('EDO. TRUJILLO',      17)
    # ('EDO. YARACUY',       18)
    # ('EDO. ZULIA',         19)
    # ('EDO. AMAZONAS',      20) Done.
    # ('EDO. DELTA AMACURO', 21) Done.
    # ('EDO. VARGAS',        22) Done.

    options_estado = [options_estado[9]]

    for estado in options_estado:
        options_mun = process_level(driver, 'cod_mun', estado)
        options_mun = options_mun[8:]
        # Change this line if the code crashes or gets booted and only a subset of the munic. have been done.

        for mun in options_mun:
            options_par = process_level(driver, 'cod_par', mun)
            # options_par = options_par[16:]
            # Change this line if the Mp. Doesn't complete.
            for par in options_par:
                options_centro = process_level(driver, 'cod_centro', par)
                l_dicts = []

                for centro in options_centro:
                    options_mesa, null_mesa = process_level(driver, 'cod_mesa', centro)

                    for mesa in options_mesa:

                        dict_mun = get_mesa_info(driver, estado, mun, par, centro, mesa, null_mesa)
                        l_dicts.append(dict_mun)

                df = pd.DataFrame(l_dicts)
                out_name = '../data/' + name_fixer(estado.text) + '-' + name_fixer(mun.text) + '-' + name_fixer(
                    par.text) + '.json'
                df.to_json(out_name, orient='records', lines=True)

    driver.close()


if __name__ == '__main__':
    main()
