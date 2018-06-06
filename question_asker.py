import json
import configparser
import requests
from datetime import datetime
import datamodel as dm
import question_gen as qg

def ask_question(question,config):
    headers = {
            'cache-control' : 'no-cache' ,
            'content' : json.dumps(question.question_json) ,
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' ,
            'email': config['serverlogin'] , 
            'password': config['serverpassword'] ,
            'postman-token': config['postman-token'] , 
            't_title': 'Task' ,
            't_until': '864000' ,
            'usersalt': question.citizen_id.citizen_id 
     
    }
    r = requests.get(config['serverURL']+'/user/newtask',headers=headers).json()
    question.task_id = r['taskid']
    question.save()
    return r

def check_data_for_date(config,date=datetime.today().date()):
    #TODO: support array of dates
    print("Checking data for date "+ str(date))
    headers = {
            'cache-control' : 'no-cache' ,
            'email': config['serverlogin'] , 
            'password': config['serverpassword'] ,
            'dates': '{ "dates": ["' + date.strftime('%Y%m%d') + '"]}' 
            }
    r = requests.get(config['dataURL']+'/checkuserdata', headers=headers)
    return r.json()

def location_average(daily_data,hours=24):
    """Receives daily data in format returned by iLog
    returns average location use
    """
    location = [record['presence'] for record in daily_data if record['tablename'] == 'locationeventpertime']
    location_array = location[0]
    return sum(location_array)/hours

def is_collected_location_enough(daily_data,hours=24):
    average = location_average(daily_data,hours)
    return average >= 1

def is_collected_accelerometer_enough(daily_data,hours=24):
    average = accelerometer_average(daily_data,hours)
    return average >= 1

def accelerometer_average(daily_data,hours=24):
    """Receives daily data in format returned by iLog
    returns average location use
    """
    accelerometer = [record['presence'] for record in daily_data if record['tablename'] == 'accelerometerevent']
    accelerometer_array = accelerometer[0]
    return sum(accelerometer_array)/hours

def send_machine_failure_message():
    print("TBI")

def send_accelerometer_failure_message():
    print("TBI")

def send_location_failure_message():
    print("TBI")

def send_whole_failure_message():
    print("TBI")

def send_message(citizen,message,config):
    """ When no new trips have been detected, send a warning message
        Either there was a machine issue or there was a collection issue
    """

    """ Messages did not work as expected, so reverted this functionality to a task
    headers = {
            'cache-control' : 'no-cache' ,
            'email': config['serverlogin'] , 
            'password': config['serverpassword'] ,
            't_title': 'Test message' , 
            't_until': '86400' , 
            'content': json.dumps(message.message_json) , 
            'usersalt': citizen.citizen_id
            }
    r = requests.get(config['serverURL']+'/user/newmessage',headers=headers).json()
    return r
    """ 
    headers = {
            'cache-control' : 'no-cache' ,
            'content' : json.dumps(message.message_json) ,
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' ,
            'email': config['serverlogin'] , 
            'password': config['serverpassword'] ,
            'postman-token': config['postman-token'] , 
            't_title': 'Task' ,
            't_until': '864000' ,
            'usersalt': citizen.citizen_id 
     
    }
    r = requests.get(config['serverURL']+'/user/newtask',headers=headers).json()
    message.task_id = r['taskid']
    message.save()
    print(r)
    return r


def instantiate_message(citizen,citizen_data,config):
    #TODO: The value of hours 10 is wired from the collection
    message = None
    if (citizen.collection_mode == "CONTINUOUS"):
        # Enough location collected, machine failure or citizen did not move
        if (is_collected_location_enough(citizen_data,10)):
            print ("Enough collection, sending machine failure message")
            with open(config['templateDir']['messages']+"/machine.failure.message.json") as template_f:
                m_json = json.load(template_f)
            message = dm.Message.create( citizen_id = citizen.citizen_id, message_json = m_json, message_type = 'MACHINEFAILURE', task_id= 0)
        #Something happened with location
        else:
            print ("Location failure, sending collection failure message")
            with open(config['templateDir']['messages']+"collection.failure.message.json") as template_f:
                m_json = json.load(template_f)
            message = dm.Message.create(citizen_id = citizen.citizen_id, message_json = m_json, message_type = 'COLLECTIONFAILURE', task_id= 0)
    elif (citizen.collection_mode == "ON-OFF"):
        #TODO: The value of 2 is wired from the reward
        if (is_collected_location_enough(citizen_data,2)):
            print ("Enough collection, sending machine failure message")
            with open(config['templateDir']['messages']+"machine.failure.message.json") as template_f:
                m_json = json.load(template_f)
            message = dm.Message.create(citizen_id = citizen.citizen_id, message_json = m_json, message_type = 'MACHINEFAILURE', task_id= 0)
        #Something happened with location
        else:
            print ("Location collection failure, sending collection failure")
            with open(config['templateDir']['messages']+"onoff.failure.message.json") as template_f:
                m_json = json.load(template_f)
            message = dm.Message.create( citizen_id = citizen.citizen_id, message_json = m_json, message_type = 'COLLECTIONFAILURE', task_id= 0)
    else:
        print("Unknown collection mode, stopping now")
        raise NameError('Unknown collection mode '+ citizen.collection_mode)
    return message

def process_citizen(citizen,daily_log_stats,config):
    print(citizen.citizen_id)
    citizen_data = [data['days'][0]['tables'] for data in daily_log_stats if data['userid'] == citizen.citizen_id ]
    citizen_data = citizen_data[0]
    # Trips for which no question has been asked
    # TODO: Might be cases where a question was instantiated but not yet asked
    new_trips = [trip for trip in citizen.trips if len(trip.questions) == 0]
    
    # If no trips detected, send warning message 
    if len(new_trips) == 0 :
        print ("No new trips for citizen "+ str(citizen.citizen_id))
        print ("Instantiating relevant message...")
        message = instantiate_message(citizen,citizen_data,config)
        print ("Sending message...")
        send_message(citizen,message,config['iLog'])

    for trip in new_trips:
        try:
            #TODO: Change to proper logging
            print ("Asking question to citizen "+ str(citizen.citizen_id))
            print ("referring trip " + str(trip.trip_id))
            print ("question type "+ citizen.question_preference)
            if citizen.question_preference == 'SEGMENT':
                question = qg.instantiate_question(trip,'SEGMENT',config)
                response = ask_question(question,config['iLog'])
                print ("Response: " + str(response))
            elif citizen.question_preference == 'POINTS':
                question = qg.instantiate_question(trip,'POINTS',config)
                response = ask_question(question,config['iLog'])
                print ("Response: " + str(response))
               #TODO: Add exception to delete instantiated question if server issue 
            else:
                #TODO: Change to exception
                print ("ERROR: Unknown question type")
        except:
            print("error sending question")

def process_questions(config):

    print ("Processing questions...")
    print ("Computing collected data average...")
    daily_log_stats = check_data_for_date(config['iLog'])

    for citizen in dm.Citizen.select():
        process_citizen(citizen,daily_log_stats,config)

def main():
    config = configparser.ConfigParser()
    config.read('question-config.ini')
    dm.db.init(config['db']['dbPath'])
    process_questions(config)
    #r = check_data_for_dates(config['iLog'],datetime(2018,4,12),datetime(2018,4,12))
    #r = check_data_for_date(config['iLog'])
    #print(r.text)
     

if __name__ == "__main__": main()
