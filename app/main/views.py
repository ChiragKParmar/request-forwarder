from flask import Flask, render_template, request, url_for, jsonify, redirect, url_for
from .. import db
from ..models import Bucket, Destination
from .forms import RegistrationForm, BucketForm, DestinationForm
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

def _get_user():
    return current_user.username if current_user.is_authenticated else None

@main.rout('/create-bucket', methods=['GET', 'POST'])
def create_bucket():
    proxy_uuid = str(uuid.uuid4())
    form = BucketForm()
    if form.validate_on_submit():
        # TODO update following logic to save bucket data with
        # end point
        proxy_url = ProxyUrl(
            incoming_url=proxy_uuid,
            outgoing_url=form.outgoing_url.data)
        db.session.add(proxy_url)
        db.session.commit()
        return redirect(url_for('main.bucket')) #TODO create bucket.html page (overview page)
    return render_template('create_forward.html', proxy_uuid=proxy_uuid, host=request.headers['host'], form=form)

@main.route('/add-destination', methods=['GET','POST'])
def add_destination_endpoint():
    form = DestinationForm(destination_endpoint=request.form.get.('destination_endpoint'))
    if form.validate_on_submit():
        bucket = Bucket(created_by=_get_user()).save()
        return redirect(url_for('.index'))
    return render_template('create_forward.html', , form=form)

@main.route('/send-request', methods=['GET','POST'])
def send_request():
    #Retrieve records from db
    return redirect(url_for('.index'))
