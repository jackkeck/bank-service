import requests
import json

def loginAsUser(username, password):
    url = 'http://127.0.0.1:5000/api/v1/login'
    headers = {'Content-Type': "application/json"}
    data = {"username": username, "password": password}
    response = requests.post(url, headers=headers, json=data)
    print ("loginAsUser("+str(username)+", password) returns: "+ str(response.status_code))

def makeTransfer(username, toUser, amount):
    url = 'http://127.0.0.1:5000/api/v1/transfer'
    headers = {'Content-Type': "application/json"}
    data = {"username": username, "toUser": toUser, "amount": amount}
    response = requests.post(url, headers=headers, json=data)
    print ("makeTransfer("+str(username)+", "+str(toUser)+", "+str(amount)+") returns: "+str(response.text))

def accountSummary(username):
    url = 'http://127.0.0.1:5000/api/v1/account'
    headers = {'Content-Type': "application/json"}
    data = {"username": username}
    response = requests.post(url, headers=headers, json=data)
    print ("accountSummary("+str(username)+") returns: "+str(response.text))

def help():
    url = 'http://127.0.0.1:5000/api/v1/help'
    response = requests.get(url)
    print ("help() returns: "+ str(response.status_code))

def logoutAsUser(username):
    url = 'http://127.0.0.1:5000/api/v1/logout'
    headers = {'Content-Type': "application/json"}
    data = {"username": username}
    response = requests.post(url, headers=headers, json=data)
    print ("logoutAsUser("+str(username)+") returns: "+ str(response.status_code))
