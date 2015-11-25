import logging
import subprocess

import flask

import config
app = flask.Flask(__name__)
LOG = logging.getLogger(__name__)


@app.route('/')
def control():
    res = subprocess.call(['pidof', 'autossh'])
    on_air = res == 0
    return flask.render_template('control.html', on_air=on_air)


@app.route('/manage')
def camera_manage():
    action = flask.request.args.get('button')
    on_air = action == u'on'
    try:
        if action == u'on':
            subprocess.check_call(
                ['autossh', '-M', '20000', '-f', '-N', config.REMOTE_HOST,
                 '-R',
                 '%(rport)s:localhost:%(lport)s' % {'rport': config.REMOTE_PORT,
                                                    'lport': config.LOCAL_PORT},
                 '-C'])
        else:
            subprocess.check_call(['exec' 'kill' '$(pidof autossh)'])
    except subprocess.CalledProcessError as e:
        LOG.error(e.message)
        on_air = False

    return flask.render_template('control.html', on_air=on_air)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
