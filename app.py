import logging
import subprocess

import flask

import config
app = flask.Flask(__name__)
LOG = logging.getLogger(__name__)


def _get_stream_url():
    return "http://%s:%d" % (config.LOCAL_IP, config.LOCAL_PORT)

def _get_outer_stream_url():
    return "http://%s:%d" % (config.REMOTE_IP, config.REMOTE_PORT)


@app.route('/')
def control():
    res = subprocess.call(['pidof', 'autossh'])
    on_air = res == 0
    return flask.render_template('control.html', on_air=on_air,
                                 stream_url=_get_stream_url(),
                                 outer_stream_url=_get_outer_stream_url())


@app.route('/manage')
def camera_manage():
    action = flask.request.args.get('button')
    try:
        if action == u'on':
            subprocess.check_call(
                ['/bin/sh', '-c',
                 ('autossh -M 20000 -f -N -o "PubkeyAuthentication=yes" '
                  '%(rhost)s -R %(rport)s:localhost:%(lport)s -C') % {
                      'rport': config.REMOTE_PORT,
                      'lport': config.LOCAL_PORT,
                      'rhost': config.REMOTE_HOST}])
        else:
            subprocess.check_call(['/bin/sh', '-c', 'kill $(pidof autossh)'])
    except subprocess.CalledProcessError as e:
        LOG.error(e.message)
    return flask.redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
