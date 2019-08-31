import json
import configparser
import requests
from datetime import datetime, timedelta, date
import datamodel as dm
import gen_questions as gq
import gen_lists as gl

#DATE=datetime(2019,3,16)
TEST = False 

def ask_question(question,config):
    headers = {
            'cache-control' : 'no-cache' ,
            'email': config['ilog']['serverlogin'] , 
            'password': config['ilog']['serverpassword'] ,
            't_title': 'Domanda di conferma QROWDLab' , 
            't_until': '86400' , 
            #'t_until': '864000' , 
            'content': json.dumps(question.question_json),
            'usersalt': question.citizen_id.citizen_id
            }
    r = requests.get(config['ilog']['serverURL']+'/sendtask',headers=headers).json()
    if (r['status'] == 'error_message'):
        print(r['payload']['results'])
        return None
    question.task_id = r['payload']['message']
    question.save()
    return r

def ask_failsafe_question(config,citizen,date):
    template_path = config['templateDir']['questions']+"no-trip-detected-question-alt.json"
    failsafe = gq.gen_failsafe_question(template_path,'/journeys/ql6/test_trips',citizen,date)
    headers = {
            'cache-control' : 'no-cache' ,
            'email': config['ilog']['serverlogin'] , 
            'password': config['ilog']['serverpassword'] ,
            't_title': 'Domanda di conferma QROWDLab' , 
            #'t_until': '864000' , 
            't_until': '86400' , 
            'content': json.dumps(failsafe),
            'usersalt': citizen.citizen_id
            }
    r = requests.get(config['ilog']['serverURL']+'/sendtask',headers=headers).json()
    print(r)
    if (r['status'] == 'error_message'):
        print(r['payload']['results'])
        return None
    question = dm.QuestionFailsafe.create(
        citizen_id = citizen.citizen_id,
        task_id = r['payload']['message'],
        date = date
        )
    question.save()
    return r

def ask_missing_question(config,citizen,date):
    template_path = config['templateDir']['questions']+"missing-trip-question.json"
    missing = gq.gen_missing_question(template_path,'/journeys/ql6/test_trips',citizen,date)
    headers = {
            'cache-control' : 'no-cache' ,
            'email': config['ilog']['serverlogin'] , 
            'password': config['ilog']['serverpassword'] ,
            't_title': 'Domanda di conferma QROWDLab' , 
            #'t_until': '864000' , 
            't_until': '86400' , 
            'content': json.dumps(missing),
            'usersalt': citizen.citizen_id
            }
    r = requests.get(config['ilog']['serverURL']+'/sendtask',headers=headers).json()
    if (r['status'] == 'error_message'):
        print(r['payload']['results'])
        return None
    question = dm.QuestionFailsafe.create(
        citizen_id = citizen.citizen_id,
        task_id = r['payload']['message'],
        date_sent = date
        )
    question.save()

def create_db_question(config,trip):
    #template_path = config['templateDir']['questions']+"trip-detected-question.json"
    template_path = config['templateDir']['questions']+"trip-detected-question-alt.json"
    tui_url = config['tui']['tui_url']
    #q_json = gq.gen_trip_question(template_path,tui_url,trip)
    q_json = gq.gen_trip_question_alt(template_path,tui_url,trip)
    question = dm.Question.create(
        citizen_id = trip.citizen_id,
        trip_id = trip.trip_id,
        question_json = q_json,
    #    update_url = q_json[4]['q']['url'],
        update_url = q_json[1]['q']['url'],
        task_id = 0
        )
    return question

def create_test_question(trip):
    q_json = gq.set_test_template(trip)
    question = dm.Question.create(
        citizen_id = trip.citizen_id,
        trip_id = trip.trip_id,
        question_json = q_json,
        update_url = q_json[4]['q']['url'],
        task_id = 0
        )
    return question

def ask_practice_question(config,citizen):
    with open(config['templateDir']['questions']+"practice-question.json") as template_f:
        q_json = json.load(template_f)
    
    q_json[2]['q']['url'] = q_json[2]['q']['url'].format(citizen.citizen_id)
    q_json[5]['q']['url'] = q_json[5]['q']['url'].format(citizen.citizen_id)
    print("Linking to confirm ", q_json[2]['q']['url'])
    print("Linking to blank answer ", q_json[5]['q']['url'])
    headers = {
            'cache-control' : 'no-cache' ,
            'email': config['ilog']['serverlogin'] , 
            'password': config['ilog']['serverpassword'] ,
            't_title': 'QROWDLab6 TEST QUESTION' , 
            't_until': '86400' , 
            'content': json.dumps(q_json),
            'usersalt': citizen.citizen_id
            }
    r = requests.get(config['ilog']['serverURL']+'/sendtask',headers=headers).json()
    if (r['status'] == 'error_message'):
        print(r)
        #print(r['payload']['results'])
        return None
    return r

def send_message(config,citizen,message):
    headers = {
            'cache-control' : 'no-cache' ,
            'email': 'soton@soton.co.uk' , 
            'email': config['ilog']['serverlogin'] , 
            'password': config['ilog']['serverpassword'] ,
            't_until': '864000' , 
            'content': json.dumps(message),
            'usersalt': citizen.citizen_id
            }
    r = requests.get(config['iLog']['serverURL']+'/sendtask',headers=headers).json()
    if (r['status'] == 'error_message'):
        print(r['payload']['results'])
        return None
    return r['payload']['message']

def send_error_message(config):
    users_data = gl.checkusersdata(dates={"dates": [DATE.strftime('%Y%m%d')]},project=config['ilog']['expcode'])
    (no_data,insuf,enough) = gl.gen_data_lists(users_data)
    for citizen in dm.Citizen.select():
        today_trips = dm.Trip.select().where((dm.Trip.citizen_id == citizen.citizen_id) & (dm.Trip.start_timestamp.between(DATE,DATE+timedelta(days=1))))
        q_json = ""
        if len(today_trips) == 0: 
            print("No trips for citizen {}".format(citizen.citizen_id))
            print("Sending error message...")
            if citizen.citizen_id in [c['userid'] for c in no_data]:
                with open("collection.failure.message.json") as template_f:
                    q_json = json.load(template_f)
                print("No data - Sending Collection Failure data")
            elif citizen.citizen_id in [c['userid'] for c in insuf]:
                with open("collection.failure.message.json") as template_f:
                    q_json = json.load(template_f)
                print("Insufficient data - Sending Collection Failure data")
            elif citizen.citizen_id in [c['userid'] for c in enough]:
                with open("machine.failure.message.json") as template_f:
                    q_json = json.load(template_f)
                print("Enough data - Sending Machine Failure data")
            else:
                print("Unknown user - Probably test")
                if citizen.citizen_id == config['test']['test_citizen_id']: 
                    with open("machine.failure.message.json") as template_f:
                        q_json = json.load(template_f)

            return send_message(config,citizen,q_json)

def process_citizen(config,citizen,date):
    #Today trips of this citizen
    trips = dm.Trip.select().where((dm.Trip.citizen_id == citizen.citizen_id) & (dm.Trip.start_timestamp.between(date,date+timedelta(days=1))))
    print("Processing citizen "+ str(citizen.citizen_id))
    for trip in trips:
        print("Trip_id "+ str(trip.trip_id))
        question = create_db_question(config,trip)
        resp = ask_question(question,config)
        if resp is None:
            print("Error: See above")
        else: 
            print("Question sent")
    if len(trips) == 0:
        print("No trips detected this date, sending failsafe question")
        ask_failsafe_question(config,citizen,date)
    else:
        print("Sending missing trips question")
        ask_missing_question(config,citizen,date)


def main():
    #DATE = (datetime.today()-timedelta(days=1)).replace(hour=0,minute=0,second=0,microsecond=0)
    DATE=datetime(2019,5,21)
    config = configparser.ConfigParser()
    config.read('./ql6-config.ini')
    dm.db.init(config['db']['dbPath'])
    citizens = dm.Citizen.select()
    if TEST:
        print("Sending Test question")
        for citizen in citizens:
            print("citizen_id ",citizen.citizen_id)
            r = ask_practice_question(config,citizen)
            print(r.text)
    else:
        #Today's trips
        print("Processing trips of date "+ DATE.strftime("%Y%m%d"))
        for citizen in citizens:
            process_citizen(config,citizen,DATE)


if __name__=="__main__":
    main()



