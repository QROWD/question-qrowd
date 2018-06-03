import datamodel as dm
import configparser
import json
import requests
from datetime import datetime

def instantiate_question(trip,q_type,config):
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
    elif(q_type == "SEGMENT"):
        q_json = set_segment_template(trip,config)
    elif(q_type == "POINTS"):
        q_json = set_points_template(trip,config)
    #TODO: Defensive code aginst wrong question type

    question = dm.Question.create(
        citizen_id = trip.citizen_id,
        trip_id = trip,
        question_json = q_json,
        task_id = 0
        )
    return question

def set_segment_template(trip,config):
    #TODO: unwire this
    with open(config['templateDir']['questions']+"/segment.allmap.json") as template_f:
        q_json = json.load(template_f)
    start_date =  str(trip.start_timestamp.day) + '/' +  str(trip.start_timestamp.month)
    start_time = str(trip.start_timestamp.hour) + ':' + trip.start_timestamp.strftime('%M')
    stop_date =  str(trip.stop_timestamp.day) + '/' +  str(trip.stop_timestamp.month)
    stop_time = str(trip.stop_timestamp.hour) + ':' + trip.stop_timestamp.strftime('%M')

    trip_data = {
            'start_date': start_date ,
            'start_time': start_time ,
            'start_address': trip.start_address ,
            'stop_date': stop_date ,
            'stop_time': stop_time ,
            'stop_address': trip.stop_address ,
            }

    # First question    
    #EN
    if (trip.start_address == '' or trip.stop_address == ''):
        alter_text = "We detected that on {trip_data[start_date]} at around {trip_data[start_time]}, you made a trip approximately on the path marked on the map, arriving around {trip_data[stop_time]}. Is this correct?"
        q_json[0]['q']['p'][0]['t'] = alter_text
        alter_text = "Abbiamo rilevato che il giorno {trip_data[start_date]} dalle {trip_data[start_time]} alle {trip_data[stop_time]} hai effettuato uno spostamento, approssimativamente sul percorso sulla mappa. È corretto?"
        q_json[0]['q']['p'][1]['t'] = alter_text

    q_json[0]['q']['p'][0]['t'] = q_json[0]['q']['p'][0]['t'].format(trip_data=trip_data)
    q_json[0]['q']['p'][1]['t'] = q_json[0]['q']['p'][1]['t'].format(trip_data=trip_data) 
    #TODO: defensive code in case of null path
    json_path = json.loads(trip.path)
    lats = [point[1] for point in json_path]
    lons = [point[0] for point in json_path]

    q_json[0]['q']['la'] = lats
    q_json[0]['q']['lo'] = lons


    # Second question does not require instantiation (transport mode)
    q_json[1]['q']['la'] = lats
    q_json[1]['q']['lo'] = lons

    # Third question    

    q_json[2]['q']['p'][0]['t'] = q_json[2]['q']['p'][0]['t'].format(trip_data=trip_data)
    q_json[2]['q']['p'][1]['t'] = q_json[2]['q']['p'][1]['t'].format(trip_data=trip_data) 

    point = json.loads(trip.stop_coordinate)
    q_json[2]['q']['l']['lat'] = point[0]
    q_json[2]['q']['l']['lon'] = point[1]

    # Fourth question    

    q_json[3]['q']['la'] = lats
    q_json[3]['q']['lo'] = lons

    return q_json

def set_points_template(trip,config):
    with open(config['templateDir']['questions']+"start.stop.points.json") as template_f:
        q_json = json.load(template_f)
    start_date =  str(trip.start_timestamp.day) + '/' +  str(trip.start_timestamp.month)
    start_time = str(trip.start_timestamp.hour) + ':' + trip.start_timestamp.strftime('%M')
    stop_date =  str(trip.stop_timestamp.day) + '/' +  str(trip.stop_timestamp.month)
    stop_time = str(trip.stop_timestamp.hour) + ':' + trip.stop_timestamp.strftime('%M')

    trip_data = {
            'start_date': start_date ,
            'start_time': start_time ,
            'start_address': trip.start_address ,
            'stop_date': stop_date ,
            'stop_time': stop_time ,
            'stop_address': trip.stop_address 
            }

    # First question    
    if trip.start_address == '':
        alter_text = "We detected that on {trip_data[start_date]} at {trip_data[start_time]}, you started a trip near the point on the map below,. Is this correct?"
        q_json[0]['q']['p'][0]['t'] = alter_text
        alter_text = "Abbiamo rilevato che il giorno {trip_data[start_date]} alle {trip_data[start_time]} hai effettuato uno spostamento con punto di partenza vicino al punto sulla mappa. È corretto?"
        q_json[0]['q']['p'][1]['t'] = alter_text

    q_json[0]['q']['p'][0]['t'] = q_json[0]['q']['p'][0]['t'].format(trip_data=trip_data)
    q_json[0]['q']['p'][1]['t'] = q_json[0]['q']['p'][1]['t'].format(trip_data=trip_data) 
    #TODO: set point
    point = json.loads(trip.start_coordinate)
    q_json[0]['q']['l']['lat'] = point[0]
    q_json[0]['q']['l']['lon'] = point[1]

    # Second question 
    if trip.stop_address == '':
        alter_text = "Great!, we then detected that you traveled somewhere near the point on the map below, arriving at {trip_data[stop_time]}. Is this correct?" 
        q_json[2]['q']['p'][0]['t'] = alter_text
        alter_text = "Ottimo! Abbiamo poi rilevato che ti sei spostato/a fino al punto sulla mappa , dove sei arrivato all'ora {trip_data[stop_time]}. È corretto?"
        q_json[2]['q']['p'][1]['t'] = alter_text

    q_json[1]['q']['p'][0]['t'] = q_json[1]['q']['p'][0]['t'].format(trip_data=trip_data)
    q_json[1]['q']['p'][1]['t'] = q_json[1]['q']['p'][1]['t'].format(trip_data=trip_data) 
    point = json.loads(trip.stop_coordinate)
    q_json[1]['q']['l']['lat'] = point[0]
    q_json[1]['q']['l']['lon'] = point[1]

    # Third question does not require instantiation    
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
    dm.db.init(config['db']['dbPath'])
    
    test_trip = dm.Trip.get(trip_id=47)
    test_question = instantiate_question(test_trip,"SEGMENT",config)
    print(test_question.question_json)

    #test_question = instantiate_question(test_trip,"POINTS",config)
    #print(test_question.question_json)

    #test_question = dm.Question.get(question_id=1)
    #print(ask_question(test_question,config['ilog']))

    #q = ask_question(question,config['ilog'])


    
if __name__ == "__main__": main()
