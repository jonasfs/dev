#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 jonasfscc <jonasfscc@gmail.com>
#

import json
import os
import sys
from time import sleep
from django.core.management import utils

from deploy_utils import call_command

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
aws = {}

# check for files that shouldn't be here
if os.path.isfile('./zappa_settings.json'):
	print('')
	print('\tA zappa_settings.json file already exists on the project dir and')
	print('\tthis script doesnt handle updates. Delete zappa_settings.json')
	print('\tand run this script again for a new full project deploy or')
	print('\thandle your project updates manually\n')
	sys.exit(0)

# create stack
msg = 'Enter your amazon credentials profile name (default \'default\'):'
amazon_user = input(msg)
if amazon_user == '':
	print(amazon_user)
stack_name = input('Enter the stack name: ')
parm_name = input('Enter the DB name: ')
parm_user = input('Enter the DB master username: ')
parm_pass = input('Enter the DB master password: ')
aws['STACKNAME'] = stack_name

cmd = 'aws cloudformation create-stack --stack-name ' + aws['STACKNAME']
cmd += ' --template-body file://./cloudformation.yaml'
cmd += ' --parameters ParameterKey=DBUSERNAME,ParameterValue=' + parm_user
cmd += ' ParameterKey=DBPASSWORD,ParameterValue=' + parm_pass
cmd += ' ParameterKey=DBNAME,ParameterValue=' + parm_name
print(cmd)
cmd_result = call_command(cmd)

# check stack
cmd = 'aws cloudformation describe-stacks --stack-name ' + aws['STACKNAME']
print(cmd)
stack_status = 'CREATE_IN_PROGRESS'
while stack_status == 'CREATE_IN_PROGRESS':
	for i in range(30, 1, -1):
		message = '\r'
		message += 'Checking if stack was created, trying again in '
		message += str(i) + ' second'
		if i > 1:
			message += 's'
		print(message, end='     ')
		sleep(1)
	cmd_result = call_command(cmd)
	result_json = json.loads(cmd_result.stdout)['Stacks'][0]
	stack_status = result_json['StackStatus']

print('\n' + stack_status)
if stack_status != 'CREATE_COMPLETE':
	print('Something went wrong during the CloudFormation stack creation')
	sys.exit(0)

outputs = result_json['Outputs']
for output in outputs:
	key = output['OutputKey']
	value = output['OutputValue']
	aws[key] = value

# setup backend with zappa
aws['SECRETKEY'] = utils.get_random_secret_key()

with open('env.json', 'w') as stream:
	json.dump(aws, stream, indent=4)

cmd = 'zappa init'
print(cmd)
cmd_result = call_command(cmd, '\n' + amazon_user + '\n\ndev.settings\n\n\n')

zappa_json = None
with open('zappa_settings.json', 'r') as stream:
	zappa_json = json.load(stream)

zappa_json['dev']['exclude'] = ['front']
with open('zappa_settings.json', 'w') as stream:
	json.dump(zappa_json, stream, indent=4)

cmd = 'zappa deploy dev'
cmd_result = call_command(cmd)
print(cmd_result.stdout)

cmd = 'zappa status dev'
cmd_result = call_command(cmd)
results = cmd_result.stdout.split('\n')
result_msg = ""
while ('http' not in result_msg) and (len(results) > 0):
	result_msg = results.pop()
url_start = result_msg.find('http')
backend_url = result_msg[url_start:]
aws['BACKENDURL'] = backend_url

with open('env.json', 'w') as stream:
	json.dump(aws, stream, indent=4)

# updating api url on local_settings KNOWN_HOSTS
cmd = 'zappa update dev'
cmd_result = call_command(cmd)

# init database
cmd = 'zappa manage dev migrate'
cmd_result = call_command(cmd)

# setup frontend
with open('front/config/prod.env.js', 'w') as stream:
	stream.write('\'use strict\'\n')
	stream.write('module.exports = {\n')
	stream.write('\tNODE_ENV: \'"production"\',\n')
	api_url = aws['BACKENDURL'] + '/api/'
	stream.write('\tROOT_API: \'"' + api_url + '"\'\n')
	stream.write('}')

# build

cmd = 'npm run build'
cmd_result = call_command(cmd, cwd=BASE_DIR + '/front')

cmd = 'aws s3 sync ./dist s3://' + aws['BUCKETNAME']
cmd_result = call_command(cmd, cwd=BASE_DIR + '/front')
