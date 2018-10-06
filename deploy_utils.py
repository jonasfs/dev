#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 jonasfscc <jonasfscc@gmail.com>
#

import subprocess
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def call_command(string, input=None, cwd=BASE_DIR):
	cmd = string.split(' ')
	output = subprocess.run(
		cmd,
		stdout=subprocess.PIPE,
		encoding="utf-8",
		input=input,
		cwd=cwd
	)
	return output
