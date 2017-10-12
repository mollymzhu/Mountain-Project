"""Flask Template for COF SCS"""
import pandas as pd
from datetime import datetime
from flask import render_template, flash, redirect, session, url_for, request, \
                  g, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from flask_admin.base import MenuLink
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from app import app, db, loginmanager, admin
from bokeh.embed import autoload_server, server_document
from bokeh.server.server import Server

from .models import User, Diamond
from .forms import LoginForm, AddRowForm, EditDiamondForm
from .datawarehouse import connect_db, query_to_dict
from .admin import AdminModelView
from .pdlgd import modify_doc

# add a view to manage users; can be accessed at /admin/user
admin.add_view(AdminModelView(User, db.session))
# add a view to manage Redhshift table; can be accessed at /admin/diamond
admin.add_view(AdminModelView(Diamond, db.session))
admin.add_link(MenuLink(name='Back To App', url='/pdlgd'))
bkapp = Application(FunctionHandler(modify_doc))

@app.before_request
def before_request():
    """ Set global user to current user and opens a new database connection if
        there is none yet for the current application context.
    """
    g.user = current_user
    if not hasattr(g, 'db'):
        g.db = connect_db()
    if g.user.is_authenticated:
        g.user.last_seen = datetime.now()


@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()

@loginmanager.user_loader
def load_user(id):
    """Load User from DB"""
    return User.query.get(int(id))

# the route decorator is used to trigger functions
# like showing a page or updating a database
@app.route('/')
@app.route('/index')
@login_required
def index():
    return redirect(url_for('rs'))

@app.route('/pdlgd', methods=['GET', 'POST'])
@login_required
def pdlgd():
    script = server_document('http://localhost:5006/bkapp')
    return render_template("embed.html", script=script, template="Flask")

def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': bkapp}, allow_websocket_origin=["localhost:5000","localhost:5006"])
    server.start()
    server.io_loop.start()

from threading import Thread
Thread(target=bk_worker).start()

#@app.route('/post', methods=['POST'])
#@login_required
#def post():
#    """Route used to update TD; returns empty json response"""
#
#    sql = """
#    sel facly_id, wcis_cnsmr_nm as customer_name, corporate_banking_dept_lvl_3b as segment,curr_pd_ratg as PD,curr_lgd_ratg as LGD, curr_pd_ratg_dt,mpe_curr as MPE,bal_curr as balance from Ud153.rtt576_corporate_banking_risk_ratg_chg
#where curr_pd_ratg not in ('*2','3B','5C')
#and curr_lgd_ratg<>'*2'
#and  facly_stat_type_cd='A'
#and segment<>'WAM'
#and segment<>'Corp. Banking Runoff'
#
#QUALIFY ROW_NUMBER() OVER (PARTITION BY facly_id ORDER BY curr_pd_ratg_dt, mpe_curr DESC)=1
#    """ % (str(request.form['name']).split('|')[0],
#           str(request.form['value']),
#           str(request.form['pk']))
#    # cursor is used to execute SQL statements that don't return anything
#    # e.g. INSERT, UPDATE, or CREATE
#    cursor = g.db.cursor()
#    cursor.execute(sql)
#    # g.db.query(sql) # use noodle to UPDATE TD
#    return jsonify('')
#
#
@app.route('/rs', methods=['GET', 'POST'])
@login_required
def rs():
    """Route to page to edit data in Redshift. Can accept a GET or POST
       request. If POST, update Redhshift with form data. If GET, query
       Redshift and display data."""
    form = EditDiamondForm()
    if form.validate_on_submit():
        d = Diamond.query.filter_by(id=request.form['id']).first()
        d.color = request.form['color']
        d.depth = request.form['depth']
        db.session.add(d)
        db.session.commit()
        flash('Row updated successfully!','success')
        return redirect(url_for('rs'))
    r = Diamond.query.all()
    df = pd.DataFrame(query_to_dict(r))
    return render_template("rs.html", data=df.to_dict('records'), form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Route for login page"""
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('edit'))

    # create an instance of the login form
    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)
    # check if form is valid
    if form.validate_on_submit():
        eid = request.form['eid'].upper()
        password = request.form['password']
        u = User.query.filter_by(eid=eid).first()
        print User.validate_via_ldap(eid, password)
        print u
        # check if eid/pw are valid and if eid is in db of authorized users
        if User.validate_via_ldap(eid, password) and u is not None:
        #if u is not None:
            # update login count
            u.login_ct += 1
            # update last login
            u.last_seen = datetime.now()
            db.session.add(u)
            db.session.commit()
            remember_me = False

            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)

            login_user(u, remember=remember_me)
            flash('Welcome ' + u.eid + '!', 'success')

            return redirect(url_for('pdlgd'))

        else:
            flash('Username or password incorrect', 'warning')
            return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    """Route to logout"""
    logout_user()
return redirect(url_for('login'))
