#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 jonasfscc <jonasfscc@gmail.com>

import os
import yaml
from deploy_utils import call_command

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE_DIR, 'env.yaml')
aws = {}

with open(path, 'r') as stream:
	aws = yaml.load(stream)

cmd = 'npm run build'
cmd_result = call_command(cmd, cwd=BASE_DIR + '/front')

cmd = 'aws s3 sync ./dist s3://' + aws['BUCKETNAME']
cmd_result = call_command(cmd, cwd=BASE_DIR + '/front')
