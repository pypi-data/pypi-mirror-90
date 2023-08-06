"""## Default application settings

Below are the default settings for Hemlock applications and extensions.

App settings
------------
clean_data : callable or None, default=None
    Callable which cleans your data before downloading or creating a data 
    profile. This callable takes and returns `pandas.DataFrame`. If `None`, no
    additional cleaning is performend.

collect_IP : bool, default=True
    Indicates that participants' IP addresses will be associated with their
    data.

duplicate_keys : list, default=[]
    List of keys (column names) on which to block duplicate participants. If
    empty, the app will not screen out duplicates.

loading_page : str or callable, default=gen_loading_page
    Loading page HTML (str) or function which returns the loading page (str).

restart_option : bool, default=True
    Indicates that participants who attempt to re-navigate to the index page 
    will be given the option to restart the survey. If `False`, participants 
    to attempt to re-navigate to the index page will be redirected to their 
    current survey page.

restart_page : str or callable, default=gen_restart_page
    Restart page HTML (str) or function which returns the restart page (str).

screenout_csv : str, default='screenout.csv'
    Name of the csv file containing criteria for screening out participants.

screenout_keys : list, default=[]
    List of keys (column names) on which to screen out participants. If empty,
    participants will be screened out based on all keys in the screenout csv.

screenout_text : str, default='...you have already participated...'
    Text displayed to participants who are ineligible to participate in this 
    survey.

socket_js_src : str, default='https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.3.0/socket.io.js'
    Source of the websocket javascript.

static_folder : str, default='static'
    Path to the static folder.

template_folder : str, default='templates'
    Path to the template folder.

time_expired_text : str, default='You have exceeded your time limit...'
    Text displayed to participants whose time has expired.

time_limit : datetime.timedelta or None, default=None
    Time limit for participants to complete the survey.

validate : bool, default=True
    Indicate that all validation is active. Set to `False` to turn off all 
    validation for testing.

Config
------
PASSWORD : str
    Looks for a `PASSWORD` environment variable.

PASSWORD_HASH : str
    Generated password hash.

SECRET_KEY : str
    Looks for a `SECRET_KEY` environment variable.

SQLALCHEMY_DATABASE_URI : str
    Looks for `DATABASE_URL` environment variable. Otherwise, we use a SQLite 
    database `data.db` in the current working directory.

SQLALCHEMY_TRACK_MODIFICATIONS: bool, default=False

REDIS_URL : str, default=None
    Looks for a `REDIS_URL` environment variable.

DownloadBtnManager
------------------

Manager
-------
loading_img_blueprint : str or None, default='hemlock'
    Name of the blueprint to which the loading image belongs. If `None`, the 
    loading image is assumed to be in the app's `static` directory.

loading_img_filename : str or None, default='img/worker_loading.gif'
    Name of the loading image file.

Talisman
--------
content_security_policy : dict
    Content security policy for 
    [flask-talisman](https://github.com/GoogleCloudPlatform/flask-talisman).
    Default allows for third party content from Bootstrap, Cloudflare, 
    Google API, JQuery, JSDeliver, SocketIO, and YouTube.

Notes
-----
See <https://flask.palletsprojects.com/en/1.1.x/config/> for more detail on 
Flask application configuration.

See <https://dsbowen.github.io/flask-download-btn/manager/> for more detail on 
DownloadBtnManager settings.

See <https://dsbowen.github.io/flask-worker/manager/> for more detail on 
Manager settings.
"""

from flask import render_template
from werkzeug.security import generate_password_hash

import os

PASSWORD = os.environ.get('PASSWORD', '')
PASSWORD_HASH = generate_password_hash(PASSWORD)

SCREENOUT_TXT = """
<p>Our records indicate that you have already participated in this or similar surveys.</p>
<p>Thank you for your continuing interest in our research.</p>
"""

SOCKET_JS_SRC = 'https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.3.0/socket.io.js'

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL', 'sqlite:///'+os.path.join(os.getcwd(), 'data.db')
)

TIME_EXPIRED_TXT = 'You have exceeded your time limit for this survey'

def gen_loading_page():
    from ..models import Page
    from ..qpolymorphs import Label

    return Page(
        Label(
            '''
            The next page should load automatically in a few seconds.
            '''
        ),
        forward=False,
        extra_js=render_template('hemlock/loading.js')
    )._render()

def gen_restart_page():
    from ..models import Page
    from ..qpolymorphs import Label

    return Page(
        Label(
            """
            <p>Click << to resume the survey. Click >> to restart 
            the survey.</p>
            If you restart the survey, your responses will not be 
            saved.
            """
        ),
        back=True
    )._render()

def gen_500_page():
    from ..models import Page
    from ..qpolymorphs import Label

    return Page(
        Label(
            """
            <p>The application encountered an error. <b>Try refreshing the page</b> (this usually solves the problem).</p> 
            If you keep getting an error, contact the survey administrator. We apologize for the inconvenience and thank your for your patience while we resolve the issue.
            """
        ),
        forward=False
    )._render()

settings = dict(
    clean_data=None,
    collect_IP=True,
    duplicate_keys=[],
    error_500_page=gen_500_page,
    loading_page=gen_loading_page,
    restart_option=True,
    restart_page=gen_restart_page,
    screenout_csv='screenout.csv',
    screenout_keys=[],
    screenout_text=SCREENOUT_TXT,
    socket_js_src=SOCKET_JS_SRC,
    static_folder='static',
    template_folder=os.path.join(os.getcwd(), 'templates'),
    time_expired_text=TIME_EXPIRED_TXT,
    time_limit=None,
    validate=True,
    Config=dict(
        PASSWORD=PASSWORD,
        PASSWORD_HASH=PASSWORD_HASH,
        SECRET_KEY=os.environ.get('SECRET_KEY', 'secret-key'),
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ENGINE_OPTIONS=(
            {} if SQLALCHEMY_DATABASE_URI.startswith('sqlite')
            else dict(
                pool_size=1,
                pool_recycle=10,
                max_overflow=0
            )
        ),
        REDIS_URL=os.environ.get('REDIS_URL'),
    ),
    DownloadBtnManager={},
    Manager=dict(loading_img_src='/hemlock/static/img/worker_loading.gif'),
    Talisman=dict(
        content_security_policy={
            'default-src': ['\'self\'', '\'unsafe-inline\'', 'data:'],
            'frame-src': [
                '\'self\'', 
                '\'unsafe-inline\'', 
                'data:',
                'https://www.youtube.com',
            ],
            'frame-ancestors': [
                '*'
            ],
            'font-src': [
                'https://fonts.googleapis.com',
                'https://fonts.gstatic.com',
            ],
            'img-src': ['\'self\'', '\'unsafe-inline\'', 'data:'],
            'script-src': [
                '\'self\'',
                '\'unsafe-eval\'',
                '\'unsafe-inline\'',
                'https://code.jquery.com',
                'https://cdn.jsdelivr.net',
                'https://stackpath.bootstrapcdn.com',
                'https://cdnjs.cloudflare.com'
            ],
            'style-src': [
                '\'self\'',
                '\'unsafe-inline\'',
                'https://fonts.googleapis.com/css',
                'https://stackpath.bootstrapcdn.com'
            ],
        },
    )
)