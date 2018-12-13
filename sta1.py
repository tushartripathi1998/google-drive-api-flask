from __future__ import print_function
import sys
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from flask import Flask

app = Flask(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'

@app.route('/')
def index():
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('drive', 'v3', http=creds.authorize(Http()))

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.', file=sys.stderr)
        else:
            print('Files:', file=sys.stderr)
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']),file=sys.stderr)
        return '''Hey there'''

if __name__ == '__main__':
    app.run(debug=True)
