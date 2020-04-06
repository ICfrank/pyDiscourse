import json

import UserAgent as UserAgent
from requests import Session


def creatTopic(data):
    ua = UserAgent()
    user_agent = {'User-agent': ua.random, 'Referer': 'https://dealbub.com/','Content-type': 'content_type_value'}
    session = Session()
    session.head('https://dealbub.com/')
    data = topicContect()
    response = session.post(
        url='https://alisdeals.com/posts/',
        headers=user_agent,
        data = data
    )

# return json
def topicContect(json):
    return