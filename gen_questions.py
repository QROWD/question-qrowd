import datamodel as dm
import json
from datetime import datetime
from collections import OrderedDict

def set_trip_data(trip):
    start_date =  str(trip.start_timestamp.day) + '/' +  str(trip.start_timestamp.month)
    start_time = str(trip.start_timestamp.hour) + ':' + trip.start_timestamp.strftime('%M')
    stop_date =  str(trip.stop_timestamp.day) + '/' +  str(trip.stop_timestamp.month)
    stop_time = str(trip.stop_timestamp.hour) + ':' + trip.stop_timestamp.strftime('%M')
    seen = set()
    path = json.loads(trip.path)
    print (len(path))
    uni_path = [x for x in path if tuple(x) not in seen and not seen.add(tuple(x)) ]
    print (len(uni_path))
    trip_data = {
            'start_date': start_date ,
            'start_time': start_time ,
            'start_address': trip.start_address ,
            'stop_date': stop_date ,
            'stop_time': stop_time ,
            'stop_address': trip.stop_address, 
            'path': uni_path,
            'json_file_path': trip.json_file_path
    }
    return trip_data

def set_study_template(test_trip):
    with open("study-question.json") as template_f:
        q_json = json.load(template_f)

    trip_data = set_trip_data(test_trip)

    # 1st question is a web view, then the second is a segment type
    alter_text = "We detected that on {trip_data[start_date]} at around {trip_data[start_time]}, you made a trip approximately on the path marked on the map, arriving around {trip_data[stop_time]}. Is this correct?"
    q_json[1]['q']['p'][1]['t'] = alter_text
    alter_text = "Abbiamo rilevato che il giorno {trip_data[start_date]} dalle {trip_data[start_time]} alle {trip_data[stop_time]} hai effettuato uno spostamento, approssimativamente sul percorso sulla mappa. È corretto?"
    q_json[1]['q']['p'][1]['t'] = alter_text
    q_json[1]['q']['p'][0]['t'] = q_json[1]['q']['p'][0]['t'].format(trip_data=trip_data)
    q_json[1]['q']['p'][1]['t'] = q_json[1]['q']['p'][1]['t'].format(trip_data=trip_data) 

    # Creating path for segment type question
    lats = [point[1] for point in trip_data['path']]
    lons = [point[0] for point in trip_data['path']]
    q_json[1]['q']['la'] = lats
    q_json[1]['q']['lo'] = lons

    # Third question is contextual. No instantiation.
    pass

    # fourth question is instructional, fifth is the update interface
    q_json[4]['q']['url'] = q_json[4]['q']['url'].format(trip_data=trip_data)

    # Questions 4-6 are contextual, no need to instantiate 
    pass

    return q_json

def set_template(trip):
    with open("web-view.json") as template_f:
        q_json = json.load(template_f)

    trip_data = set_trip_data(trip)
    
    # 1st question is a segment type
    alter_text = "We detected that on {trip_data[start_date]} at around {trip_data[start_time]}, you made a trip approximately on the path marked on the map, arriving around {trip_data[stop_time]}. Is this correct?"
    q_json[0]['q']['p'][0]['t'] = alter_text
    alter_text = "Abbiamo rilevato che il giorno {trip_data[start_date]} dalle {trip_data[start_time]} alle {trip_data[stop_time]} hai effettuato uno spostamento, approssimativamente sul percorso sulla mappa. È corretto?"
    q_json[0]['q']['p'][1]['t'] = alter_text
    q_json[0]['q']['p'][0]['t'] = q_json[0]['q']['p'][0]['t'].format(trip_data=trip_data)
    q_json[0]['q']['p'][1]['t'] = q_json[0]['q']['p'][1]['t'].format(trip_data=trip_data) 

    # Creating path for segment type question
    lats = [point[1] for point in trip_data['path']]
    lons = [point[0] for point in trip_data['path']]
    q_json[0]['q']['la'] = lats
    q_json[0]['q']['lo'] = lons

    # Second question is contextual. No instantiation.
    pass

    # third question is the web-view
    q_json[2]['q']['url'] = q_json[2]['q']['url'].format(trip_data=trip_data)

    # Questions 4-6 are contextual, no need to instantiate 
    pass

    return q_json

#
#  DB access with peewee (there is new model)

# For each user
# For each trip of the day
# Instantiate question (should be hackable from previous code)
# Send question
