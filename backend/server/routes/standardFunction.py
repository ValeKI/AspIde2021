from flask import request, make_response
from ..database.dbmanager import DBManager
import json

dbm = DBManager()


def listGetRoute(names: list, functions: list, allfunction, nameAll, keyValue):
    if len(names) != len(functions):
        return None
    vrb = []
    list = []

    if keyValue is None and allfunction is not None and len(request.args) == 0:
        list = allfunction()

    if keyValue is not None and len(list) == 0:
        list = functions[0](keyValue)
    elif len(request.args) > 0:
        for i in range(0, len(names)):
            v = request.args.get(names[i])
            vrb.append(v)
            if v is not None:
                list = functions[i](v)
            if len(list) > 0:
                break

    return list


def classicGetRoute(names: list, functions: list, allfunction, nameAll, keyValue):
    list = listGetRoute(names, functions, allfunction, nameAll, keyValue)

    if len(list) > 0:
        return json.dumps({nameAll: [o.serialize() for o in list]})

    return make_response(nameAll, 404)