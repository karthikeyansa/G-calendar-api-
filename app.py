from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from datetime import datetime,timedelta
import datefinder

scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file('client_secret.json',scopes=scopes)

#credentials =  flow.run_local_server()
#pickle.dump(credentials,open('token.pkl','wb'))
credentials = pickle.load(open('token.pkl','rb'))
service = build('calendar','v3',credentials=credentials)
result = service.calendarList().list().execute()
calendar_id = result['items'][0]['id']
result = service.events().list(calendarId = calendar_id,timeZone  = "Asia/Kolkata").execute()
print(result)
#create event
start_time = input('Enter date month time AM/PM format')
summary = input('Event summary')

def create_event(start_time, summary, duration=1, description=None, location=None):
  matches = list(datefinder.find_dates(start_time))
  if len(matches):
    start_time = matches[0]
    end_time = start_time + timedelta(hours=duration)

  event = {
    'summary': summary,
    'location': location,
    'description': description,
    'start': {
      'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
      'timeZone': 'Asia/Kolkata',
    },
    'end': {
      'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
      'timeZone': 'Asia/Kolkata',
    },
    'attendees': [
      {'email': 'karthikeyansa39@gmail.com'},
    ],
    'reminders': {
      'useDefault': False,
      'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
      ],
    },
  }
  return service.events().insert(calendarId='primary', body=event).execute()
create_event(start_time,summary)
print('Event created')

page_token = None
while True:
  events = service.events().list(calendarId='primary', pageToken=page_token).execute()
  for event in events['items']:
    print (event['summary'],event['id'])
    service.events().delete(calendarId='primary', eventId=event['id']).execute()
    print('Event destroyed')
  page_token = events.get('nextPageToken')
  if not page_token:
    break

