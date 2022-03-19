import pandas as pd
import requests
from datetime import datetime
import json
import os
import re
import numpy as np
import json
pd.options.mode.chained_assignment = None


class Link_Manager():
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.base_link = dir_path
        # self.path_10K = os.path.join(self.base_link , 'Data','Dataframes','10_K.csv')
        # self.path_10Q = os.path.join(self.base_link , 'Data','Dataframes','10_Q.csv')
        # self.path_8K = os.path.join(self.base_link , 'Data','Dataframes','8_K.csv')
        # self.path_10K_old = os.path.join(self.base_link , 'Data','Dataframes','10_K.csv')
        # self.path_10Q_old = os.path.join(self.base_link , 'Data','Dataframes','10_Q.csv')
        # self.path_8K_old = os.path.join(self.base_link , 'Data','Dataframes','8_K.csv')
        # print(self.path_10K)
        os.path.join(self.base_link,'Data','Temp','index.idx')
        # self.update()
        try:
            self.df10Q = pd.read_csv(
                os.path.join(self.base_link,'Data','Dataframes','10_Q.csv'))
            self.df10K = pd.read_csv(
                os.path.join(self.base_link,'Data','Dataframes','10_K.csv'))
            self.df8K = pd.read_csv(
                os.path.join(self.base_link , 'Data','Dataframes','8_K.csv'))
        except:
            # Folder does not exist
            self.fetch_old_index()
            self.update()

    def _parse_idx(self):
        """Function to parse form.idx files from sec edgar"""
        form = []
        date = []
        location = []
        CIK = []
        company = []
        flag = True
        with open(
            os.path.join(self.base_link,'Data','Temp','index.idx'), encoding='Latin_1') as f:
            for line in f:
                if flag:
                    try:
                        if line.split()[0] == '1-A':
                            flag = False
                        else:
                            continue
                    except:
                        continue
                line = line.split()
                CIK.append(line[-3])
                company.append(" ".join(line[1:-3]))
                form.append(line[0])
                date.append(line[-2])
                location.append(line[-1])
        df = pd.DataFrame({'CIK': CIK,
                           'Company': company,
                           'Type': form,
                           'Date': date,
                           'Location': location})
        return df

    def _get_idx(self, year, Qtr):
        """Function to get index year and QTR wise"""
        link = "https://www.sec.gov/Archives/edgar/full-index/"
        link = link + str(year) + "/" + "QTR" + str(Qtr) + "/" + "form.idx"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
        r = requests.get(link, headers=headers)
        with open(
            os.path.join(self.base_link,'Data','Temp','index.idx'), 'wb') as f:
            f.write(r.content)

    def fetch_old_index(self, years=None):
        """Function to get all old index. Run this once every Quarter"""
        try:
            os.remove(os.path.join(self.base_link , 'Data','Dataframes','10_K_old.csv'))
            os.remove(os.path.join(self.base_link , 'Data','Dataframes','8_K_old.csv'))
            os.remove(os.path.join(self.base_link , 'Data','Dataframes','10_Q_old.csv'))
        except:
            pass
        if years == None:
            years = list(range(1993, datetime.now().year))
        flag = True
        for year in years:
            for i in range(1, 5):
                self._get_idx(year, i)
                df = self._parse_idx()
                groups = df.groupby('Type')
                mode = 'a'
                try:  # Fail silently, form Not available if failed:/
                    groups.get_group(
                        '10-K').to_csv(
                            os.path.join(self.base_link , 'Data','Dataframes','10_K_old.csv'), mode=mode, index=False)
                except:
                    pass
                try:
                    groups.get_group(
                        '8-K').to_csv(os.path.join(self.base_link , 'Data','Dataframes','8_K_old.csv'), mode=mode, index=False)
                except:
                    pass
                try:
                    groups.get_group(
                        '10-Q').to_csv(os.path.join(self.base_link , 'Data','Dataframes','10_Q_old.csv'), mode=mode, index=False)
                except:
                    pass
                print(year, i, 'Completed')

    def update(self):
        """Function to fetch latest index file. Run this once everyday"""
        try:
            os.remove(os.path.join(self.base_link , 'Data','Dataframes','10_K.csv'))
            os.remove(os.path.join(self.base_link , 'Data','Dataframes','8_K.csv'))
            os.remove(os.path.join(self.base_link + 'Data','Dataframes','10_Q.csv'))
        except:
            pass
        link = "https://www.sec.gov/Archives/edgar/full-index/form.idx"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
        r = requests.get(link, headers=headers)
        with open(os.path.join(self.base_link,'Data','Temp','index.idx'), 'wb') as f:
            f.write(r.content)
        df = self._parse_idx()
        groups = df.groupby('Type')
        groups.get_group('10-K')
        groups.get_group('8-K')
        groups.get_group('10-Q')
        df_old = pd.read_csv(os.path.join(self.base_link , 'Data','Dataframes','10_K.csv'))
        self.df10K = pd.concat([df_old, groups.get_group('10-K')],
                               axis=0).reset_index(drop=True)
        df_old = pd.read_csv(os.path.join(self.base_link , 'Data','Dataframes','10_Q.csv'))
        self.df10Q = pd.concat([df_old, groups.get_group('10-Q')],
                               axis=0).reset_index(drop=True)
        df_old = pd.read_csv(os.path.join(self.base_link , 'Data','Dataframes','8_K.csv'))
        self.df8K = pd.concat([df_old, groups.get_group('8-K')],
                              axis=0).reset_index(drop=True)
        self.df10Q.to_csv(
            os.path.join(self.base_link , 'Data','Dataframes','10_Q.csv'), index=False)
        self.df10K.to_csv(
            os.path.join(self.base_link , 'Data','Dataframes','10_K.csv'), index=False)
        self.df8K.to_csv(os.path.join(self.base_link , 'Data','Dataframes','8_K.csv'), index=False)

    def get_form_link(self, link):
        """ Return link to the form from given link in forms.idx"""
        front = 'https://www.sec.gov/Archives/'
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
        link = front + link
        text = requests.get(link, headers=headers, timeout=1).text
        for line in text.split('\n'):
            if line.startswith('<FILENAME>'):
                file = line.replace('<FILENAME>', '')
                break
        link = link.replace('-', '').replace('.txt', '') + '/' + file
        return link

    def _fetch(self, df, n):
        """Fetches the links from DataFrame"""
        if len(df) == 0:
            return None
        df.loc[:, 'Date'] = pd.to_datetime(
            df.loc[:, 'Date'], errors='coerce').values.astype(np.int64) // 10 ** 9
        df = df.sort_values('Date', ascending=False)
        links = []
        for link in df.Location[:n]:
            links.append(self.get_form_link(link))
        return list(zip(links, list(df.Date)))

    def fetch(self, cik, query, n=3):
        """Fetches forms and financial report based on CIK.\n
            Attributes:\n
            cik :\t CIK id of the company to query, without leading zeros\n
            query:\t Supprted: { "10-K", "8-K", "10-Q","FinRep}\n
            n:\t Number of results from most recent to least order.\n
            Returns: \n
                \t* list of tuple pairs of links and dates in timestamps
                \t* None if not found or if query is wrong
            """
        if query == '10-K':
            df = self.df10K
            return self._fetch(df=df[df.CIK == str(cik)], n=n)

        elif query == '8-K':
            df = self.df8K
            return self._fetch(df=df[df.CIK == str(cik)], n=n)

        elif query == '10-Q':
            df = self.df10Q
            return self._fetch(df=df[df.CIK == str(cik)], n=n)

        elif query == 'FinRep':
            df = self.df10K
            df = df[df.CIK == str(cik)]
            if len(df) == 0:
                return None
            df.loc[:, 'Date'] = pd.to_datetime(
                df.loc[:, 'Date'], errors='coerce').values.astype(np.int64) // 10 ** 9
            df = df.sort_values('Date', ascending=False)
            links = df.Location
            dates = list(df.Date)
            front = 'https://www.sec.gov/Archives/'
            file = 'Financial_Report.xlsx'
            ret_links = []

            for link in links:
                link = front + \
                    link.replace('.txt', '/').replace('-', '') + file
                ret_links.append(link)
            return list(zip(ret_links[:n], dates[:n]))

    def fetch_mappings(self):
        self.load()
        companies = list(self.df10K.Company)
        cik = list(self.df10K.CIK)
        companies.extend(list(self.df10Q.Company))
        cik.extend(list(self.df10Q.CIK))
        companies.extend(list(self.df8K.Company))
        cik.extend(list(self.df8K.CIK))
        mappings = dict(zip(companies, cik))
        # jsonarr = json.dumps(mappings, indent=2)
        return mappings

    def load(self):
            self.df10Q = pd.read_csv(
                os.path.join(self.base_link,'Data','Dataframes','10_Q.csv'))
            self.df10K = pd.read_csv(
                os.path.join(self.base_link,'Data','Dataframes','10_K.csv'))
            self.df8K = pd.read_csv(
                os.path.join(self.base_link , 'Data','Dataframes','8_K.csv'))
