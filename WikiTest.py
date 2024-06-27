from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
import logging
import time

# Configuração de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    driver = webdriver.Chrome()
    return driver

def teardown_driver(driver):
    driver.quit()

def open_page(driver, url):
    driver.get(url)

def check_element_displayed(driver, by, value):
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
        return element.is_displayed()
    except (NoSuchElementException, TimeoutException):
        return False

def capture_screenshot(driver, name):
    driver.save_screenshot(name)

def main():
    driver = setup_driver()
    url = "https://pt.wikipedia.org/wiki/Selenium_(software)"
    
    num_repetitions = 5
    for i in range(num_repetitions):
        open_page(driver, url)
        logging.info(f"Execução {i + 1}:")
        
        if check_element_displayed(driver, By.CSS_SELECTOR, "img.mw-logo-wordmark"):
            logging.info("Imagem encontrada na página!")
        else:
            logging.warning("Imagem não encontrada na página")

        if check_element_displayed(driver, By.CSS_SELECTOR, "img[src*='Selenium_Logo.png']"):
            logging.info("Imagem do logotipo do Selenium encontrada na página!")
        else:
            logging.warning("Imagem do logotipo do Selenium não encontrada na página")

        if check_element_displayed(driver, By.XPATH, "//a[@href='https://github.com/SeleniumHQ/selenium/releases/tag/selenium-4.16.0']"):
            logging.info("Primeiro link encontrado na página!")
        else:
            logging.warning("Primeiro link não encontrado na página")

        if check_element_displayed(driver, By.XPATH, "//a[@href='https://www.selenium.dev/downloads/']"):
            logging.info("Segundo link encontrado na página!")
        else:
            logging.warning("Segundo link não encontrado na página")

        if check_element_displayed(driver, By.ID, "firstHeading"):
            title_element = driver.find_element(By.ID, "firstHeading")
            if title_element.text == "Selenium (software)":
                logging.info("Título da página está correto!")
            else:
                logging.warning("Título da página está incorreto")
        else:
            logging.warning("Título da página não encontrado")

        if check_element_displayed(driver, By.XPATH, "//p[contains(text(),'Selenium')]"):
            logging.info("Palavra encontrada na página!")
        else:
            logging.warning("Palavra não encontrada na página")

        capture_screenshot(driver, f"pagina_selenium_{i + 1}.png")
        logging.info(f"Captura de tela salva como 'pagina_selenium_{i + 1}.png'")

        if check_element_displayed(driver, By.CSS_SELECTOR, ".reflist"):
            table_element = driver.find_element(By.CSS_SELECTOR, ".reflist")
            rows = table_element.find_elements(By.TAG_NAME, "li")
            logging.info(f"Tabela de referências encontrada com {len(rows)} linhas")
        else:
            logging.warning("Tabela de referências não encontrada")

        # Teste do link para a página 'Framework'
        try:
            framework_link = driver.find_element(By.XPATH, "//a[@href='/wiki/Framework']")
            if framework_link.is_displayed():
                framework_link.click()
                logging.info("Navegando para a página de 'Framework'...")
                
                # Verifica se a navegação foi bem-sucedida
                WebDriverWait(driver, 10).until(EC.url_contains('/wiki/Framework'))
                if check_element_displayed(driver, By.ID, "firstHeading"):
                    title_element = driver.find_element(By.ID, "firstHeading")
                    if title_element.text == "Framework":
                        logging.info("Navegação para a página 'Framework' bem-sucedida e título correto!")
                    else:
                        logging.warning("Título da página 'Framework' está incorreto")
                else:
                    logging.warning("Título da página 'Framework' não encontrado")
                
                # Volta para a página anterior
                driver.back()
            else:
                logging.warning("Link para 'Framework' não encontrado na página")
        except NoSuchElementException:
            logging.warning("Link para 'Framework' não encontrado na página")
        
        # Atualiza a página ao invés de fechar o navegador
        driver.refresh()
        time.sleep(2)

    teardown_driver(driver)

if __name__ == "__main__":
    main()
