from WebTools import WebScraping
from TableSteam import TableSteam
from bs4 import BeautifulSoup
from ExportTable import ExportTableBQ


url = 'https://steamdb.info/sales/'
path = "page"
key_path = 'chave-bq.json'


print("Iniciando processo...")

# Caso tenha dado algum problema no processo da tabela, porem o html está correto: trocar as linhas abaixo
html_content = WebScraping(url, path).execute().get_html_file()
# html_content = WebScraping(url, path).get_html_file()

print("Html gerado! Criando tabela...")

soup = BeautifulSoup(html_content, 'html.parser')

table = TableSteam(soup).get_data()

print("Tabela gerada. Exportando resultados...")

# descomentar abaixo para gerar dados locais em xlsx
#table.to_excel("dados_steam.xlsx",sheet_name='dados_enviados')

# comente abaixo caso não tenha acesso ao google bq
export_status = ExportTableBQ(key_path).export_table(table)
print("Processo Finalizado !!")
