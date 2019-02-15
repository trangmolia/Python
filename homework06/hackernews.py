from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier

s = session()


# when access to localhost, need to type "/news" or any string, which inside @route()
# can use @route("/") (dynamic route) on top to render default page, if available
@route("/news")
def news_list():
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # get value of label via query parameter in template
    label = request.query.label
    current_id = request.query.id
    row = s.query(News).filter(News.id == current_id).all()
    # row is list of map, and length of row is 1, so need to call row[0]
    row[0].label = label
    s.commit()
    redirect("/news")


# update news to news.db (use SQLALchemy)
@route("/update")
def update_news():
    news = get_news('https://news.ycombinator.com/newest', 1)
    for new in news:
        s.add(News(title=new['title'],
                   author=new['author'],
                   url=new['url'],
                   comments=new['comments'],
                   points=new['points']))
    s.commit()
    redirect("/news")


@route('/recommendations')
def recommendations():
    # 1. Получить список неразмеченных новостей из БД
    # 2. Получить прогнозы для каждой новости
    # 3. Вывести ранжированную таблицу с новостями

    return template('news_recommendations', rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
