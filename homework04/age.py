from datetime import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    friend = get_friends(user_id, fields='bdate')
    list_age = []

    for item in friend:
        if 'bdate' in item:
            item = User(**item)
            birthday = item.bdate
            today = dt.now()

            if len(birthday) == 10:
                born = dt.strptime(birthday, '%d.%m.%Y')
                age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
                list_age.append(age)

    if len(list_age) != 0:
        return median(list_age)

    return None





