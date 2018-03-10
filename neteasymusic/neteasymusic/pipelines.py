# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:mysql@127.0.0.1:3306/neteasymusic?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Music(db.Model):
    __tablename__ = 'music'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    artists_name = db.Column(db.String(140))
    album_name = db.Column(db.String(140))
    total = db.Column(db.Integer)
    books = db.relationship('Comment', backref='author')

    def __init__(self, id, name, artists_name, album_name, total):

        self.id = id
        self.name = name
        self.artists_name = artists_name
        self.album_name = album_name
        self.total = total



class Comment(db.Model):

    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    music_id = db.Column(db.Integer, db.ForeignKey('music.id'))
    comment = db.Column(db.String(140))
    nickname = db.Column(db.String(140))
    time = db.Column(db.DATETIME)
    likecount = db.Column(db.Integer)

    def __init__(self, id, music_id, comment, nickname, time, likecount):

        self.id = id
        self.music_id = music_id
        self.comment = comment
        self.nickname = nickname
        self.time = time
        self.likecount = likecount



db.create_all()
class NeteasymusicPipeline(object):
    def __init__(self):
        db.create_all()
        self.comment_count = 0
        self.music_count = 0
        self.f = open('/Users/Xiaobaoxia/Desktop/comment.json', 'a')

    def process_item(self, item, spider):

        try:
            new = Comment(id=item['id'], music_id=item['music_id'], comment=item['comment'],
                          nickname=item['nickname'], time=item['time'], likecount=item['likedcount'])
            # json.dump(f, item)
            self.comment_count += 1
            print self.comment_count

        except Exception :
            new = Music(id=item['id'], name=item['name'], artists_name=item['artists_name'],
                        album_name=item['album_name'], total=item['total'])
            self.music_count += 1
            print self.music_count

        db.session.add(new)


        db.session.commit()

        return item

    def close_spider(self, spider):

        db.session.close()