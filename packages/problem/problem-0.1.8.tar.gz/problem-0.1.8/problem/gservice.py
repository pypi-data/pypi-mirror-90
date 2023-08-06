from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import gspread
import gdown
import requests

class gsheet:
    def __init__(self, sheet_type, json_api, url_id):
        """
        mode : 0(read-only), 1(read and write)

        json_api : json variable form google sheet api 

        url_id : id of share link ex. 1mR5oLFWVIdSdSSegtbem6mn70nebCL6Da7VSN_ThpSs
                    
        """
        sheet_url = f'https://docs.google.com/spreadsheets/d/{url_id}/edit?usp=sharing'
        if sheet_type == 1: scope = ['https://www.googleapis.com/auth/spreadsheets']
        elif sheet_type == 0 : scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
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

if __name__ == '__main__':
    mode = 'rw'
    json = {'type': 'service_account',
            'project_id': 'ai-history',
            'private_key_id': 'c798c51fa2c0ed554db45374ff8c07ab225f5d41',
            'private_key': '-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDfkL7zgkh5FfXD\nHPyb5zV53NugxOxIHh3kFgBO1Sns4/uofgPb/8gjmhmHnM6TN0NuOQSr8YfORI/y\nUDfa7axOJbmExsYP8ZZiKxmFMmnmXLBm9tUjMFzMQcqxS45J4ViL0nc71jXUnp6O\nufJNKIrjwKqWsmi3py3R9I08pCyfCRC2e/U9iEM9CSi4c48vOpaQq/VfclE2I0HY\nErByN/MjjAn+kExzjyUx1Om73tRXqADQCsFp0tgk4P13ApihpYppA/ZXRiobTjhk\nJBM/OGq6cU2WyUrTj9217QX9Yr182YeSivAvKSyeCrX81tm8PXPFEl46MCE2KsNs\n6ubobE05AgMBAAECggEADPP83ky7gHmBX2RF7g4Buw1s87YJJx4IlxMfwjGHT/R/\nG5puhI//s3Fdno37KYwrhd67mq9AMjcmfHCBpfd8ktwMcUkXh2u0zfwHiuA6gsh2\nx4ZwX60xCTwcH3TcWgM6j0Ja2m6NOKQWlXgoVeheELdUYu4UE2T2Koqf5sYv2Chx\nbuUmG6+K4OoAgTXFdEXoG97EMlOxdllNj7I/VaZuaEfS9cguhCEloeKrlr5AtxSG\nRXJeURId7A+1YDJ9hpFO4vmIh8NRsFq9xa/iUoO+fgw8sRBL0gjrQKfuWPK7OZFp\nPyHq6NGPWgsI70vuIZUN6H14s6EsjXpQcKPUitDSwQKBgQD5G1eOt5zwbrJk7pIu\nehltv+a4mrdboVL3Pkaeec2HKkdlZFfZBfLVok4s2y0MQTjPTNcoRLWDA3i0MbOD\nCreIXdpfoJBorxMIGRjlgX424XJt3JQaKpyC7eFcrRPtVmnV1kf8E4GSo0JWBojd\nT1sG4Dwpvta5RfJ1cixNIQ77+QKBgQDlwHhc3A3jcMKogM3ss3QTkXJdsCqYRR1K\nWz6sN1Ek38JywWYDxwgN/jm4pQFW3jLlkQNb1MN2ggkv2f6hJv2vo1M4Sihymy9j\n37OO3ZqVFJqsKjnZjplHnMZyWYfUb7ZJV4adUsOClABCNTL/cy8h6X0FffqCYb8S\nurQA6YerQQKBgBYRlAoyvhaW1/sVH6I6cvJEI/6Kxl+5xQ3eWIdFpy2oUzbqUtYJ\nLuA6Rs62hCEnzg6fchhBLgtzTUg5dvvPAT91gRkjsmdzyy3We1wpwrK9+lM9TWmc\nCM2YoXSCaNeH5kxpdWshl0MUb5YLciiZFSlgyDOykndLeRVqjf4vRZKRAoGBALxm\n/sy3LzRpTVc8eKE372H0jaJCSkufsYs+E8DJg+MHEr9j1LIYToSbCt5dgSGpCHe0\nWNq/OKI/tCTnUKT6AmI7Po0UUuLYWx49XVM0agUCZmv0HIhJJWzSJPG0dWxBR2wR\nODReoDC+CRBB69YKsIXQoFMWoYy1dyh2rhFpb3WBAoGBAJ3DU6fQ0RnrwL66h6YK\n1cUhBcU3uBaLdClcDythbDnYra8Dt2MF5Uimldzygv2rK4fdQxi7YIQtAr5V07Se\niE978Rm892qfM3lseJ/gc0Q1/puLwGEPdKmB6cSBiHbelY2Q1/aCW8A7IVYS+BaD\nLf7wwJXxFONPgQ1v1k8vR5To\n-----END PRIVATE KEY-----\n',
            'client_email': 'email-name@ai-history.iam.gserviceaccount.com',
            'client_id': '111448330398979300581',
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
            'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x509/email-name%40ai-history.iam.gserviceaccount.com'}
    _id = '1mR5oLFWVIAeBaSegtbem6mn70nebCL6Da7VSN_ThpSs'
    gs = gsheet(mode, json, id)