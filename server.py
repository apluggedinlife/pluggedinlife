from flask import Flask, render_template, abort, url_for

PLAYERS = ('thoas', 'norelijn',)

app = Flask(__name__)

try:
    import settings
    app.config.from_object(settings.DevelopmentConfig \
                           if __name__ == '__main__' else settings.ProductionConfig)
except ImportError:
    pass

@app.route('/<any(%s):username>' % ', '.join(PLAYERS), methods=['GET'])
def get(username):
    return render_template('players/%s.html' % username) 

@app.route('/')
def index():
    return render_template('index.html', players=PLAYERS)

@app.errorhandler(404)
@app.route('/404')
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
