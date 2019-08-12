import json
import requests
from datetime import datetime, timedelta

#CONFIG BLOCK
QROWDDB = "http://streambase1.disi.unitn.it:8090/checkuserdata"
EXPCODE = 'qrowd5'
MIN_DATA_HOURS = 10
DATE = (datetime.today()-timedelta(days=1)).strftime('%Y%m%d')
#DATE = "20190313"

def checkusersdata(dates, project):
    headers = {
            'cache-control' : 'no-cache' ,
            'email': config['ilog']['serverlogin'] , 
            'password': config['ilog']['serverpassword'] ,
            'dates': str(dates),
            'project': project
            }
    r = requests.get(QROWDDB, headers=headers)
    return r.json()

def gen_data_lists(usersdata):
    no_data_list = []
    insufficient_data_list = []
    enough_data_list = []
    for udata in usersdata['payload']['data']:
        utabs = udata['days'][0]['tables']
        if is_no_data(utabs,MIN_DATA_HOURS):
            no_data_list.append(udata)
        elif is_enough_data(utabs,MIN_DATA_HOURS):
            enough_data_list.append(udata)
        else:
            insufficient_data_list.append(udata)
    return (no_data_list,insufficient_data_list,enough_data_list)

def is_no_data(utabs,hours=24):
    return (location_average(utabs,hours) == 0.0 and accelerometer_average(utabs,hours) == 0.0)

def is_enough_data(utabs,hours=24):
    return (location_average(utabs,hours) >= 1.0 and accelerometer_average(utabs,hours) >= 1.0)

def location_average(daily_data,hours=24):
    """Receives daily data in format returned by iLog
    returns average location use
    """
    location = [record['presence'] for record in daily_data if record['tablename'] == 'locationeventpertime']
    location_array = location[0]
    return sum(location_array)/hours

def accelerometer_average(daily_data,hours=24):
    """Receives daily data in format returned by iLog
    returns average location use
    """
    accelerometer = [record['presence'] for record in daily_data if record['tablename'] == 'accelerometerevent']
    accelerometer_array = accelerometer[0]
    return sum(accelerometer_array)/hours

def gyroscope_average(daily_data,hours=24):
    """Receives daily data in format returned by iLog
    returns average location use
    """
    gyroscope = [record['presence'] for record in daily_data if record['tablename'] == 'gyroscopeevent']
    gyroscope_array = gyroscope[0]
    return sum(gyroscope_array)/hours


def main():
    users_data = checkusersdata(dates={"dates": [DATE]},project=EXPCODE)
    with open(DATE+'/full_user_data_'+DATE,'w') as f:
        json.dump(users_data,f,sort_keys=True,indent=2)

    lists = gen_data_lists(users_data)
    no_data_list = lists[0]
    print("No data: "+str(len(no_data_list)))
    
    with open(DATE+'/no_data_list_'+DATE,'w') as f:
        json.dump(no_data_list,f,sort_keys=True,indent=2)

    insufficient_data_list = lists[1]
    print("Insufficient data: "+str(len(insufficient_data_list)))
    with open(DATE+'/insufficient_data_list_'+DATE,'w') as f:
        json.dump(insufficient_data_list,f,sort_keys=True,indent=2)

    enough_data_list = lists[2]
    print("Enough data: "+str(len(enough_data_list)))
    with open(DATE+'/enough_data_list_'+DATE,'w') as f:
        json.dump(enough_data_list,f,sort_keys=True,indent=2)

if __name__=="__main__":
    main()
