from .eventcreate import builder
import datefinder

def create():
    start_time = input('Enter date month time AM/PM format Eg:30 may 8:15 PM ')
    end_time = input('Enter date month time AM/PM format same as start time ')
    summary = input('Event summary ')
    total = int(input('Enter total number of attendes '))
    email_ids = []
    for i in range(total):
      email = input('Enter an email id and press enter ')
      email_ids.append(email)
    print('Creating event ')
    create_event(email_ids,start_time,end_time,summary)
    print('event created')

def create_event(email_ids, start_time, end_time, summary):
    start_time = list(datefinder.find_dates(start_time))
    end_time = list(datefinder.find_dates(end_time))
    start_time = start_time[0]
    end_time = end_time[0]

    EVENT = {
              "end": {
                "timeZone": "Asia/Kolkata",
                "dateTime": end_time.strftime('%Y-%m-%dT%H:%M:%S')
              },
              "start": {
                "dateTime": start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                "timeZone": "Asia/Kolkata"
              },
              "attendees": [],
              "reminders": {
                "useDefault": True
              },
              "description": "description",
              "summary":  summary,
              "location": "Chennai"
            }

    for email_id in email_ids:
        EVENT["attendees"].append({"email": email_id})

    event = builder().events().insert(calendarId='primary', body=EVENT, sendNotifications=True).execute()
    return True

def delete(id):
    try:
        builder().events().delete(calendarId='primary', eventId=id).execute()
        print('event deleted')
    except Exception as e:
        print(e)
def update(id):
    try:
        event = builder().events().get(calendarId='primary', eventId=id).execute()
        if event:
            start_time = input('Enter new start time: ')
            end_time = input('Enter new end time: ')
            start_time = list(datefinder.find_dates(start_time))
            end_time = list(datefinder.find_dates(end_time))
            start_time = start_time[0]
            end_time = end_time[0]
            try:
                event['start']['dateTime'] = start_time.strftime('%Y-%m-%dT%H:%M:%S')
                event['end']['dateTime'] = end_time.strftime('%Y-%m-%dT%H:%M:%S')
                updated_event = builder().events().update(calendarId='primary', eventId=id, body=event).execute()
                print('Event updated',updated_event['updated'])
            except Exception as e:
                print(e)
            print('Event found')
        else:
            print('Event not found')
    except Exception as e:
        print(e)
def events():
    try:
        page_token = None
        while True:
            events = builder().events().list(calendarId='primary', pageToken=page_token).execute()
            if not events:
                print('No events')
            else:
                for event in events['items']:
                    print(event['summary'], event['id'])
                page_token = events.get('nextPageToken')
                if not page_token:
                    break
    except Exception as e:
        print(e)


