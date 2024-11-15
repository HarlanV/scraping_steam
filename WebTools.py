from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time


class WebScraping:
    def __init__(self, url:str, local_html_name='page') -> None:
        self.local_html_name =  f"{local_html_name}.html"
        self.url = url


    def get_html_file(self):
        file_name = self.local_html_name
        with open(file_name, 'r', encoding='utf-8') as file:
            html_content = file.read()
            return html_content
        # soup = BeautifulSoup(html_content, 'html.parser')
        return soup


    def get_browser(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.experimental_options["prefs"] = {"profile.managed_default_content_settings.javascript": 2}
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        chrome_options.set_capability('browserName', 'chrome')
        browser = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))
        self.browser = browser
        return self.browser


    def save_file(self, file, file_name:str, encoding='utf-8') -> None:
            try:
                with open(file_name, 'w', encoding=encoding) as f:
                    f.write(file)
            except:
                raise Exception("Não foi possivel salvar o arquivo localmente")


    def download_page(self) -> bool:
        browser = self.get_browser()
        try:
            browser.get(self.url)
            time.sleep(10)
            html = browser.page_source
            self.save_file(html, self.local_html_name)
            return True
        except:
            return False
        finally:
            browser.quit()
        

    def execute(self):
        self.download_page()
        return self
