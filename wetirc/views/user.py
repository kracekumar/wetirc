from brubeck.templating import Jinja2Rendering

class IndexHandler(Jinja2Rendering):
    def get(self):
        context = {'message': 'Welcome to wetirc'}
        return self.render_template('index.html', **context)


class IRCChannel(Jinja2Rendering):
    def get(self, name):
        context = {'message': 'channel'}
        return self.render_template('index.html', **context)
