from fabric.api import local
from os import getcwd
from os.path import sep


def build_path(path):
    """
        Function to build the path, since fabfile.py is placed in
       current directory, just append the value with current path
    """
    if path:
        return sep.join([getcwd(), path])
    else:
        print "path is not mentioned"


############################gunicorn configuration##############################
app_name = 'wetirc'
workers = 2
access_log = build_path('access.log')
error_log = build_path('error.log')
log_level = 'debug'
timeout = 120
port = 27502

start_recv_command = "nohup python2.7 recv.py >> recv.out &"
start_collector_command = "nohup python2.7 collector.py >> collector.out &"


def start_server(pid):
    command = """gunicorn %s:app --workers=%d --access-logfile %s --error-logfile %s --log-level %s --timeout=%d --daemon --bind=127.0.0.1:%d --pid=%s""" %\
                 (app_name, workers, access_log, error_log, log_level, timeout, port, build_path("." + pid))
    print command
    local(command)


def restart_server():
    try:
        with open('.pid', 'r') as f:
            pid = int(f.readline())
            local("kill -HUP %d" % pid)
    except IOError:
        try:
            with open('..pid', 'r') as f:
                pid = int(f.readline())
                local("kill -HUP %d" % pid)
        except IOError:
            print "pid file not found"
    except:
        print "unable to restart"


def push_to_github():
    local("git push -u origin master")


def list_process():
    local("ps aux | grep %d" % port)


def deploy():
    local("git pull")
    restart_server()


def hello():
    print 'hello, This is test!'
