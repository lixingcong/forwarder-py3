#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

try:
	PYCART_DIR = ''.join(['python-', '.'.join(map(str, sys.version_info[:2]))])
	zvirtenv = os.path.join(os.environ['OPENSHIFT_HOMEDIR'], PYCART_DIR, 'virtenv', 'bin', 'activate_this.py')
	exec(compile(open(zvirtenv).read(), zvirtenv, 'exec'), dict(__file__ = zvirtenv))
except:
	print("Error virtenv");
	pass

#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

help_str="""
<h1>python网络请求转发器</h1>

可以将其部署到任何一个支持WSGI的托管空间。<br>

<code>
Github repo:    https://github.com/lixingcong/forwarder-py3<br>
Inspired from:  https://github.com/seff/forwarder
</code><br>

<h2>用法</h2>
<code>
http://hostedurl?u=url&k=AUTHKEY&t=timeout
</code><br>

解析：<br>
hostedurl: 你搭建的转发服务器的URL<br>
url: 需要转发到url，需要先使用urllib.quote转义，特别是如果有&符号<br>
AUTHKEY: 为了防止滥用，需要提供一个key，为ALLOW_KEYS里面的任何一个值<br>
timeout: [可选]超时时间，默认为30s<br>
"""

__Version__ = "1.0"
__Author__ = "lixingcong"


from wsgiref.util import is_hop_by_hop
import socket, bottle
import urllib.request

ALLOW_KEYS = ('xzSlE','ILbou','DukPL')

application = app = bottle.Bottle()

@app.route(r'/')
def Home():
	resp = bottle.response
	qry = bottle.request.query
	url,k,timeout = qry.u, qry.k, int(qry.get('t','30'))
	if k and k not in ALLOW_KEYS:
		return 'Auth Key is invalid!'

	if url and k:
		url = urllib.request.unquote(url)
		try:
			req = urllib.request.Request(url)
			req.add_header('User-Agent', "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36")
			req.add_header('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
			ret = urllib.request.urlopen(req,timeout=timeout)
			content = ret.read()
			headers = [(n,v) for n,v in ret.info().items() if not is_hop_by_hop(n)]
			cookieadded = False
			for n,v in headers:
				if n == 'Set-Cookie' and cookieadded:
					resp.add_header(n, v)
				else:
					resp.set_header(n, v)
					if n == 'Set-Cookie':
						cookieadded = True
			return content
		except socket.timeout:
			print("ERR: timeout, %s" % (url))
			pass
		except Exception as e:
			print("ERR:%s:%s" % (type(e),str(e)))
			bottle.abort(400)
	else:
		html_content="<html><head><title>Forwarder Url</title></head><body>"+help_str+"</body></html>"
		return html_content

if __name__ == '__main__':
	bottle.run(app, reloader=True)         # run in a local test server
# else:
# 	application=bottle.default_app()       # run in a WSGI server