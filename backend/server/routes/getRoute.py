from backend.app import app
from backend.server.routes.standardFunction import *
from flask import request, redirect, url_for, make_response


@app.route('/users/<email>', methods=['GET'])
@app.route('/users/', defaults={'email': None}, methods=['GET'])
def user(email):
    if email is None:
        email = request.args.get('email')
    passw = request.args.get('cryptPass')
    if passw is not None and email is not None:
        if dbm.isCorrectPassword(email, passw):
            return 'correct'
        else:
            return 'no correct'
    elif passw is None and email is not None:
        users = dbm.userByEmail(email)
        if len(users) > 0:
            return json.dumps({'user': [u.serialize() for u in users]})
    return json.dumps({'user': []})


@app.route('/competitions/<keyId>', methods=['GET'])
@app.route('/competitions/', defaults={'keyId': None}, methods=['GET'])
def competitions(keyId):
    return classicGetRoute(
        ['key', 'nameGroup', 'idSolution', 'idTest'],
        [dbm.competitionById, dbm.competitionByNameGroup, dbm.competitionByIdSolution, dbm.competitionByIdTest],
        dbm.allCompetitions,
        'competitions',
        keyId)


@app.route('/groups/<key>', methods=['GET'])
@app.route('/groups/', defaults={'key': None}, methods=['GET'])
def group(key=None):
    if key is None:
        key = request.args.get('nameGroup')
    return classicGetRoute(
        ['key', 'idCompetition', 'idSolution', 'idCompetition'],
        [dbm.groupByName, dbm.groupByIdCompetition, dbm.groupByIdSolution, dbm.groupByIdCompetition],
        dbm.allGroups,
        'groups',
        key
    )


@app.route('/problems/<key>', methods=['GET'])
@app.route('/problems/', defaults={'key': None}, methods=['GET'])
def problems(key):
    return classicGetRoute(
        ['key', 'idCompetition', 'name', 'idSolution', 'idTest'],
        [dbm.problemByKey, dbm.problemByIdCompetition, dbm.problemByName, dbm.problemByIdTest, dbm.problemByIdTest],
        dbm.allProblems,
        'problems',
        key
    )


@app.route('/solutions/<key>', methods=['GET'])
@app.route('/solutions/', defaults={'key': None}, methods=['GET'])
def solutions(key):
    nameP = request.args.get('nameProblem')
    idComp = request.args.get('idCompetition')

    if nameP is not None and idComp is not None:
        list = dbm.solutionByNameProblemAndIdComp(nameP, idComp)
        return json.dumps({'solutions': [o.serialize() for o in list]})

    return classicGetRoute(
        ['key', 'nameGroup', 'nameProblem', 'idCompetition', 'keyProblem'],
        [dbm.solutionById, dbm.solutionByNameGroup, dbm.solutionByNameProblem,
            dbm.solutionByIdComp, dbm.solutionByKeyProblem],
        dbm.allSolutions,
        'solutions',
        key
    )


@app.route('/tests/<key>', methods=['GET'])
@app.route('/tests/', defaults={'key': None}, methods=['GET'])
def testCase(key):
    return classicGetRoute(
        ['key', 'problemName', 'idCompetition', 'keyProblem'],
        [dbm.testCaseById, dbm.testCaseByNameProblem, dbm.testCaseByIdCompetition, dbm.testCaseByKeyProblem],
        dbm.allTestCases,
        'tests',
        key
    )


@app.route('/people/<key>', methods=['GET'])
@app.route('/people/',  defaults={'key': None}, methods=['GET'])
def person(key):
    if key is not None and not key.isnumeric():
        list = dbm.personByNameGroup(key)
        return json.dumps({'people': [obj.serialize() for obj in list]})
    return classicGetRoute(
        ['key', 'nameGroup', 'idSolution'],
        [dbm.personById, dbm.personByNameGroup, dbm.peopleByIdSolution],
        dbm.allPeople,
        'people',
        key
    )


@app.route('/predictions/<key>', methods=['GET'])
@app.route('/predictions/', defaults={'key': None}, methods=['GET'])
def predictions(key):
    return classicGetRoute(
        ['key', 'idCompetition'],
        [dbm.pananalysisById, dbm.pananalysisByIdSolution],
        None,
        'predictions',
        key
    )


@app.route('/sanalysis/<key>', methods=['GET'])
@app.route('/sanalysis/', defaults={'key': None}, methods=['GET'])
def syntacticAnalysis(key):
    # list = listGetRoute(
    #     ['key', 'idSolution', 'idTest'],
    #     [dbm.sanalysisById, dbm.sanalysisByIdSolution, dbm.sanalysisByIdTest],
    #     None,
    #     'sanalysis',
    #     key
    # )
    #
    idProgram = request.args.get('idSolution') \
        if request.args.get('idSolution') is not None else request.args.get('idTest')

    isTest = request.args.get('idTest') is not None

    if idProgram is not None:
        return json.dumps({'sanalysis': [dbm.dictonarySAnalysis(idProgram, isTest)]})

    return make_response('sanalysis', 404)


@app.route('/text/<name>', methods=['GET'])
@app.route('/text/', defaults={'name': None}, methods=['GET'])
def text(name):
    if name is None:
        return make_response('Not found', 404)
    return redirect(url_for('static', filename='text/' + name), code=301)


@app.route('/textsolutions/<key>', methods=['GET'])
@app.route('/textsolutions/', defaults={'key': None}, methods=['GET'])
def textsolutions(key):
    name = dbm.solutionById(key)[0].text
    return redirect(url_for('static', filename='text/' + name), code=301)


@app.route('/texttestcase/<key>', methods=['GET'])
def texttestcase(key):
    name = dbm.testCaseById(key)[0].text
    return redirect(url_for('static', filename='text/' + name), code=301)


@app.route('/images/<name>', methods=['GET'])
def image(name):
    return redirect(url_for('static', filename='images/' + name), code=301)


@app.route('/logoCompetition/<key>', methods=['GET'])
@app.route('/logoCompetition/', defaults={'key': None}, methods=['GET'])
def logo(key):
    if key is None:
        name = 'default.png'
    else:
        name = dbm.competitionById(key)[0]
        if name.logo is None:
            name = 'default.png'
        else:
            name = name.logo
    return redirect(url_for('static', filename='images/' + name), code=301)
