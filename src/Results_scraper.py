from selenium import webdriver
import time
import pandas as pd
import sys
import unicodedata

def setup_selenium(url):
    driver = webdriver.Firefox(executable_path='/Users/harvey/Downloads/geckodriver')
    #driver = webdriver.Chrome(executable_path='/Users/harvey/Downloads/chromedriver')
    driver.implicitly_wait(3)
    return driver


def get_options(driver, level, tries):
    time.sleep(4)
    if tries > 3:
        sys.exit("too many retries")
    select_box = driver.find_element_by_name(level)

    options_list = [x for x in select_box.find_elements_by_tag_name("option")]
    if len(options_list) == 1:
        tries += 1
        get_options(driver, level, tries)

    return options_list


def string_fixer(s_object):
    return str(unicodedata.normalize('NFD', s_object).encode('ascii', 'ignore'))


def name_fixed(s_object):
    s_object = string_fixer(s_object)
    s_object = s_object.replace('.', '').replace(' ', '_')
    return s_object


def process_accordion(accordion, dict_mun, tries):
    if tries < 5:
        for i in xrange(0, len(accordion), 3):
            l_row = accordion[i:i + 3]

            try:
                n_votos = float(l_row[1])
            except:
                time.sleep(3)
                process_accordion(accordion, dict_mun, tries)
                tries += 1

            dict_mun[string_fixer(l_row[0])] = n_votos

    return dict_mun


def get_mesa_info(driver, estado, mun, par, centro, mesa):
    try:
        mesa.click()
    except:
        time.sleep(6)
        mesa.click()

    time.sleep(1)

    dict_mun = {}
    dict_mun['estado'] = string_fixer(estado.text)
    dict_mun['municipio'] = string_fixer(mun.text)
    dict_mun['parroquia'] = string_fixer(par.text)
    dict_mun['centro'] = string_fixer(centro.text)
    dict_mun['mesa'] = mesa.text

    print("mesa: " + str(mesa.text))
    accordion = [i.text for i in driver.find_elements_by_tag_name('b')]

    if 'ADJUDICADO' in accordion:
        time.sleep(4)
        accordion = [i.text for i in driver.find_elements_by_tag_name('b')]

    info = [x for x in driver.find_elements_by_tag_name('tr')]
    for row in info:
        l_row = row.text.rsplit(' ', 2)
        dict_mun[string_fixer(l_row[0])] = float(l_row[1])

    dict_mun = process_accordion(accordion, dict_mun,0)

    return dict_mun


def process_level(driver, level, element):
    print(element.text)
    element.click()

    options = get_options(driver, level, 0)
    options.pop(0)

    return options


def main():
    base_url = 'http://www.cne.gob.ve/resultados_regionales2017/'

    driver = setup_selenium(base_url)
    driver.get(base_url)
    time.sleep(10)

    options_estado = get_options(driver, 'cod_edo', 0)
    options_estado.pop(0)

    options_estado = [options_estado[11]]

    for estado in options_estado:
        options_mun = process_level(driver, 'cod_mun', estado)
        options_mun = options_mun[9:] ## Change this line if the code crashes or gets booted and only a subset of the munic. have been done.
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

            out_name = '../data/'+name_fixed(estado.text) + '-' + name_fixed(mun.text) + '.json'
            df.to_json(out_name, orient='records', lines=True)

    driver.close()

if __name__ == '__main__':
    main()

