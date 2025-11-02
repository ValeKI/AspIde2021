from lark.exceptions import UnexpectedToken

from backend.panalysis.SimpleRegression import saveRegression
from backend.app import app
from backend.syntAnalysis.ParserASP import SentenceParsing, WEAK_CONSTRAINT, \
    VARIABLE, STATEMENT, FACT, DISJUNCTION, CONSTRAINT_RULE, CLASSICAL_RULE, AGGREGATE_FUNCTION, isCorrectSentence
from backend.timing.TimingASP import TimingASP
from flask import request, redirect, url_for
import json
import re
import time

construct = [
    WEAK_CONSTRAINT,
    VARIABLE,
    STATEMENT,
    FACT,
    DISJUNCTION,
    CONSTRAINT_RULE,
    CLASSICAL_RULE,
    AGGREGATE_FUNCTION
]

be = []
keyBe = None


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = '*'
    return response

@app.route('/')
def hello():
    return '<p>Hello, World!</p>'


@app.route('/answersets/', methods=['POST'])
def getAnswerSet():
    r = request.json
    tim = TimingASP(r['programs'], r['tests'])

    res = tim.runPrograms()
    dict = []
    for test in r['testsIndex']:
        answer = \
            {
                "index": test+1,
                "result": res[test]
            }
        dict.append(answer)

    if len(r['testsIndex']) == 0 and r['programs'] is not None:
        answer = \
            {
                "index": 0,
                "result": res[0]
            }
        dict.append(answer)

    return json.dumps({'answersets': dict})


@app.route('/correctSynt/', methods=['POST', 'GET'])
def correctSynt():
    r = request.json
    text = r['text']
    sp = isCorrectSentence(text)

    if sp is not True:
        sp = str(sp)
        regex = re.compile(r'[\n\r\t]')
        sp = regex.sub(" ", sp)

    return json.dumps(sp)


@app.route('/syntAnalysis/', methods=['POST'])
def syntAnalysis():
    r = request.json
    text = r['text']
    synt = {}
    try:
        sp = SentenceParsing(text)
        for c in construct:
            synt[c] = sp.countConstruct(c)
    except UnexpectedToken:
        for c in construct:
            synt[c] = 0
    return json.dumps(synt)


@app.route('/benchmark/', methods=['POST'])
def benchmark():
    r = request.json
    problem = r['programs']
    test = r['test']

    timBen = TimingASP()
    if 'n' in r:
        timBen.N = r['n']

    timeB = timBen.clocksNTime(problem, test)
    index = r['testIndex']
    time.sleep(1*index)

    return json.dumps({
        "index": index,
        "time": timeB
    })


@app.route('/performace/', methods=['POST'])
def performace():
    r = request.json
    benchmarks = r['benchmarks']
    facts = r['tests']

    statementFacts = []

    for fact in facts:
        synt = SentenceParsing(fact)
        statementFacts.append(synt.countConstruct(STATEMENT))

    b = []
    for benchmark in benchmarks:
        b.append(benchmark['time'])

    import random
    name = f'regression{random.randint(0, 8000)}'
    saveRegression(f'../static/{name}', statementFacts, b, 'facts statements', 'seconds')

    return json.dumps({'url': url_for('static', filename=f'{name}.png')})


if __name__ == "__main__":
     app.run(debug=True, host='0.0.0.0')
