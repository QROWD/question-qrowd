import json
import configparser
import requests
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
    query = dm.Question.update(task_id = r["taskid"])
    query.execute()
    return r

def main():
    config = configparser.ConfigParser()
    config.read('question-config.ini')
    #For each citizen
    for citizen in dm.Citizen.select():
        print(citizen.citizen_id)
        # Trips for which no question has been asked
        # TODO: Might be cases where a question was instantiated but not yet asked
        new_trips = [trip for trip in citizen.trips if len(trip.questions) == 0]
        for trip in new_trips:
            #TODO: Change to proper logging
            print ("Asking question to citizen "+ str(trip.citizen_id))
            print ("referring trip " + str(trip.trip_id))
            print ("question type "+ citizen.question_preference)
            if citizen.question_preference == 'SEGMENT':
                question = qg.instantiate_question(trip,'SEGMENT')
                response = ask_question(question,config['iLog'])
                print ("Response: " + response)
            elif citizen.question_preference == 'POINTS':
                question = qg.instantiate_question(trip,'POINTS')
                response = ask_question(question,config['iLog'])
                print ("Response: " + response.text)
                #TODO: Add exception to delete instantiated question if server issue 
            else:
                #TODO: Change to exception
                print ("ERROR: Unknown question type")

        #for trip in citizen.trips.where(dm.Trip.stop_address == 'Via Berlin'):
        #    print(trip.stop_address)
        #new_trips = [trip for dm.Trip.select().where()]
    # if no new trips detected
    # If data issues:
        # Send data problem message
    # If machine issue
        # Send explicative message
    #for new trip detected
        # For each new trip 
        # Ask question regarding trip, depending on type
     

if __name__ == "__main__": main()
