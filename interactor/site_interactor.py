import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options


class WbScrp:
    def __init__(self, url, visible):
        """Instala o chromedriver e inicia o webdriver do chrome

        Args:
            url (string): recebe a url para abrir
            visible (boolean): torna a janela visivel ou não
        """        
        chromedriver_autoinstaller.install()  # instala o chrome driver e o adiciona ao path
        chrome_options = Options()
        if not visible:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get(url)

    def wait_until(self, xpath, seconds, ec):
        """Recebe o xpath de um elemento e espera uma quantidade de segundos até a
            Expected Condition (presence ou clickable)

        Args:
            xpath (string): xpath do elemento a ser esperado
            seconds (int): quantidade de segundos que será aguardada
            ec (string): expected condition (presence ou clickable)
        """
        
        expected_condition = {
            "presence": EC.presence_of_element_located,
            "clickable": EC.element_to_be_clickable
        }
        WebDriverWait(self.driver, seconds).until(
            expected_condition[ec]((By.XPATH, xpath)),
            message=f"O elemento não foi encontrado a tempo, xpath={xpath}"
        )

    def all_options(self, xpath, seconds_to_wait=10):
        """Recebe o xpath de um dropdown e retorna uma lista com todos os nomes de cada opcao

        Args:
            xpath (string): xpath do dropdown 

        Returns:
            list: uma lista com todos os nomes de cada opção
        """        
        """"""
        self.wait_until(
            xpath=xpath,
            seconds=seconds_to_wait,
            ec="clickable"
        )
        select_element = Select(
            self.driver.find_element(By.XPATH, xpath)
        )
        all_element_names = []
        for option in select_element.options:
            all_element_names.append(option.get_attribute("text"))

        return all_element_names

    def table_html_to_df(self, table_xpath, seconds_to_wait=10):
        """Recebe o xpath de uma tabela em html e a transforma em dataframe

        Args:
            table_xpath (string): xpath da tabela a ser transformado em dataframe

        Returns:
            pd.DataFrame: retorna um dataframe do pandas da tabela passada
        """
        import pandas as pd

        self.wait_until(
            xpath=table_xpath,
            seconds=seconds_to_wait,
            ec="presence"
        )
        table = self.driver.find_element(By.XPATH, table_xpath)
        table_html = table.get_attribute("outerHTML")

        return pd.read_html(table_html, thousands='.', decimal=',')[0]

    def select_option_dropdown(self, dropdown_xpath, option_name, seconds_to_wait=10):
        """Recebe xpath de um dropdown e uma opcao dentro desse e a seleciona

        Args:
            dropdown_xpath (string): xpath do dropdown
            option_name (string): texto visivel da opcao
        """        
        self.wait_until(
            xpath=dropdown_xpath,
            seconds=seconds_to_wait,
            ec="clickable"
        )
        select = Select(self.driver.find_element(By.XPATH, dropdown_xpath))
        select.select_by_visible_text(option_name)

    def click_xpath(self, xpath, seconds_to_wait=10):         
        self.wait_until(
            xpath=xpath,
            seconds=seconds_to_wait,
            ec="clickable"
        )
        self.driver.find_element(By.XPATH, xpath).click()

    def switch_to_frame_xpath(self, xpath, seconds_to_wait=10):
        self.wait_until(
            xpath=xpath, 
            seconds=seconds_to_wait, 
            ec="presence"
        )
        self.driver.switch_to.frame(
            self.driver.find_element(By.XPATH, xpath)
        )
