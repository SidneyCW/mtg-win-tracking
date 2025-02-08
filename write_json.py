import json

def write_json(new_data, username, filename='user_data/users'):

    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data[username].update(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)
        file.truncate()
        
# code written by aman neekhara and found on https://www.geeksforgeeks.org/append-to-json-file-using-python/