from flask import Flask, render_template, request, url_for, jsonify
from flask_bootstrap import Bootstrap
import requests, uuid

app = Flask(__name__)
bootstrap = Bootstrap(app)

NOT_ALLOWED_HEADERS = ['Host']


@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
    
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
    form = CreateProxy()
    proxy_uuid = uuid.uuid4()
    #insert uuid in the db
    #send uuid to ui
    #get at least one proxy url from the ui
    #update db to insert proxy url
    return render_template('create_forward.html', proxy_uuid=proxy_uuid, host=request.headers['host'])

if __name__ == '__main__':
    app.run(debug=True)	