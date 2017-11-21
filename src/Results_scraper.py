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
    time.sleep(2)
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


def get_mesa_info(driver, estado, mun, par, centro, mesa):
    try:
        mesa.click()
    except:
        time.sleep(6)
        mesa.click()

    time.sleep(1)

    dict_estado = {}
    dict_estado['estado'] = string_fixer(estado.text)
    dict_estado['municipio'] = string_fixer(mun.text)
    dict_estado['parroquia'] = string_fixer(par.text)
    dict_estado['centro'] = string_fixer(centro.text)
    dict_estado['mesa'] = mesa.text

    print("mesa: " + str(mesa.text))
    accordion = [i.text for i in driver.find_elements_by_tag_name('b')]

    if 'ADJUDICADO' in accordion:
        time.sleep(4)
        accordion = [i.text for i in driver.find_elements_by_tag_name('b')]

    info = [x for x in driver.find_elements_by_tag_name('tr')]
    for row in info:
        l_row = row.text.rsplit(' ', 2)
        dict_estado[string_fixer(l_row[0])] = float(l_row[1])

    for i in xrange(0, len(accordion), 3):
        l_row = accordion[i:i + 3]
        dict_estado[string_fixer(l_row[0])] = float(l_row[1])

    return dict_estado


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

    options_estado = [options_estado[20]]

    for estado in options_estado:
        options_mun = process_level(driver, 'cod_mun', estado)

        for mun in options_mun:
            l_dicts = []
            options_par = process_level(driver, 'cod_par', mun)

            for par in options_par:
                options_centro = process_level(driver, 'cod_centro', par)

                for centro in options_centro:
                    options_mesa = process_level(driver, 'cod_mesa', centro)

                    for mesa in options_mesa:
                        dict_estado = get_mesa_info(driver, estado, mun, par, centro, mesa)

                        l_dicts.append(dict_estado)

            df = pd.DataFrame(l_dicts)

            out_name = name_fixed(estado.text) + '-' + name_fixed(mun.text) + '.json'
            df.to_json(out_name, orient='records', lines=True)

    driver.close()

if __name__ == '__main__':
    main()

