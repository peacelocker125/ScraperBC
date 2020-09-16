from django.shortcuts import render

import datetime
import selenium

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def index(request):

    class Artigo:
        def __init__(self, titulo, link, desc):
            self.t = titulo
            self.l = link
            self.d = desc


    DRIVER_PATH = "C:\\Users\\Family Member\\Downloads\\chromedriver_win32\\chromedriver"
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    date = str(datetime.date.today())
    date2 = str(datetime.date.today() - datetime.timedelta(days=3))
    date_sliced = date.split('-')
    date_sliced2 = date2.split('-')
    year = date_sliced[0]
    month = date_sliced[1]
    day = date_sliced[2]
    year2 = date_sliced2[0]
    month2 = date_sliced2[1]
    day2 = date_sliced2[2]
    url = f'https://www.bcb.gov.br/estabilidadefinanceira/buscanormas?dataInicioBusca={day2}%2F{month2}%2F{year2}&dataFimBusca={day}%2F{month}%2F{year}&tipoDocumento=Todos'
    art_todos = []
    driver.get(url)

    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "resultado-item")))
    finally:
        artigos = driver.find_elements_by_class_name('resultado-item')
        for artigo in artigos:
            title_class = artigo.find_element_by_tag_name('a')
            about_class = artigo.find_element_by_tag_name('span')
            title = title_class.text
            link = title_class.get_attribute('href')
            about = about_class.text
            art_novo = Artigo(title, link, about)
            art_todos.append(art_novo)
        driver.quit()
    
    return render(request, 'scraper/index.html', {
        'artigos': art_todos,
    })