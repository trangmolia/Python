from collections import Counter
from datetime import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from typing import List, Tuple

from api import messages_get_history
from api_models import Message
import config
import random


Dates = List[datetime.date]
Frequencies = List[int]

dates = []
frequencies = []


plotly.tools.set_credentials_file(
    username=config.PLOTLY_CONFIG['username'],
    api_key=config.PLOTLY_CONFIG['api_key']
)


def fromtimestamp(ts: int) -> datetime.date:
    return datetime.datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) -> Tuple[Dates, Frequencies]:
    """ Получить список дат и их частот

    :param messages: список сообщений
    """

    new_date = []
    flag = []

    for message in messages:
        new_date.append(message['date']) # list with unixtime

    new_date = sorted(new_date)

    for i in range(len(new_date)):
        _date = datetime.utcfromtimestamp(new_date[i]).strftime("%Y-%m-%d")
        if _date not in dates:
            dates.append(_date)
            flag.append(i)

    for i in range(len(flag)):
        if i == 0:
            frequencies.append(flag[i] + 1)
        else:
            frequencies.append(flag[i] - flag[i-1])

    return dates, frequencies


def plotly_messages_freq(dates: Dates, freq: Frequencies) -> None:
    """ Построение графика с помощью Plot.ly

    :param date: список дат
    :param freq: число сообщений в соответствующую дату
    """
    data = [go.Scatter(x=dates, y=freq)]
    py.plot(data)

if __name__ == '__main__':
    flag = messages_get_history(user_id=73415922)
    count_dates_from_messages(flag)
    plotly_messages_freq(dates=dates, freq=frequencies)




