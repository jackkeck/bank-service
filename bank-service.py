from flask import Flask, request, abort, jsonify
from flask_restplus import Api, Resource, fields
from flask_api import status
import json
import traceback
import time
from time import strftime
from datetime import datetime
import logging
import sys
import uuid
import structlog

import user_db

logger = structlog.get_logger()
bank_service = Flask(__name__)
api = Api(bank_service, version='1.0', title='Bank Service API', description='A Sample Banking API')
#emitter_thing.setup_metrics(bank_service)

with open('config/users.json') as users_file:
    accounts = json.load(users_file)

@api.route('/api/v1/login', methods=['POST'])
@api.doc(params={'username': 'A username for logging in', 'password': 'because lulz'})
class Login(Resource):
    def post(self):
        log = logger.new(request_id=str(uuid.uuid4()))
        json_data = request.get_json()
        username = json_data['username']
        password = json_data['password']

        start_time = start_timer()
        user_exists = user_db.user_exists(username, password)
        resp_time = stop_timer(start_time)
        logger.info(ts=timestamp(),host=request.remote_addr,path=request.full_path, function="user_db.user_exists()", resp_time=resp_time)

        if username == "throw_error":
            logger.error(ts=timestamp(),host=request.remote_addr,path=request.full_path,status=500, username=username, msg="SERVICE_UNAVAILABLE")
            print ("THIS IS  THROWN ON PURPOSE BECAUSE USER IS: %s", username)
            abort(500)
        if user_exists:
            logger.info(ts=timestamp(),host=request.remote_addr,path=request.full_path,status=200, username=username, msg="LOGIN_SUCCESS")
            contents = jsonify(status="SUCCESS")
            return contents
        else:
            logger.error(ts=timestamp(),host=request.remote_addr, path=request.full_path, status=401, username=username, msg="INVALID_LOGIN")
            abort(401)

@api.route('/api/v1/logout', methods=['POST'])
@api.doc(params={'username': 'A username for logging in'})
class Logout(Resource):
    def post(self):
        json_data = request.get_json()
        username = json_data['username']

        start_time = start_timer()
        user_exists = user_db.user_exists(username, "doesn't matter")
        resp_time = stop_timer(start_time)
        logger.info(ts=timestamp(),host=request.remote_addr,path=request.full_path, function="user_db.user_exists()", resp_time=resp_time)

        if user_exists:
            logger.info(ts=timestamp(),host=request.remote_addr, path=request.full_path, status=200, username=username, msg="SUCCESS")
            contents = jsonify(status="SUCCESS")
            return contents
        else:
            logger.error(ts=timestamp(),host=request.remote_addr, path=request.full_path, status=401, username=username, msg="INVALID_LOGOUT")
            abort(401)

@api.route('/api/v1/transfer', methods=['POST'])
@api.doc(params={'username': 'A username for logging in'})
class Transfer(Resource):
    def post(self):
        json_data     = request.get_json()
        username      = json_data['username']
        toUser        = json_data['toUser']
        amount        = json_data['amount']

        start_time = start_timer()
        user_exists = user_db.user_exists(username, "doesn't matter")
        resp_time = stop_timer(start_time)
        logger.info(ts=timestamp(),host=request.remote_addr,path=request.full_path, function="user_db.user_exists()", resp_time=resp_time)
        start_time = start_timer()
        toUser_exists = user_db.user_exists(toUser, "doesn't matter")
        resp_time = stop_timer(start_time)
        logger.info(ts=timestamp(),host=request.remote_addr,path=request.full_path, function="user_db.user_exists()", resp_time=resp_time)

        if user_exists and toUser_exists:

            fund_transfer(username, toUser, amount)
            start_time = start_timer()
            fund_transfer(username, toUser, amount)
            resp_time = stop_timer(start_time)
            logger.info(ts=timestamp(),host=request.remote_addr,path=request.full_path, function="fund_transfer()", resp_time=resp_time)

            logger.info(ts=timestamp(),host=request.remote_addr, path=request.full_path, status=200, username=username, msg="SUCCESS")
            contents = jsonify(status="SUCCESS",
                               transfer="Completed transfer of "+amount+" from "+username+" to "+toUser)
            return contents
        else:
            logger.error(ts=timestamp(),host=request.remote_addr, path=request.full_path, status=401, username=username, msg="INVALID_TRANSFER")
            abort(401)

@api.route('/api/v1/account', methods=['POST'])
@api.doc(params={'username': 'A username for logging in'})
class Account(Resource):
    def post(self):
        json_data = request.get_json()
        username = json_data['username']

        start_time = start_timer()
        user_exists = user_db.user_exists(username, "doesn't matter")
        resp_time = stop_timer(start_time)
        logger.info(ts=timestamp(),host=request.remote_addr,path=request.full_path, function="user_db.user_exists()", resp_time=resp_time)

        if user_exists:
            logger.info(ts=timestamp(),host=request.remote_addr, path=request.full_path, status=200, username=username, msg="SUCCESS")
            return jsonify(accounts[username])
        else:
            logger.error(ts=timestamp(),host=request.remote_addr, path=request.full_path, status=401, username=username, msg="INVALID_ACCOUNT")
            abort(401)

@api.route('/api/v1/help', methods=['GET'])
class Help(Resource):
    def get(self):
        logger.info(ts=timestamp(),host=request.remote_addr, path=request.full_path, status=200, msg="SUCCESS")
        return jsonify(there="is",absiolutely="no",help="lol")

def fund_transfer(username, toUser, amount):
    accounts[username]['balance'] -= int(amount)
    accounts[toUser]['balance'] += int(amount)
    accounts[username]['transactions'].append({'type': 'to', 'who': toUser, 'amount': amount})
    accounts[toUser]['transactions'].append({'type': 'from', 'who': username, 'amount': amount})

def timestamp():
    return str(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'))


def start_timer():
    return time.time()

def stop_timer(start_time):
    resp_time = time.time() - start_time
    return resp_time

if __name__ == '__main__':
    logging.basicConfig(
        format="%(message)s", stream=sys.stdout, level=logging.DEBUG
    )
    structlog.configure(processors=[structlog.processors.KeyValueRenderer()])
    bank_service.run(host="127.0.0.1",port=5000)
