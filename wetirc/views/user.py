#! -*- coding: utf-8 -*-

from wetirc import app
from flask import render_template
import jinja2

def make_filename(name, date):
    name = '_'.join([name, date])
    return name + '.log'


def check_date(date):
    split_date = date.split('-')
    try:
        if len(split_date[0]) == 4 and int(split_date[0]) >= 2012 and len(split_date[1]) == 2 and \
            1 <= int(split_date[1]) <= 12 and len(split_date[2]) == 2 and 1 <= int(split_date[2]) <= 31:
            return True
        else:
            return False

    except:
        return False


def read_file(filename, date):
    with open(''.join([app.config['IRCLOG'], make_filename(filename, date)])) as f:
        return f.readlines()


@app.route('/')
def index():
    return render_template('index.html', channels=app.config['CHANNELS'])


@app.route('/channel/<name>/<date>')
def channel_dates(name, date):
    CHANNELS = app.config['CHANNELS']
    channel_name = '#' + name
    if '#' + name not in CHANNELS:
        channel_name = '##' + name
        if '##' + name not in CHANNELS:
            channels = "<br/>".join(CHANNELS)
        message = " <br/>".join(["Channel name not found in the list. Following are the channels.", channels, "URL FORMAT: /channel/<channel>/<date>"])
        return message

    else:
        if check_date(date):
            contents = read_file(channel_name, date)
            for no, content in enumerate(contents):
                tmp = content.replace("<", "[")
                tmp = tmp.replace(">", "]")
                contents[no] = tmp

            contents = '<br/>'.join(contents)
            return '<br/>'.join(["<b>Time is in UTC format</b><br/>", contents])
        else:
            message = "Use YYYY-MM-DD format. E.G: /hasgeek/2012-07-23"
            return message
