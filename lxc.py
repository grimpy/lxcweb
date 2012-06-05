# all the imports
import subprocess
from flask import Flask, request, session, g, redirect, url_for, \
             abort, render_template, flash


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def command(cmd, *args):
    cargs = [ cmd ]
    cargs.extend(args)
    return subprocess.check_output(cargs)


@app.route('/')
def show_container():
    names = command("lxc", "ls", "-x").strip().split()
    machines = dict()
    for name in names:
        if not name:
            continue
        state = "STOPPED"
        if names.count(name) > 1:
            state = "RUNNING"
        machines[name] = state
    return render_template('overview.html', machines=sorted(machines.items()))

@app.route('/<name>/')
def info(name):
    status = command("lxc", "info", "-n", name, "-s").strip().split()[-1]
    return render_template('details.html', name=name, status=status)


@app.route('/<name>/<action>')
def action(name, action):
    args = [action, "-n", name]
    if action == "start":
        args.append("-d")
    result = command("lxc", *args)
    if action != "info":
        return redirect(url_for('info', name=name))
    else:
        return result

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
