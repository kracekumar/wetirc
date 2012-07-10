#! /usr/bin/env python
from fabric.api import local


def push(branch):
    local("git push -u origin %s" % branch)


def pull():
    local("git pull")


def commit(message):
    local("git commit -am '%s'" % message)


def commit_and_push(message, branch):
    commit(message)
    push(branch)


def track_all():
    local("git add -A")


def track(filename):
    local("git add %s" % filename)


def load_mongrel():
    local("m2sh load -config mongrel2.conf -db the.db")


def start_mongrel():
    local("m2sh start -db the.db -host localhost")


def start_brubeck():
    local("python app.py")
