#!/usr/bin/python
# -*- coding: utf-8 -*-

# generate invite code using sha256
import hashlib
import re

def generateInviteCode(prefix, id):
    origin = prefix + str(id)

    hex_output = hashlib.sha256(origin.encode('utf-8')).hexdigest()
    hex_output = hashlib.sha256(hex_output.encode('utf-8')).hexdigest()
    result = (prefix + hex_output[-5:]).upper()
    return result

def isInviteCode(prefix, text):
    pattern = "^%s[A-F0-9]{5}" % prefix
    print(pattern)
    pattern = re.compile(pattern)
    return re.match(pattern, text)
