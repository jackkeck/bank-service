import requests
import json
import hit_me
import random
import itertools
import collections
import hit_me

with open('config/users.json') as users_file:
    accounts = collections.OrderedDict(json.load(users_file))

accounts_index = len(accounts)-1
for _ in itertools.repeat(None, 100):
    username_object = random.choice(list(accounts.items()))
    username_index = accounts.keys().index(username_object[0])
    username = username_object[0]

    if (username_index) == accounts_index:
        toUser_index = random.randint(0, (username_index-1))
    else:
        toUser_index = random.randint((username_index+1), accounts_index)

    toUser_object = accounts.items()[toUser_index]
    toUser = toUser_object[0]
    amount = str(random.randint(3, 7654))
    password = "randomWHASSUP12!@" 

    hit_me.loginAsUser(username, password)
    hit_me.makeTransfer(username, toUser, amount)
    hit_me.accountSummary(username)
    hit_me.help()
    hit_me.logoutAsUser(username)
