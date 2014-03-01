from flask import Flask, redirect, url_for, \
             render_template
import lxc

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def machinesorter(m):
    order = ['RUNNING', 'FROZEN', 'PAUSED']
    if m.state in order:
        nr = order.index(m.state)
    else:
        nr = 9
    return "%s%s" % (nr, m.name)

@app.route('/')
def show_container():
    classmap = {'RUNNING': 'text-success',
                'STOPPED': 'text-error',
               }
    names = lxc.list_containers()
    machines = list()
    for name in names:
        machine = lxc.Container(name)
        machine.klass = classmap.get(machine.state, 'text-warning')
        machines.append(machine)
    return render_template('overview.html', machines=sorted(machines, key=machinesorter))

@app.route('/<name>/')
def info(name):
    return render_template('details.html', machine=l.getMachine(name))


@app.route('/<name>/<action>')
def action(name, action):
    m = lxc.Container(name)
    result = getattr(m, action)()
    if action != "info":
        return redirect(url_for('show_container'))
    else:
        return result

@app.route('/<name>/delete')
def deleteMachine(name):
    m = lxc.Container(name)
    m.destroy()
    return redirect(url_for('show_container'))

@app.route('/<name>/clone/<newname>')
def clone(name, newname):
    m = lxc.Container(name)
    m.clone(newname)
    return redirect(url_for('show_container'))



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
