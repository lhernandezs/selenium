from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys 

import os.path
import time
import json

# Configuración de las opciones de Chrome
options = Options()
appState = {
    "recentDestinations": [
        {
            "id"        : "Save as PDF",
            "origin"    : "local",
            "account"   : ""
        }
    ],
    "selectedDestination": "Save as PDF",
    "version": 2
}
prefs = {
    'printing.print_preview_sticky_settings.appState'   : json.dumps(appState),
    'savefile.default_directory'                        : 'C:\pdfs'
}

options.add_experimental_option('prefs', prefs)
options.add_argument('--kiosk-printing')
options.add_argument('start-maximized')

# Iniciar el driver
driver = webdriver.Chrome(options=options)

# Abrir la URL
url = "https://sena.territorio.la/indexLoginDashboard.php"
driver.get(url)

time.sleep(2)

# Loggearse con el usuario autorizado
usuario     = driver.find_element(By.XPATH, '//*[@id="MyUserName"]')
password    = driver.find_element(By.XPATH, '//*[@id="MyPassWord"]')
usuario.send_keys('jpulgarin@sena.edu.co')
password.send_keys('Jcamilo.210657')
clicaBoton  = driver.find_element(By.XPATH, '//*[@id="LogIn"]')
clicaBoton.click()

time.sleep(2)

paginas =driver.find_elements(By.XPATH,'//*[@id="pagination"]/div/ul/li')

for pagina in range(1, len(paginas) - 3):

    fichas = driver.find_elements(By.XPATH,'//*[@id="catalogo-main-content"]/li')

    for i in range(1, len(fichas) + 1):

        botonMostrarFicha = driver.find_element(By.XPATH, '//*[@id="catalogo-main-content"]/li['+str(i)+']/div/div[2]/span[1]/div/a')
        botonMostrarFicha.click()
        nombreArchivo= (driver.find_element(By.XPATH,'//*[@id="groupTitle tt"]').text).replace("\n", " ")

        ban = True
        contador = 40   
        while ban and contador > 0 :
            try:
                time.sleep(2)
                driver.execute_script('javascript:verMas()')
            except: 
                ban = False
            contador -= 1

        with open(os.path.join('', nombreArchivo + '.html'), "a", encoding="utf-8") as f:
            f.write(driver.page_source)

        # Ejecutar el script de impresión
        driver.execute_script('window.print();')

        print('ficha ', nombreArchivo)
        driver.get('https://sena.territorio.la/init.php')
        cadena= "goPage(" + str(pagina) + ")"
        driver.execute_script(cadena)
        time.sleep(2)
    
    print("pagina que recorro:" , pagina)
    driver.execute_script("goPage('+1')")
    time.sleep(4)



time.sleep(5)

# Cerrar el driver
driver.quit()

print("-----FIN-----")