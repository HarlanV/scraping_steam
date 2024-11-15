## Requisitos

# Python
O projeto foi desenvolvido utlizando o Python 3.13.0

# Pacotes
Os pacotes necessarios para execução do projeto estão listados em requirements.txt . Para importação direta, execute o comando abaixo
> pip install -r /path/to/requirements.txt

## Configuração

# Google BigQuery
1 - Para gerar tabela no google bigquery, é necessário ter uma chave de acesso do tipo json, que deve ser armazenada na raiz do projeto.

2 - altere o nome da variavel "key_path" no arquivo main.py de acordo com o nome que deu para sua chave json.

3 - É necessário preencher as informações da sua tabela de destino dentro do arquivo .env

Obs: Caso não tenha acesso ao BQ e pretenda visualizar apenas local, verifique as linhas as serem comentadas e descomentadas no main. Elas estão sinalizadas por comentarios.


# Configuração de 


## Execução
Para execução do projeto, após baixado e devidamente configurado, basta a execução do arquivo main.py