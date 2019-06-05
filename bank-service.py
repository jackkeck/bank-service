from flask import Flask, request, abort, jsonify
from flask_restplus import Resource, Api
from flask_api import status
import emitter_thing
import json
import user_db

bank_service = Flask(__name__)
emitter_thing.setup_metrics(bank_service)

with open('config/users.json') as users_file:
    accounts = json.load(users_file)

@bank_service.route('/api/v1/login', methods=['POST'])
def login():
        json_data = request.get_json()
        username = json_data['username']
        password = json_data['password']
        user_exists = user_db.user_exists(username, password)
        if user_exists:
            content = jsonify(status="SUCCESS")
            return content
        else:
            bank_service.logger.error('Invalid login details: %s', (401))
            abort(401)

@bank_service.route('/api/v1/logout', methods=['POST'])
def logout():
        json_data = request.get_json()
        username = json_data['username']
        if user_db.user_exists(username, "doesn't matter"):
            content = jsonify(status="SUCCESS")
            return content
        else:
            bank_service.logger.error('Invalid logout details: %s', (401))
            abort(401)

@bank_service.route('/api/v1/transfer', methods=['POST'])
def transfer():
        json_data = request.get_json()
        username = json_data['username']
        toUser = json_data['toUser']
        amount = json_data['amount']
        user_exists = user_db.user_exists(username, "doesn't matter")
        toUser_exists = user_db.user_exists(toUser, "doesn't matter")
        if user_exists and toUser_exists:
            fund_transfer(username, toUser, amount)
            content = jsonify(status="SUCCESS",
                              transfer="Completed transfer of "+amount+" from "+username+" to "+toUser)
            return content
        else:
            bank_service.logger.error('Invalid logout details: %s', (401))
            abort(401)

@bank_service.route('/api/v1/account', methods=['POST'])
def account():
    json_data = request.get_json()
    username = json_data['username']
    user_exists = user_db.user_exists(username, "doesn't matter")
    if user_exists:
        return jsonify(accounts[username])
    else:
        bank_service.logger.error('Invalid logout details: %s', (401))
        abort(401)

@bank_service.route('/api/v1/help', methods=['GET'])
def help():
    return jsonify(there="is",absiolutely="no",help="lol")

def fund_transfer(username, toUser, amount):
    accounts[username]['balance'] -= int(amount)
    accounts[toUser]['balance'] += int(amount)
    accounts[username]['transactions'].append({'type': 'to', 'who': toUser, 'amount': amount})
    accounts[toUser]['transactions'].append({'type': 'from', 'who': username, 'amount': amount})

if __name__ == '__main__':
    bank_service.run(debug=True)
