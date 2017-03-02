import requests

dictToSend = {'question':'Example question here!'}
res = requests.post('http://localhost:5000/forward', json=dictToSend)
print 'response from server:',res
dictFromServer = res.json()