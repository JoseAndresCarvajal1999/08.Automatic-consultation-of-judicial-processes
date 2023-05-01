from selenium import webdriver
from time import sleep
import os 
import re 
import urllib.request
import time 
import shutil 
from datetime import date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import requests


def download_file(download_url, filename,rute):
    response = requests.get(download_url)    
    #response = urllib.request.urlopen(download_url)    
    file = open(rute + '/'+ filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

def ConsultaPaginaweb(excel,rute_aux):
    today = date.today()
    rute = rute_aux + f'\{today}'
    
    if os.path.exists(rute):
        shutil.rmtree(rute)
        os.mkdir(rute)
    else: 
        os.mkdir(rute)
     
    chromeOptions = webdriver.ChromeOptions()    
    chromeOptions.add_argument('--disable-gpu')
    chromeOptions.add_argument('--disable-software-rasterizer')
    #chromeOptions.add_argument('--headless')
    #chromeOptions.add_argument('window-size=1920x1080')
    
    #chromeOptions.add_argument("--start-maximized")
    chromeOptions.add_argument("--start-fullscreen")
    chromeOptions.add_argument("--no-proxy-server")
    chromeOptions.add_argument("--proxy-server='direct://'")
    chromeOptions.add_argument("--proxy-bypass-list=*") 
    
    driver = webdriver.Chrome(executable_path='chromedriver', chrome_options = chromeOptions)
    page = os.environ['URL']
    driver.get(page)
    
    #rute = r'ScraperRadicados\{}'.format(name_folder)
    times = []
    Ciudades = []
    Juzgados = []
    pdfs_radicados = {}
    for radicado, juzgado, ciudad in zip(excel['RADICADO'],excel['JUZGADO'],excel['CIUDAD']):
        print(radicado)
        start = time.time()
        #Escoger la Ciudad 
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ddlCiudad")))
        if ciudad not in Ciudades:
            WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ddlCiudad")))
            driver.find_element_by_css_selector('#ddlCiudad').click()
            i = 1
            for x in driver.find_elements_by_xpath('//div//div//table//select//option'):
                if x.text == ciudad:
                    String_aux = '//*[@id="ddlCiudad"]/option[{}]'.format(i)
                    driver.find_element_by_xpath(String_aux).click()
                    break
                i = i+1 
            Ciudades = []
            Ciudades.append(ciudad)
            sleep(3)
         #Escoger el Juzgado 
        if juzgado not in Juzgados: 
            WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ddlEntidadEspecialidad")))
            driver.find_element_by_css_selector('#ddlEntidadEspecialidad').click()
            sleep(2)
            j = 1
            for y in driver.find_elements_by_xpath('//div//div//table//tbody//tr[3]//select//option'):
                if y.text == juzgado:
                    String_aux2 = '//*[@id="ddlEntidadEspecialidad"]/option[{}]'.format(j)
                    driver.find_element_by_xpath(String_aux2).click()
                    break
                j = j+1
            Juzgados = []
            Juzgados.append(juzgado)
        #print(Juzgados)
        #sleep(5)     
        driver.find_element_by_xpath('//div[2]//div[3]//table//tbody//tr[4]//td//div//table//tbody//tr[2]//td//div//input').clear()
        driver.find_element_by_xpath('//div[2]//div[3]//table//tbody//tr[4]//td//div//table//tbody//tr[2]//td//div//input').send_keys(radicado)
        sleep(1)
        button = driver.find_element_by_xpath('//div[2]//div[3]//table//tbody//tr[4]//td//div//table//tbody//tr[3]//td//input')
        driver.execute_script('arguments[0].removeAttribute("disabled");', button)
        driver.find_element_by_xpath('//div[2]//div[3]//table//tbody//tr[4]//td//div//table//tbody//tr[3]//td//input').click()
        #sleep(10)
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#btnGetPDF")))
        sleep(1)
        driver.find_element_by_css_selector('#btnGetPDF').click()
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#lblPDFFileStatus > b > a")))
        sleep(1)
        aux3 = driver.find_element_by_css_selector('#lblPDFFileStatus > b > a').get_attribute('href')
        aux3 = aux3.replace('\'','')
        string_aux1 = 'javascript:abrirDocumento\(([\s\S]*?)\)'
        match = re.search(string_aux1,aux3).group(1)
        download_file(match,radicado, rute)
        pdfs_radicados[radicado] = match
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#btnNuevaConsultaNum")))
        sleep(1)
        driver.find_element_by_css_selector('#btnNuevaConsultaNum').click()
        finish = time.time()
        times.append(start-finish)
    driver.quit()
    sleep(1)
    return pdfs_radicados

    
