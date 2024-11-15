from WebTools import WebScraping
from TableSteam import TableSteam
from bs4 import BeautifulSoup
from ExportTable import ExportTableBQ


url = 'https://steamdb.info/sales/'
path = "page"
key_path = 'chave-bq.json'


print("Iniciando processo...")
# html_content = WebScraping(url, path).execute().get_html_file()
html_content = WebScraping(url, path).get_html_file()

print("html gerado!")

soup = BeautifulSoup(html_content, 'html.parser')

print("Soup gerado!")

table = TableSteam(soup).get_data()

print("Dataframe Gerado!")

table.to_excel("dados_steam.xlsx",sheet_name='dados_enviados')
export_status = ExportTableBQ(key_path).export_table(table)
print("!! Processo Finalizado !!")
