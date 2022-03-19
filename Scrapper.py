from Scrap.Extractor import Extractor
from Scrap.Link_Manager import Link_Manager
import json
from models.companies import insert_company


class ScrapWrap():
    def __init__(self):
        self.E = Extractor()
        self.L = Link_Manager()

    
    # def initiate(self):
    #     self.L.fetch_old_index()
    #     self.update()
        

    def update(self):
        """Function to update index database. Call this daily"""
        self.L.update()
        self.make_map()

    def update_quarter_end(self):
        """Function to add new quarter data. Call this once a quarter"""
        self.L.fetch_old_index()
        self.make_map()


    def extract(self, cik, form_type='10-K', n=3):
        """
        Function to Scrape Metrics from Specified HTML File\n
        Input: \n
            \t* to_extract:    \tList of link,date pairs from Link_Manager\n
           \t * add_info:  \tAdditional information like CIK,Form type,etc\n
        Returns : \n
                List of dictionary of Metric and Values in format {'Metric_name': 'Value_Found'} along
                with additional information provides.
        """
        to_extract = self.L.fetch(cik, form_type, n)
        add_info = {}
        add_info['CIK'] = cik
        add_info['Form Type'] = form_type
        return self.E.scrap_metrics(to_extract, add_info)

    def make_map(self):
        """Makes map to cik-company database"""
        mapping = self.L.fetch_mappings()
        with open('Data\mapped_cik.json') as f:
            mapped = json.load(f)
        for key, value in mapping.items():
            if value not in mapped:
                mapped.append(value)
                print('Inserting',key)
                insert_company(value, key)
        with open('mapped_cik.json', 'w') as f:
            json.dump(mapped, f)
