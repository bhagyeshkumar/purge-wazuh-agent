#!/usr/bin/python3
# Written by Bhagyesh Parmar [bhagyeshinfosec@gmail.com]

import os
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# REPLACE WITH IP or HOST NAME BELOW. e.g localhost, example.com, 127.0.0.1
host = 'lab.bhagyesh.ml'

def get_auth_token(user,pwd):

    TOKEN = requests.get(f'https://{host}:55000/security/user/authenticate', params=(('raw', 'true'),), verify=False, auth=(user,pwd))
    
    return TOKEN.text
    
# PROVIDE WAZUH API USER & PASSWORD HERE.
auth_token = get_auth_token('wazuh','wazuh')
    
def get_disconnected(Platform,Older_than):
    
	agent_list = []
	
	headers = {
	    'Authorization': f"Bearer {auth_token}",
	}

	params = (
	    ('select', 'name'),
	    ('os.platform', Platform),
	    ('status', 'disconnected'),
	    ('older_than', Older_than),
	    ('pretty', 'true'),
	)

	response = requests.get(f'https://{host}:55000/agents', headers=headers, params=params, verify=False)
	
	agent_dict = json.loads(response.text)['data']['affected_items']
	
	for agent in agent_dict:
		agent_list.append(agent['id'])
	
	list_to_string = ",".join(agent_list)
	
	#print(list_to_string)
	
	return list_to_string

def del_disconnected(Platform,Older_than):
	
	headers = {
	    'Authorization': f"Bearer {auth_token}",
	}
	
	# Calling Get_Disconnect method to get agent_list
	#agents_list = get_disconnected(Platform, Older_than)
	
	params = (
	    #('os.platform', Platform),
	    ('status', 'disconnected'),
	    ('older_than', '0s'),
	    ('agents_list', get_disconnected(Platform, Older_than)),
	    ('pretty', ''),
	)
	
	# DELETE /agents?older_than=0s&status=disconnected&agents_list=39038,39491,
	response = requests.delete(f'https://{host}:55000/agents', headers=headers, params=params, verify=False)

	return response.text
	
def del_neverconnected():
	
	headers = {
	    'Authorization': f"Bearer {auth_token}",
	}

	params = (
	    ('status', 'neverconnected'),
	    ('older_than', '7d'),
	    ('pretty', ''),
	)

	response = requests.delete(f'https://{host}:55000/agents', headers=headers, params=params, verify=False)

	return response.text

# e.g. del_disconnected(Platform, older_than)
# platfrom = amzn, ubuntu, centos, opensuse, windows
# older_than = 0s,21d,1m,1y

del_disconnected('amzn', '3d')

del_disconnected('ubuntu', '3d')

#del_disconnected('windows', '21d')

#del_neverconnected()

