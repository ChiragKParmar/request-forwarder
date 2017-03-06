from flask import Flask, render_template, request, url_for, jsonify, redirect, url_for
from .. import db
from ..models import ProxyUrl
from .forms import RegistrationForm
from . import main
import requests, uuid

@main.route('/')
def index():
    return render_template('index.html')

NOT_ALLOWED_HEADERS = ['Host']
#@app.route('/forward/<int:uuid>', methods=['POST'])
@main.route('/forward', methods=['POST'])
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

@main.route('/create-forward', methods=['GET','POST'])
def create_forward_endpoint():
    proxy_uuid = str(uuid.uuid4())
    form = RegistrationForm()
    if form.validate_on_submit():
        proxy_url = ProxyUrl(
            incoming_url=proxy_uuid,
            outgoing_url=form.outgoing_url.data)
        db.session.add(proxy_url)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('create_forward.html', proxy_uuid=proxy_uuid, host=request.headers['host'], form=form)

@main.route('/send-request', methods=['GET','POST'])
def send_request():
    #Retrieve records from db
    return redirect(url_for('index'))
