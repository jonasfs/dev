#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 jonasfscc <jonasfscc@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABb4WHo94UEAo63XozI4RTdk_SGL0qPZkopcN_jJVHZnygfEby15jw6IamoQqBAsaW8bTnheQ1AOuXGQ3abMHnpvLdWXkV9C4z7Mt_c8zkpyL_CIJFyS3anZZkCz908ybjbIiNyy1v-RQzxq2jQqgYx3bcvvY_0U5MTKDGAsra83eLo-hl_p0s4A_H3LS03EIBP-yC3'

f = Fernet(key)
print(f.decrypt(message))


