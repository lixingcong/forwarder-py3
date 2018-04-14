#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os

try:
	zvirtenv = os.path.join(os.environ['OPENSHIFT_HOMEDIR'], PYCART_DIR, 'virtenv', 'bin', 'activate_this.py')
	exec(compile(open(zvirtenv).read(), zvirtenv, 'exec'), dict(__file__ = zvirtenv))
except:
	print("Error virtenv");
	pass



import bottle
from bottle import get, post, request


@get('/my_form')
def show_form():
	return '''\
<form action="" method="POST">
    <label for="name">What is your name?</label>
    <input type="text" name="name"/>
    <input type="submit"/>
</form>'''

@post('/my_form')
def show_name():
	return "Hello, {}!".format(request.POST.name)

if __name__ == '__main__': #for debug
	bottle.run(host='localhost', port=8080) # run in a local test server
else:
	application=bottle.default_app()       # run in a WSGI server