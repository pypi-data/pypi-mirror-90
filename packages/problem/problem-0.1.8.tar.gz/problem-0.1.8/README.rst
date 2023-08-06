Need more problem?
==================

install
~~~~~~~

.. code:: python

    pip install problem

google sheet
~~~~~~~~~~~~

.. code:: python

    sheet_type = 1 #0(read-only), 1(read and write)
    url_id = '1mR5oLXxxXxxSdSSegtbxxxxxxxxL6Da7VSN_ThpSs' #id of share link
    json = {'type': 'service_account',
            'project_id': 'demo',
            'private_key_id': 'cxxxc5xxxxxxxxxxxxxxx74xxxxxxx15x41',
            'private_key': '-----BEGIN PRIVATE KEY-----\xxxxxxxxxxxxxxxxxxxxx\n-----END PRIVATE KEY-----\n',
            'client_email': 'email@demo.iam.gserviceaccount.com',
            'client_id': '254998354398547502142',
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
            'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x5/email@demo.iam.gserviceaccount.com'}

.. code:: python

    gs = gsheet(sheet_type, json, url_id) #connect to sheet
    sheet1 = gs.select_worksheet(1) #select sheet page
    gs.update_row(sheet1, ['1', '20/12/2020', '200USD', 100]) #update row in sheet page

google drive
~~~~~~~~~~~~

.. code:: python

    url_id = '1mR5oLXxxXxxSdSSegtbxxxxxxxxL6Da7VSN_ThpSs' #id of share link
    gd = gdrive()
    gd.download(url_id) #download file

