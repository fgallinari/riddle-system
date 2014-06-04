#!/usr/bin/env python
import logging
import os
import mimetypes
import tornado.ioloop
import tornado.options
import tornado.web
import hashlib

APP_PORT   = 9550
codes_path = '.codes'
end_game   = 'f92c358cefa4'
def makeLevelsList():
    levels = []
    count = 0
    for line in open(codes_path):
        line = line.split("|")
        count += 1
        levels.append({'number': count, "id":line[0].strip(), "img":line[1].strip(), "phrase":line[2].strip(), "kw":line[3].strip()})
    return levels

def getLevelFromID(levels, id):
    for level in levels:
        if id == level.get('id'):
            return level
    return levels[0]

settings = {
        "debug": True,
        }
if (settings["debug"]):
    print 'enter:', hashlib.sha224('enter').hexdigest()
    print 'gg:', hashlib.sha224('google').hexdigest()
    print 'bs:', hashlib.sha224('barney stinson').hexdigest()
    print 'in:', hashlib.sha224('isaac newton').hexdigest()
    print 'cs:', hashlib.sha224('computer science').hexdigest()
class GameOverHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('gameover.tmpl')
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.tmpl')
class LevelHandler(tornado.web.RequestHandler):
    def get(self, id_lvl):
        levels = makeLevelsList()
        level  = getLevelFromID(levels, id_lvl)

        self.render('level.tmpl', password='', level=level)

    def post(self, id_lvl):
        levels = makeLevelsList()
        level  = getLevelFromID(levels, id_lvl)

        keyword = self.get_argument('password', '')
        digest  = hashlib.sha224(keyword.lower().strip()).hexdigest()
        correct_ans = False
        next_id     = False
        if digest == level.get('kw'):
            correct_ans = True
            try:
                next_id     = levels[level.get('number')].get('id')
            except:
                next_id = end_game
        self.render('level.tmpl', level=level, password=keyword, correct_ans=correct_ans, next_id=next_id)
class DefaultHandler(tornado.web.RequestHandler):
    def get(self, path):
        try:
            with open(path, 'rb') as f:
                self.set_header('Content-Type', mimetypes.guess_type(path)[0])
                self.write(f.read())
        except:
            self.write('{"error": "Page not found"}')
if __name__ == "__main__":
    application = tornado.web.Application(**settings)
    application.add_handlers('', [
        (r"/", MainHandler),
        (r"/level", tornado.web.RedirectHandler, {'url': 'level/'}),
        (r"/level/"+end_game, GameOverHandler),
        (r"/level/(.*)", LevelHandler),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {'path': './_css'}),
        (r"/images/(.*)", tornado.web.StaticFileHandler, {'path': './_images'}),
        # (r"/(.*)", DefaultHandler),
    ])

    application.listen(APP_PORT)
    print 'Now listening at port:', APP_PORT
    tornado.options.parse_command_line()
    tornado.ioloop.IOLoop.instance().start()
