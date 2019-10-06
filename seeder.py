import csv
import json
import requests
from conf.settings import Config

HOST = "http://127.0.0.1"

HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


def add_users(users):
    url = "{}:{}/users".format(HOST, Config.port)
    for user in users:
        resp = requests.post(url, json.dumps(user), headers=HEADERS)
        if resp.status_code != 200:
            print("user creation failed for user:{}".format(user))


def add_associations(user_maps):
    for email, users in user_maps.items():
        url = "{}:{}/users/{}/following_users".format(
            HOST, Config.port, email)
        for user in users:
            resp = requests.put(
                url,
                json.dumps({"following_user_email": user}),
                headers=HEADERS)
            if resp.status_code != 200:
                print(
                    "user association failed for user:{} with user:{}".format(
                        email, user))


def read_users_from_csv(filename):
    users = []
    with open(filename, mode='r') as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i == 0:
                i += 1
                continue
            value = row[0].split(",")
            users.append({
                "email": value[0],
                "name": value[1],
                "phone": value[2]})
            i += 1
    return users


def read_following_users_from_csv(filename):
    user_maps = {}
    with open(filename, mode='r') as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i == 0:
                i += 1
                continue
            value = row[0].split(",")
            if value[1:]:
                user_maps[value[0]] = value[1:]
            i += 1
    return user_maps


if __name__ == "__main__":
    users = read_users_from_csv("users.csv")
    add_users(users)
    user_maps = read_following_users_from_csv("following_users.csv")
    add_associations(user_maps)
