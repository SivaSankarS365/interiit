import requests
from bs4 import BeautifulSoup as bs
import os
import re
# import logging
from price_parser import Price

# logging.basicConfig(filename='balance_sheet_extraction.log',
#                     encoding='utf-8', level=logging.DEBUG)


class Extractor():
    def __init__(self):
        """
            Define Metrics Here Along with acceptable search words    
        """
        self.metrics_dict = {'total_asset': 'totalasset',
                             "shareholder_equity": 'stockholdersequity',
                             'net_loss': 'netloss',
                             'total_liabilities': 'totalliabilit',
                              }

    def search_amount(self, table_row):
        """
    Function which reads the Table Row of Balance Sheet and Returns Amount in it.
        """
        ix_tag = table_row.findChildren('ix:nonfraction', text=True)
        amount_text = (re.sub('<.*?>', '!#!', str(table_row)))
        amount = Price.fromstring(amount_text)
        # amount = amount.split('!#!')[0]
        return amount.amount_float

    def read_balance_sheet(self, all_div):
        """
        Function That Reads the HTML file and returns the Balance Sheet found inside
        Returns : list of form [[balance_sheet_div_html], [balance_sheet_table_html]] : supposed to be of len = 1
        """
        # list of form [[balance_sheet_div_html], [balance_sheet_table_html]] : supposed to be of len = 1
        balance_sheets = []
        for div in all_div:
            # if more than one Balance Sheets found
            # if len(balance_sheets) > 1:
            #     logging.warnings('Found MORE THAN 1 BALANCE SHEET')
            tables = div.findChildren('table', recursive=False)
            if len(tables) > 0:
                for table in tables:
                    # Search 'Balance Sheets' & 'Total Assets' in this div and table respectively
                    text_div = str(div).lower().replace(" ", "")
                    text_table = str(table).lower().replace(" ", "")
                    search_bal = re.search('balancesheet', text_div)
                    search_assets = (re.search('totalasset', text_table))
                    if search_bal is not None and search_assets is not None:
                        balance_sheets.append([div, table])
                        # logging.info('Found Balance Sheet')
        return balance_sheets

    def _get_html(self, link):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
        text = requests.get(link, headers=headers, timeout=1).text
        return text

    def _scrap(self, link, out_dict={}):
        """function to scrap based on link given"""
        html = self._get_html(link)
        soup = bs(html, "lxml")
        all_div = soup.find_all("div")
        balance_sheets = self.read_balance_sheet(all_div)
        for balance_sheet in balance_sheets:
            div = balance_sheet[0]
            table = balance_sheet[1]
            table_rows = table.findChildren('tr')
            for table_row in table_rows:
                text = re.sub('[^a-z]', '', str(table_row).lower())
                # Searching for METRICS in table row
                # Searching for all metrics and adding them to dict
                for metric in self.metrics_dict.keys():
                    metric_matches = re.search(self.metrics_dict[metric], text)
                    if metric_matches is not None:
                        # Search for value of this metric if match found
                        out_dict[metric] = self.search_amount(
                            table_row)
        return out_dict, balance_sheets[0][0]

    def scrap_metrics(self, to_extract, add_info):
        """
        Function to Scrape Metrics from Specified HTML File\n
        Input: \n
            \t* to_extract:    \tList of link,date pairs from Link_Manager\n
           \t * add_info:  \tAdditional information like CIK,Form type,etc\n
        Returns : \n
                List of dictionary of Metric and Values in format {'Metric_name': 'Value_Found'} along
                with additional information provides.
        """
        extracted = []
        for link, date in to_extract:
            metrics = {}
            for key, value in add_info.items():
                metrics[key] = value
            metrics["Date"] = date
            metrics, balance_sheet_div = self._scrap(link, metrics)
            mul = '$'
            # Search for amounts in thousands or millions
            text = re.sub('<.*?>', '', str(balance_sheet_div)
                          ).lower().replace(' ', '')
            if 'thousand' in text:
                mul = 'Thousand $'
            elif 'million' in text:
                mul = 'Million $'
            metrics['amount_in'] = mul
            metrics['balance_sheet_html'] = balance_sheet_div
            extracted.append(metrics)
        return extracted
