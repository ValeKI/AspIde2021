from backend.app import app
from backend.server.routes.standardFunction import *
from flask import request, make_response


def checkUser():
    email = request.form['email']
    nickname = request.form['nickname']
    password = request.form['password']

    if password is None:
        return False

    if email is None and nickname is None:
        return False

    return dbm.isCorrectPassword(email, password) if email is not None else dbm.isCorrectPasswordByNickname(nickname, password)


@app.route('/users/', methods=['POST'])
def userPost():
    email = request.form['email']
    nickname = request.form['nickname']
    password = request.form['password']
    moderator = request.form['moderator']
    if moderator is None:
        moderator = False
    if email is None or nickname is None or password is None:
        return make_response('bad request', 400)
    dbm.addUser(email, nickname, password, moderator)


@app.route('/request/', methods=['POST'])
def requestPost():
    email = request.form['email']
    text = request.form['text']
    r = None
    if request is not None and text is not None:
        r = dbm.addRequest(email, text)
    return r if r is not None else make_response('bad request', 400)


@app.route('/requestOutcome/', methods=['POST'])
def outcomeRequest():
    if not checkUser():
        return make_response('bad request', 400)
    outcome = request.form['outcome']
