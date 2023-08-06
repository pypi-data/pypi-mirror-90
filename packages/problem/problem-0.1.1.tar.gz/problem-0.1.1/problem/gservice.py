from oauth2client.service_account import ServiceAccountCredentials
import gspread

class gsheet:
    def __init__(self, mode, json_api, sheet_url):
        if mode == 'rw': scope = ['https://www.googleapis.com/auth/spreadsheets']
        elif mode == 'r' : scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(json, scope)
        client = gspread.authorize(credentials)
        self.sheet = client.open_by_url(sheet_url)

    def select_worksheet(self, sheet_page):
        sheet_page = (sheet_page-1)
        if self.sheet.get_worksheet(sheet_page): return self.sheet.get_worksheet(sheet_page)
        else: print('No work sheet')

    def update_row(self, sheet_page, list_value):
        sheet_page.append_row(list_value)