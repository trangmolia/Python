import requests
import config
import telebot
from datetime import *
from bs4 import BeautifulSoup


bot = telebot.TeleBot(config.access_token)
work_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']


def get_page(group: str, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_any_day(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    index = str(work_days.index(day) + 1)
    index += "day"
    schedule_table = soup.find("table", attrs={"id": index})

    # Время проведения занятий
    if schedule_table is None:
        return None
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [times.span.text for times in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    day, group = message.text.split()
    web_page = get_page(group)
    resp = ''
    day = day[1].upper() + day[2:]
    if parse_schedule_for_any_day(web_page, day) is None:
        bot.send_message(message.chat.id, 'The system is currently unavailable. Please try back later.',
                         parse_mode='HTML')
        return None
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_any_day(web_page, day)
    if times_lst:
        for _time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(_time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, 'No classes today, Trang')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    _, group = message.text.split()
    web_page = get_page(group)
    today = datetime.now()
    _date = today.weekday()
    if _date is not 6:
        if parse_schedule_for_any_day(web_page, work_days[_date]) is None:
            bot.send_message(message.chat.id, 'The system is currently unavailable. Please try back later.',
                             parse_mode='HTML')
            return None
        times_lst, locations_lst, lessons_lst = \
            parse_schedule_for_any_day(web_page, work_days[_date])
        for i in range(len(times_lst)):
            t1 = times_lst[i][0:5]
            t1 = datetime.strptime(t1, '%H:%M')
            if today.time() < t1.time():
                result = '<b>{}</b>, {}, {}\n'.format(times_lst[i], locations_lst[i], lessons_lst[i])
                bot.send_message(message.chat.id, result, parse_mode='HTML')
                return None

    if _date == 6:
        _date = 0

    for i in range(_date, 5):
        if parse_schedule_for_any_day(web_page, work_days[_date]) is None:
            bot.send_message(message.chat.id, 'The system is currently unavailable. Please try back later.',
                             parse_mode='HTML')
            break
        times_lst, locations_lst, lessons_lst = \
            parse_schedule_for_any_day(web_page, work_days[_date])
        if times_lst:
            result = '<b>{}</b>, {}, {}\n'.format(times_lst[0], locations_lst[0], lessons_lst[0])
            bot.send_message(message.chat.id, result, parse_mode='HTML')
            break


@bot.message_handler(commands=['tomorrow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    _, group = message.text.split()
    web_page = get_page(group)
    tomorrow = datetime.now().weekday() + 1
    resp = ''

    if tomorrow == 6:
        bot.send_message(message.chat.id, 'No classes tomorrow, Trang', parse_mode='HTML')
        return None
    if tomorrow == 7:
        tomorrow = 0
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_any_day(web_page, work_days[tomorrow])
    if times_lst:
        for _time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(_time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, 'No classes tomorrow, Trang', parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    _, group = message.text.split()
    web_page = get_page(group)
    for day in work_days:
        resp = ''
        if parse_schedule_for_any_day(web_page, day) is None:
            bot.send_message(message.chat.id, 'The system is currently unavailable. Please try back later.',
                             parse_mode='HTML')
            break
        times_lst, locations_lst, lessons_lst = \
            parse_schedule_for_any_day(web_page, day)

        if times_lst:
            for _time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}\n'.format(_time, location, lession)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
