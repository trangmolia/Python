from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


s = session()


@route("/news")
def news_list():
    # find all news not has label
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    label = request.query.label
    current_id = request.query.id
    row = s.query(News).filter(News.id == current_id).all()
    row[0].label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    news_list = get_news('https://news.ycombinator.com/newest', 1)
    for news in news_list:
        s.add(News(title=news['title'],
                   author=news['author'],
                   url=news['url'],
                   comments=news['comments'],
                   points=news['points']))
    s.commit()
    redirect("/news")


@route('/recommendations')
def recommendations():
    # 1. Получить список неразмеченных новостей из БД
    # 2. Получить прогнозы для каждой новости
    # 3. Вывести ранжированную таблицу с новостями

    # if define title_unclassified = title_classified = []
    # 2 lists will receive the same values
    title_unclassified = []
    title_classified = []
    label_list = []

    unclassified_news = s.query(News).filter(News.label.is_(None)).all()
    for news in unclassified_news:
        title_unclassified.append(news.title)

    classified_news = s.query(News).filter(News.label.isnot(None)).all()
    for news in classified_news:
        title_classified.append(news.title)
        label_list.append(news.label)

    data = NaiveBayesClassifier(alpha=1)
    data.fit(title_classified, label_list)

    label_classified = data.predict(title_unclassified)
    for i in range(len(unclassified_news)):
        unclassified_news[i].label = label_classified[i]
    s.commit()
    classified_news = s.query(News).filter(News.label == 'good').all()

    return template('recommendations_template', rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
