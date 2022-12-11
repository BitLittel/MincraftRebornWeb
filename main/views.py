# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, jsonify, g
from main import main
import time
from datetime import datetime
from sqlalchemy import and_, null
from main.database import Session, Versions, News


@main.before_request
def before_request():
    g.db = Session()


@main.teardown_request
def teardown_request(exception):
    g.db.close()


@main.errorhandler(404)
def internal_error(error):
    return render_template('404.html')


@main.errorhandler(500)
def internal_error(error):
    return render_template('500.html')


@main.route('/api/add_version', methods=['POST'])
def api_add_version():
    data = request.json
    new_version = Versions(data=data)
    g.db.add(new_version)
    g.db.commit()
    return jsonify(dict(result=True, message='Версия успешно добавлена'))


@main.route('/api/get_version', methods=['GET'])
def api_get_version():
    return jsonify(dict(result=True, versions=[i for i in g.db.query(Versions).all()]))


@main.route('/api/del_news', methods=['GET'])
def api_del_news():
    news_id = int(request.args.get('news_id'))
    get_news = g.db.query(News).filter(and_(News.visible == True, News.news_id == news_id)).first()
    get_news.visible = False
    g.db.commit()
    return jsonify(dict(result=True, message='Новость удалена'))


@main.route('/api/add_news', methods=['GET'])
def api_add_news():
    new_news = News(
        title=request.args.get('title'),
        message=request.args.get('message'),
        link=request.args.get('link')
    )
    g.db.add(new_news)
    g.db.commit()
    return jsonify(dict(result=True, message='Новость добавлена'))


@main.route('/api/get_news', methods=['GET'])
def api_get_news():
    get_news = g.db.query(News).filter(News.visible == True).order_by(News.datetime).all()
    news = [
        {
            "news_id": i.news_id,
            "datetime": i.datetime,
            "title": i.title,
            "message": i.message,
            "link": i.link
        } for i in get_news
    ]
    return jsonify(dict(result=True, news=news))
