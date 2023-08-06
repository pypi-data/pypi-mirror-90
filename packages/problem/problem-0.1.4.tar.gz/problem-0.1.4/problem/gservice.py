from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import gspread, gdown, requests

class gsheet:
    def __init__(self, mode, json_api, id):
        """
        mode : 'rw', 'r'
            'rw' = read and write
            'r' = read-only 

        json_api : json variable form google sheet api 

        id : id of share link ex. 1mR5oLFWVIdSdSSegtbem6mn70nebCL6Da7VSN_ThpSs
                    
        """
        sheet_url = f'https://drive.google.com/file/d/{id}/view?usp=sharing'
        if mode == 'rw': scope = ['https://www.googleapis.com/auth/spreadsheets']
        elif mode == 'r' : scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(json_api, scope)
        client = gspread.authorize(credentials)
        self.sheet = client.open_by_url(sheet_url)

    def select_worksheet(self, sheet_page):
        sheet_page = (sheet_page-1)
        if self.sheet.get_worksheet(sheet_page): return self.sheet.get_worksheet(sheet_page)
        else: print('No work sheet')

    def update_row(self, sheet_page, list_value):
        sheet_page.append_row(list_value)

class gdrive:
    def download(self, id):
        url = requests.get(f'https://drive.google.com/file/d/{id}/view?usp=sharing', headers = {'User-Agent': 'Mozilla/5.0','Content-Type': 'application/x-www-form-urlencoded','Referer': 'https://www.investing.com/equities/credit-agricole-technical','X-Requested-With': 'XMLHttpRequest'})
        soup = BeautifulSoup(url.content, 'html.parser')
        filename = soup.find('title').text.split()[0]
        gdown.download(f'https://drive.google.com/uc?id={id}', f'{filename}', quiet=False)