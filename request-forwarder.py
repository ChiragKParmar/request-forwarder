from flask import Flask, render_template, request, url_for, jsonify
import requests
app = Flask(__name__)

NOT_ALLOWED_HEADERS = ['Host']
@app.route('/forward', methods=['POST'])
def request_forwarder():
    headers= {}
    MAX_RETRIES = 10

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

if __name__ == '__main__':
    app.run(debug=True)	