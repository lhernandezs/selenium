from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys 

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

# Iniciar el driver
driver = webdriver.Chrome(options=options)

# Abrir la URL
url = "https://sena.territorio.la/indexLoginDashboard.php"
driver.get(url)

time.sleep(2)

usuario     = driver.find_element(By.XPATH, '//*[@id="MyUserName"]')
password    = driver.find_element(By.XPATH, '//*[@id="MyPassWord"]')
usuario.send_keys('jpulgarin@sena.edu.co')
password.send_keys('Jcamilo.210657')
clicaBoton  = driver.find_element(By.XPATH, '//*[@id="LogIn"]')
clicaBoton.click()

time.sleep(2)

cajaFicha   = driver.find_element(By.XPATH, '//*[@id="nombreMateria"]')
cajaFicha.send_keys('2758519')
botonBuscar = driver.find_element(By.XPATH, '//*[@id="nombreMateriabuscar"]')
botonBuscar.click()

time.sleep(2)

botonMostrarFicha = driver.find_element(By.XPATH, '//*[@id="catalogo-main-content"]/li/div/div[2]/span[1]/div/a')
botonMostrarFicha.click()

ban = True
contador = 50
while ban and contador > 0 :
    try:
        time.sleep(2)
        driver.execute_script('javascript:verMas()')
    except:
        ban = False
    contador -= 1

# Ejecutar el script de impresión
driver.execute_script('window.print();')

# Esperar 20 segundos
time.sleep(2)

# Cerrar el driver
driver.quit()

print("-----FIN-----")