# Importando as bibliotecas necessárias
from bs4 import BeautifulSoup, Tag
import pandas as pd
from datetime import datetime, timedelta


class TableSteam():

    def __init__(self, soup_html:BeautifulSoup) -> None:
        self.soup_html = soup_html
        pass
    
    def get_table(self):
        self.table = self.soup_html.find('table', class_='table-sales')
        return self.table
    

    def get_rows(self, table:Tag):
        self.rows = table.find_all('tr')
        return self.rows
        

    def get_special_tags(self, table:Tag) -> list:
        span_classes = []
        subinfo_divs = table.find_all('div', class_='subinfo')
        for div in subinfo_divs:
            spans = div.find_all('span')
            for span in spans:
                if span.get('class'):  # Verifica se span tem o atributo class
                    span_classes.extend(span.get('class'))

        special_tags = list(set(span_classes))
        if 'cat' in special_tags: special_tags.remove('cat')
        self.special_tags = special_tags
        return special_tags


    def get_df_structure(self, table:Tag):
        columns_names = ["Name", "Price","Rating", "Release", "Ends", "Started" ]
        special_tags = self.get_special_tags(table)
        columns_names = [*columns_names, *special_tags]
        df_structure = {col: None for col in columns_names}
        return df_structure


    def get_deltatime(self, row:Tag,td_position:int):
        try:
            td = row.find_all('td')[td_position]
            value = td.attrs.get('data-sort')
            # value = td.attrs.get('data-sort').text
            return value
        except:
            return None


    def get_td_value_by_position(self, row:Tag, td_position:int) -> str:
        try:
            td = row.find_all('td')[td_position]
            value = td.text
            return value
        except:
            return None


    def get_name(self, row:Tag, td_position:int) -> str:

        try:
            # print(row)
            td = row.find_all('td')[td_position]
            # print(td)
            a_tag = td.find('a')
            name = a_tag.text
            return name        
        except:
            return None


    def get_discount(self, row:Tag, td_position:int)-> str:
        try:
            td = row.find_all('td')[td_position]
            value = td.text
            return value
        except:
            return 'n/a'




    def get_optional_tags(self, row:Tag, row_data:dict, td_position:int) -> dict:
        try:
            td = row.find_all('td')[td_position]
            subinfo_divs = td.find_all('div', class_='subinfo')[0]
            spans = subinfo_divs.find_all('span')
            for span in spans:
                classes = span['class']
                if 'cat' in classes: classes.remove('cat')
                key = ' '.join(classes)
                row_data[key] = span.get_text(strip=True)
            return row_data
        except:
            return row_data


    def data_treatment(self, df_sales:pd.DataFrame) -> pd.DataFrame:

        rename_columns = {
            "cat-daily-deal":'DailyDeal' , 
            "cat-week-long-deal":'WeekLongDeal' , 
            "cat-midweek-deal":'MidweekDeal' , 
            "highest-discount":'HighestDiscount', 
            "cat-top-seller":'TopSeller' , 
            "cat-weekend-deal":'WeekendDeal' , 
            "cat-play-for-free":'PlayForFree' , 
            "highest-discount-major":'HighestDiscountMajor' , 
            "cat-introductory-offer":'IntroductoryOffer' , 
        }

        df_sales = df_sales.rename(columns=rename_columns)

        df_sales['DailyDeal'] = df_sales['DailyDeal'].notnull()
        df_sales['WeekLongDeal'] = df_sales['WeekLongDeal'].notnull()
        df_sales['MidweekDeal'] = df_sales['MidweekDeal'].notnull()
        df_sales['TopSeller'] = df_sales['TopSeller'].notnull()
        df_sales['WeekendDeal'] = df_sales['WeekendDeal'].notnull()
        df_sales['PlayForFree'] = df_sales['PlayForFree'].notnull()
        df_sales['IntroductoryOffer'] = df_sales['IntroductoryOffer'].notnull()


        t_now = datetime.now()

        df_sales['Ends'] = df_sales['Ends'].astype(int)
        df_sales['Started'] = df_sales['Started'].astype(int)

        df_sales['Ends'] = df_sales['Ends'].apply(lambda x: (t_now - timedelta(milliseconds=x)).strftime("%Y-%m-%d"))
        df_sales['Started'] = df_sales['Started'].apply(lambda x: (t_now - timedelta(milliseconds=x)).strftime("%Y-%m-%d"))

        df_sales['Price'] = df_sales['Price'].str.replace("R$", "").str.replace(",", ".").str.replace(" ", "").astype(float)
        df_sales['Rating'] = df_sales['Rating'].str.replace("%", "").str.replace(" ", "").astype(float) / 100
        df_sales['Discount'] = df_sales['Discount'].str.replace("%", "").str.replace(" ", "").astype(float) / 100
        return df_sales


    def get_data(self) -> pd.DataFrame:
        table = self.get_table()
        rows = self.get_rows(table)
        df_structure = self.get_df_structure(table)
   
        table_data = []
        for row in rows[1:]: 
            row_data = df_structure.copy()
            row_data["Name"] = self.get_name(row,2)
            row_data["Discount"] = self.get_td_value_by_position(row,3)
            row_data["Price"] = self.get_td_value_by_position(row,4)
            row_data["Rating"] = self.get_td_value_by_position(row,5)
            row_data["Release"] = self.get_td_value_by_position(row,6)
            row_data["Ends"] = self.get_deltatime(row, 7)
            row_data["Started" ] = self.get_deltatime(row, 8)
            row_data = self.get_optional_tags(row,row_data,2)
            table_data.append(row_data)
        df_sales = pd.DataFrame(table_data)
        df_sales = self.data_treatment(df_sales)
        return df_sales
