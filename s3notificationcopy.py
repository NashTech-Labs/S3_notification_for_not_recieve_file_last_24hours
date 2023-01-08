#!/usr/bin/env python3
import boto3
from datetime import datetime,timedelta
import pytz
from json import dumps
from httplib2 import Http



s3 = boto3.resource('s3')

#bucket prefix
prefix= ['']  #Enter prefix for your bucket that You want to check 


#check your bucket is modified in last 24 hours

def check_bucket(i):

    time_now_UTC = datetime.utcnow().replace(tzinfo=pytz.UTC)
    delta_hours = time_now_UTC - timedelta(days=1) #hours
    year=int(delta_hours.strftime('%Y'))
    month=int(delta_hours.strftime('%m'))
    previous_day = int(delta_hours.strftime('%d'))
    present_day=int(datetime.today().strftime('%d'))

    # time_now_UTC = datetime.utcnow().replace(tzinfo=pytz.UTC)
    # delta_hours = time_now_UTC - timedelta(hours=17) #hours
    bucket = s3.Bucket("Enter_you_bucket")  # your bucket name
    for key in bucket.objects.filter(Prefix=i):
            if key.last_modified > datetime(year,month,previous_day,tzinfo = pytz.UTC) and  key.last_modified < datetime(year,month,present_day,tzinfo = pytz.UTC):
                print('Checking ')
                return True
    return False        

def sendnotification(msgsend):
    """Hangouts Chat incoming webhook quickstart."""
    url = "https://chat.googleapis.com/v1/spaces/ug6dJYAAAAE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=1p6NmhoowcKhI5Mue3-PEd4pGjOmAW2YdujlbUKW4UA%3D"
    message = {}
    msg = msgsend
    text = 'text'
    message[text]=msg
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(message),
    )



def main():
    Notrecieved =[]
    for i in prefix:
        if check_bucket(i):
                print(check_bucket(i))
                pass
        else:
                Notrecieved.append(i)            
    if len(Notrecieved) >=1:            
        message = "No files have been received in Following Interface in last 24 hours\n \n"
        newmessage = message
        for i in Notrecieved:
            newmessage=newmessage+i+'\n' 
        print(newmessage)
        sendnotification(newmessage)         

if __name__ == "__main__":
    main()
