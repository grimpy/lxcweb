# all the imports
import subprocess
from flask import Flask, request, session, g, redirect, url_for, \
             abort, render_template, flash
import lxc


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
l = lxc.LXC()


def command(cmd, *args):
    cargs = [ cmd ]
    cargs.extend(args)
    return subprocess.check_output(cargs)


@app.route('/')
def show_container():
    return render_template('overview.html', machines=l.list())

@app.route('/<name>/')
def info(name):
    return render_template('details.html', machine=l.getMachine(name))


@app.route('/<name>/<action>')
def action(name, action):
    m = l.getMachine(name)
    result = getattr(m, action)()
    if action != "info":
        return redirect(url_for('show_container'))
    else:
        return result

@app.route('/<name>/delete')
def deleteMachine(name):
    m = l.getMachine(name)
    m.delete()
    return redirect(url_for('show_container'))

@app.route('/<name>/clone/<newname>')
def clone(name, newname):
    m = l.getMachine(name)
    m.clone(newname)
    return redirect(url_for('show_container'))



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
