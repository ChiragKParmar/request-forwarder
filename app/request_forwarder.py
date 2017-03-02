from flask import Flask, render_template, request, url_for, jsonify, redirect, url_for
from flask_bootstrap import Bootstrap
import requests, uuid
import os
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.fields import (BooleanField, PasswordField, StringField,
                            SubmitField)
from wtforms.validators import Email, EqualTo, InputRequired, Length
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'myverylongsecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


NOT_ALLOWED_HEADERS = ['Host']


class RegistrationForm(FlaskForm):
    outgoing_url = StringField('Outgoing URL', validators=[InputRequired(), Length(1, 64)])
    submit = SubmitField('submit')

class ProxyUrl(db.Model):
    __tablename__ = 'proxy'
    id = db.Column(db.Integer, primary_key=True)
    incoming_url = db.Column(db.String(64), unique=True)
    outgoing_url = db.Column(db.String(64))

    def __repr__(self):
        return '<ProxyUrl %r>' % self.incoming_url

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

#@app.route('/forward/<int:uuid>', methods=['POST'])
@app.route('/forward', methods=['POST'])
def request_forwarder():
    headers= {}
    MAX_RETRIES = 10
    # proxy_url = get_url_list_from_database_by(uuid)

    for hi in request.headers:
    	if hi[0] not in NOT_ALLOWED_HEADERS:
    		headers[hi[0]]=request.headers.get(hi[0])

    proxy_url = ['http://requestb.in/15tkd7q1', 'http://requestb.in/1krh6n61']
    for url in proxy_url:
    	attempt = 0
    	while (attempt < MAX_RETRIES):
    		res = requests.post(url=url, data=request.data, headers=headers)
    		if res.status_code > 399:
    			res = requests.post(url=url, data=request.data, headers=headers)
    			attempt += 1
    		else:
    			print res.status_code
    			break


    return jsonify(' ', 200)

@app.route('/create-forward', methods=['GET','POST'])
def create_forward_endpoint():
    proxy_uuid = str(uuid.uuid4())
    form = RegistrationForm()
    if form.validate_on_submit():
        proxy_url = ProxyUrl(
            incoming_url=proxy_uuid,
            outgoing_url=form.outgoing_url.data)
        db.session.add(proxy_url)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_forward.html', proxy_uuid=proxy_uuid, host=request.headers['host'], form=form)

@app.route('/send-request', methods=['GET','POST'])
def send_request():
    #Retrieve records from db
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
