__author__ = 'Andrzej Skrodzki 292510'

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.collection import *
import datetime


def main():
    client = None
    try:
        client = MongoClient('mongodb://as292510:test1234@ds027699.mongolab.com:27699/zbd2013')
    except ConnectionFailure:
        print "Connection to database failed."
        exit()
    print "Login succeseed"
    createDatabase(client["zbd2013"])
    exit()


def createDatabase(db):
    assert(db is not None)
    print "Database creation started."
    teamId = createTeam(db)
    playerId = createPlayer(db, teamId)
    matchId = createMatch(db, teamId)
    pointId = createPoint(db, matchId)
    createSquad(db, pointId, playerId)
    createInjury(db, playerId)
    createTrainer(db, teamId)
    print "Database creation finished successfully."
    return


def createTrainer(db, teamId):
    id = ObjectId()
    trainer_col = db.Trainer
    trainer_col.insert({
        "_id": id,
        "Name": "Jan",
        "Surname": "Kowalski",
        "Start_time": str(datetime.date(2013, 2, 3)),
        "End_time": str(datetime.date(2013, 2, 3)),
        "Team_id": teamId
    })


def createInjury(db, playerId):
    id = ObjectId()
    injury_col = db.Injury
    injury_col.insert({
        "_id": id,
        "Player_id": playerId,
        "Start_date": str(datetime.datetime.now()),
        "End_date": str(datetime.datetime.now())
    })
    return id


def createSquad(db, pointId, playerId):
    id = ObjectId()
    squad_col = db.Squad
    squad_col.insert({
        "_id" : id,
        "Player_id": playerId,
        "Point_id": pointId,
        "Position": 1
    })
    return id


def createTeam(db):
    id = ObjectId()
    team_col = db.Teams
    team_col.insert({
        "Name": "Polska",
        "_id": id
    })
    return id
    pass


def createPlayer(db, teamId):
    id = ObjectId()
    player_col = db.Player
    player_col.insert({
        "_id": id,
        "Name": "Jan",
        "Surname": "Kowalski",
        "Birth": str(datetime.date(1990, 07, 14)),
        "Team_id": teamId
    })
    return id


def createMatch(db, opponent):
    id = ObjectId()
    match_col = db.Match
    match_col.insert({
        "_id": id,
        "Team_id": opponent,
        "Won": 1,
        "Date": str(datetime.datetime.today()),
    })
    return id


def createPoint(db, match):
    id = ObjectId()
    point_col = db.Point
    point_col.insert({
        "_id": id,
        "Score": 1,
        "Serve": 110.2,
        "Match_id": match
    })
    return id


if __name__ == "__main__":
    main()
