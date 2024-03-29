from flask import Flask, render_template, request, session, copy_current_request_context
from vsearch import search4letters
from DBcm import UseDatabase, ConnectionError
from checker import check_logged_in
from threading import Thread


app = Flask(__name__)
app.secret_key = 'YouWillNeverGuessMySecretKey'


@app.route('/search4', methods=['POST'])
def do_search() -> str:
    @copy_current_request_context
    def log_request(req: 'flask-request', res: str) -> None:
        """ Log details of the web request and the results."""
        with UseDatabase (app.config['dbconfig']) as cursor:
            _SQL = """insert into log
                    (phrase, letters, ip, browser_string, results)
                    values
                    (%s, %s, %s, %s, %s)"""

            cursor.execute (_SQL, (req.form['phrase'],
                                   req.form['letters'],
                                   req.remote_addr,
                                   req.user_agent.browser,
                                   res,))
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results: '
    results = str(search4letters(phrase, letters))
    try:
        t = Thread(target= log_request, args= (request, results))
        t.start()
    except Exception as err:
        print('DB right activity failed with error:', str(err))
    return render_template ('results.html', the_title=title, the_phrase=phrase, the_letters=letters,
                                the_results=results)
    

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4letters on the web!')

@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            Query = """Select phrase, IP, browser_string, results from log"""
            cursor.execute(Query)
            log = cursor.fetchall()
    except ConnectionError as err:
        print('""" Databse Could Not be connected', str(err))
        log = ''
    except Exception as err:
        print('""" Databse Could Not be connected', str(err))
        log = ''
    titles = ('Form Data', 'Remote_addr', 'User_agnet', 'Results')
    return render_template('viewlog.html', the_title='View Log', the_row_titles=titles, the_data=log)

@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'you are now logged in'

@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'you are now logged out'

if __name__ == '__main__':
    app.config['dbconfig'] = {'host': '127.0.0.1',
                              'user': 'root',
                              'password': 'pakistan',
                              'database': 'vsearchlogdb', }
    app.run (debug=True)

else:
    app.config['dbconfig'] = { 'host': 'shussain.mysql.pythonanywhere-services.com',
                             'user': 'shussain',
                             'password': 'sarfrazMySQL',
                             'database': 'shussain$vsearchlogdb', }