import json
import requests
import datamodel as dm
import configparser
import re
import csv
from datetime import datetime, timedelta, date

qrowddb_tasks = "http://streambase1.disi.unitn.it:8095/gettasksbyuser"
qrowddb_answer = "http://streambase1.disi.unitn.it:8095/gettaskanswer"

# For trip detected question
def get_task_answer(user_id, task_id):
    headers = {
            'cache-control' : 'no-cache',
            'email': 'soton@soton.co.uk', 
            'password': '202c653a505f6815357bfa5d067ca5af0a742a839d764582e686d826554b52ad',
            'userid': user_id,
            'instanceid': task_id
            }
    print(headers)
    r = requests.get(qrowddb_answer, headers=headers)
    return r.json()

def get_trip_answers(date,user_id):
    qs = dm.Question.select().join(dm.Trip).where((dm.Question.citizen_id == user_id) & (dm.Trip.start_timestamp <= date) & (dm.Question.answer_json.is_null()))
    ans = [(q.task_id,get_task_answer(user_id,q.task_id)) for q in qs]
    return ans

def update_answer(answer):
    ans = answer[1]
    if ans['status'] == 'error_message':
        print(ans['status'])
        return None
    q = dm.Question.get(dm.Question.task_id == answer[0])
    q.answer_json = ans
    q.save()
    return q
    # The flow of the current answer means that all edits are in the json file


def update_answers(answers):
    updates = {'answered':0,'pending':0}
    for a in answers:
        q = update_answer(a)
        if q is None:
            updates['pending'] += 1
        else:
            updates['answered'] += 1
    return updates
    

def main():
    config = configparser.ConfigParser()
    config.read('test/test-config.ini')
    dm.db.init('test/'+config['db']['dbPath'])
    citizen = config['test']['test_citizen_id']
    instance = config['ilog']['expcode']
    ans = get_trip_answers(datetime(2019,5,21),citizen)
    update = update_answers(ans)
    print(update)


if __name__=="__main__":
    main()
