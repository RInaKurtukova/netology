import re
import json
from collections import defaultdict

import click
import requests as req

import vkauth


SERVICE_ACCESS_KEY = "1c58294f1c58294f1c58294f8c1c39c58411c581c58294f46e9903d693fa29aac4aaf92"
API_VERSION = 5.73
APP_ID = 6417611
SECRET_KEY = "8GBWBYWSrf3mNQWMZmZp"


class UserNotExist(Exception):
    pass


def get_user_info(user_name):
    data = {
        'user_ids': [user_name],
        'v': API_VERSION
    }
    r = req.get("https://api.vk.com/method/users.get", params=data)

    try:
        return json.loads(r.text)['response'][0]
    except KeyError:
        raise UserNotExist(r.text)


def get_user_id(user):
    if re.findall(r'id[\d]+$', user):
        return user

    user_info = get_user_info(user)
    return user_info['id']


def get_user_groups(user_id, access_token):
    data = {
        'user_id': user_id,
        'v': API_VERSION,
        'access_token': access_token
    }
    r = req.get("https://api.vk.com/method/groups.get", params=data)
    try:
        return json.loads(r.text)['response']['items']
    except:
        return set()


def get_friends(user_id):
    data = {
        'user_id': user_id,
        'v': API_VERSION
    }
    r = req.get("https://api.vk.com/method/friends.get", params=data)

    return json.loads(r.text)['response']['items']


def get_groups_info(groups, access_token):
    data = {
        'access_token': access_token,
        'group_ids': ','.join(groups),
        'v': API_VERSION,
        'fields': 'members_count'
    }
    r = req.get("https://api.vk.com/method/groups.getById", params=data)
    r.encoding = 'utf-8'

    try:
        response = json.loads(r.text)['response']
    except:
        print("ERROR!")

    groups = []
    for group in response:
        groups.append({
            'id': group['id'],
            'name': group['name'],
            'members_count': group.get('members_count', '0')
        })

    return groups


@click.command()
@click.argument('user')
def main(user):
    user_id = get_user_id(user)

    session = vkauth.VKAuth(permissions='groups',
                            app_id=APP_ID, api_v=API_VERSION)
    session.auth()

    user_groups = set(get_user_groups(user_id, session._access_token))

    friend_ids = get_friends(user_id)

    print("Progress:")
    friend_groups = defaultdict(list)
    for i, friend_id in enumerate(friend_ids):
        print("{}/{}".format(i, len(friend_ids)), end='\r', flush=True)
        friend_groups[friend_id] = get_user_groups(
            friend_id, session._access_token)

    for friend_id, groups in friend_groups.items():
        user_groups -= set(groups)

    user_groups = {str(i) for i in user_groups}

    groups = get_groups_info(user_groups, session._access_token)

    with open("groups.json", "w") as file:
        json.dump(groups, file)

    print("Complete")
    print("Done. Data saved in groups.json")


if __name__ == "__main__":
    main()