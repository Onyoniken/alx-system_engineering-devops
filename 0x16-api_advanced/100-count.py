#!/usr/bin/python3
""" raddit api"""

import json
import requests


def count_words(subreddit, word_list, after="", count=[]):
    """count words"""

    if after == "":
        count = [0] * len(word_list)

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    request = requests.get(url,
                           params={'after': after},
                           allow_redirects=False,
                           headers={'user-agent': 'bhalut'})

    if request.status_code == 200:
        data = request.json()

        for topic in (data['data']['children']):
            for word in topic['data']['title'].split():
                for k in range(len(word_list)):
                    if word_list[k].lower() == word.lower():
                        count[k] += 1

        after = data['data']['after']
        if after is None:
            save = []
            for k in range(len(word_list)):
                for a in range(k + 1, len(word_list)):
                    if word_list[k].lower() == word_list[a].lower():
                        save.append(a)
                        count[k] += count[a]

            for k in range(len(word_list)):
                for j in range(k, len(word_list)):
                    if (count[a] > count[k] or
                            (word_list[k] > word_list[a] and
                             count[a] == count[k])):
                        aux = count[k]
                        count[k] = count[a]
                        count[a] = aux
                        aux = word_list[k]
                        word_list[k] = word_list[a]
                        word_list[a] = aux

            for k in range(len(word_list)):
                if (count[k] > 0) and k not in save:
                    print("{}: {}".format(word_list[k].lower(), count[k]))
        else:
            count_words(subreddit, word_list, after, count)
