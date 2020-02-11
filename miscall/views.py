"""
	FBV (Function Based View)
"""

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
import requests
import json




def index(request):
	return render(request,'miscall/index.html')


def reqotp(request):
	
	APIKEY = 'Your API KEY'
	msisdn = request.POST.get('phone')

	if msisdn == '':
		return_response = {
			'error': True,
			'info': 'Phone Number Cannot empty'
		}
		return JsonResponse(return_response)
	
	if 'trying' not in request.session:
		gateway = 0
		request.session['gateway'] = gateway
	else:
		gateway = request.session['gateway'] + 1
		if gateway > 4 :
			gateway = 0
		request.session['gateway'] = gateway

	base_url = "http://104.199.196.122/gateway"
	version = "/v3"
	action = "/asynccall"

	url = base_url + version + action
	data = {
		'msisdn':msisdn,
		'gateway':gateway
	}


	content = json.dumps(data)

	headers = {
		"Content-Type":"application/json",
		"Authorization": 'Apikey '+ APIKEY,
		"Content-Length":str(len(content))
	}

	r = requests.post(url,data=content,headers=headers)
	response_json = r.json()
	print(response_json) # debugging, you can comment this line
		
	rc = response_json['rc']
	error = True

	if rc == 0:
		error = False
		token = response_json['token']
		trxid = response_json['trxid']
		request.session['token'] = token
		request.session['trxid'] = trxid
		first_token = token[0:-4]
		length = len(token)
		this_return = {
			'error':error,
			'trxid':trxid,
			'first_token':first_token,
			'length':length
		}
	else:
		info = response_json['info']
		this_return = {
			'error':error,
			'info':info
		}

	print(this_return) # debugging, you can comment this line
	return JsonResponse(this_return)



def verify(request):
	if 'trxid' not in request.session or 'token' not in request.session:
		this_return = {
			'error': True,
			'info': 'Please do request first'
		}
		print(this_return) # debugging, you can comment this line
		return JsonResponse(this_return)

	code = request.POST.get('code')
	trxid = request.POST.get('trxid')

	error = True

	if code == "" or trxid == "":
		info = "Cannot empty"
	else:
		if code == request.session['token'] and trxid == request.session['trxid']:
			info = "Success"
			error = False
			request.session.flush()
		else:
			info = "Wrong Code"

	this_return = {
		'error':error,
		'info':info
	}
	print(this_return) # debugging, you can comment this line
	return JsonResponse(this_return)


	






