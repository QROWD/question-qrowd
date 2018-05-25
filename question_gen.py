import datamodel as dm
import configparser
import json
import requests
from datetime import datetime

def instantiate_question(trip,q_type,q_template="question-templates/stop.points.json"):
    """
    Take a trip and ask a question of q_type by instantiating a q_template
    Assumption: q_type and q_template match
    """
    #TODO: Depending on q_type, choose template
    if(q_type == "Stop_point"):
        with open(q_template) as template_f:
            q_json = json.load(template_f)
        q_json = set_stop_coordinates(q_json,trip)
        q_json = set_stop_question(q_json,trip)
    elif(q_type == "Trip"):
        q_json = set_segment_template(trip)
    question = dm.Question.create(
        citizen_id = trip.citizen_id,
        trip_id = trip,
        question_json = q_json,
        task_id = 0
        )
    return question

def set_segment_template(trip):
    #TODO: unwire this
    with open("question-templates/segment.json") as template_f:
        q_json = json.load(template_f)
    # Set stop address
    dt = trip.start_timestamp.strftime("%d-%m at %H:%M")
    q_json[0]['q']['p'][0]['t'] = q_json[0]['q']['p'][0]['t'].format(start_address=trip.start_address, start_datetime = dt,stop_address = trip.stop_address)
    q_json[0]['q']['p'][1]['t'] = q_json[0]['q']['p'][1]['t'].format(start_address=trip.start_address, start_datetime = dt,stop_address = trip.stop_address) 
    return q_json


def set_stop_coordinates(q_json,trip):
    point = json.loads(trip.stop_coordinate)
    q_json[0]['q']['l']['lat'] = point[1]
    q_json[0]['q']['l']['lon'] = point[0]
    return q_json

def set_stop_question(q_json,trip):
    dt = trip.stop_timestamp.strftime("%d-%m at %H:%M")
    q_json[0]['q']['p'][0]['t'] = q_json[0]['q']['p'][0]['t'].format(stop_time = dt,stop_address = trip.stop_address)
    q_json[0]['q']['p'][1]['t'] = q_json[0]['q']['p'][1]['t'].format(stop_time = dt,stop_address = trip.stop_address)
    return q_json

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
            'usersalt': question.citizen_id 
            }
    r = requests.get(config['serverURL']+'/user/newtask',headers=headers).json()
    query = dm.Question.update(task_id = r["taskid"])
    query.execute()
    return r

def get_answer(question,config):
    headers = {
            'cache-control' : 'no-cache' ,
            'email': config['serverlogin'] , 
            'password': config['serverpassword'] ,
            'postman-token': config['postman-token'] , 
            'taskid': question.task_id,
            'userid': question.citizen_id
            }
    r = requests.get(config['serverURL']+'/user/gettaskanswer', headers=headers)
    #TODO: Defensive code
    print(r.text)
    return r.json()



def main():
    config = configparser.ConfigParser()
    config.read('question-config.ini')
    
    test_trip = dm.Trip.get(trip_id=1)
    test_question = instantiate_question(test_trip,"Trip")
    #print(test_question)

    #test_question = dm.Question.get(question_id=1)
    print(ask_question(test_question,config['ilog']))

    #q = ask_question(question,config['ilog'])


    
if __name__ == "__main__": main()
