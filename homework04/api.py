import requests
import time
import random

import config


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    flag = 0
    while flag < max_retries:
        try:
            return requests.get(url)
        except requests.exceptions.RequestException:
            if flag == max_retries - 1:
                raise
            sum_time = backoff_factor * (2 ** flag)
            flag += 1
            time.sleep(sum_time)


def get_friends(user_id, fields):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    query_params = {
        'domain': config.VK_CONFIG['domain'],
        'access_token': config.VK_CONFIG['access_token'],
        'user_id': user_id,
        'fields': fields
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.92".format(**query_params)
    response = get(query).json()

    if 'response' in response:
        return response['response']['items']

    return None


def messages_get_history(user_id, offset=0, count=20):
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"

    query_params = {
        'domain': config.VK_CONFIG['domain'],
        'access_token': config.VK_CONFIG['access_token'],
        'user_id': user_id,
        'offset': offset,
        'count': count,
    }

    query = "{domain}/messages.getHistory?access_token={access_token}\&user_id={user_id}&offset={offset}&count={count}&v=5.92".format(**query_params)

    mess = []
    response = get(query)
    data = response.json()
    cycles = data['response']['count'] // 200

    if not cycles:
        mess.append(response.json()['response']['items'])
        return mess

    for i in enumerate(cycles, 1):
        response = get(query)
        query_params['offset'] += 200
        mess.append(response.json()['response']['items'])
        time.sleep(0.33)

    return  mess

if __name__ == '__main__':
    print(messages_get_history(user_id=462579673))








