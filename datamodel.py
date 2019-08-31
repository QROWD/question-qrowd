from peewee import *

db = SqliteDatabase(None)

class Citizen(Model):
    citizen_id = CharField(primary_key=True)

    class Meta:
        database = db

class Trip(Model):
    #trip_id = IntegerField(primary_key=True)
    trip_id = PrimaryKeyField()
    citizen_id = ForeignKeyField(Citizen, backref = 'trips')
    start_coordinate = CharField()
    start_address = CharField()
    stop_coordinate = CharField()
    stop_address = CharField()
    start_timestamp = DateTimeField()
    stop_timestamp = DateTimeField()
    transportation_mode = CharField(null=True)
    segment_confidence = FloatField(null=True)
    transportation_confidence = FloatField(null=True)
    path = TextField(null=True)
    json_file_path = TextField(null=True)

    class Meta:
        database = db

class Question(Model):
    question_id = AutoField(primary_key=True)
    citizen_id = ForeignKeyField(Citizen, backref = 'questions')
    task_id = CharField()
    trip_id = ForeignKeyField(Trip, backref='trip')
    #All the JSON
    question_json = TextField()
    update_url = CharField()
    answer_file_path = TextField(null=True)
    diff_file_path = TextField(null=True)
    answer_json = TextField(null=True)
    answer_code = CharField(null=True)

    class Meta:
        database = db

class QuestionFailsafe(Model):
    question_id = AutoField(primary_key=True)
    citizen_id = ForeignKeyField(Citizen, backref = 'questions')
    task_id = CharField()
    #question_json = TextField()
    date = DateTimeField()
    file_paths = TextField(null=True)
    answer_json = TextField(null=True)

    class Meta:
        database = db

def initialize(dbname):
    db.init(dbname)
    db.connect()
    db.create_tables([Citizen,Trip,Question])
    db.close()

def main():
    db.init('')
    db.connect()
    db.create_tables([Citizen,Trip,Question])
    db.close()


if __name__ == "__main__": main()
