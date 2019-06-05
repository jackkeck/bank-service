import json

# Simulate a user database in memory
def user_exists(username, password):
    with open('config/users.json') as users_file:
        accounts = json.load(users_file)
    print ("checking users.json for: "+username)
    if username in accounts:
        return True
    else:
        return False
