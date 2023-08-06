import platform

if platform.system() != "Java":
    print("Load this file inside jython, if you need the stand-alone tool run: inql")
    exit(-1)

try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer

try:
    import urllib.request as urllib_request # for Python 3
except ImportError:
    import urllib2 as urllib_request # for Python 2 and Jython

import threading
import json

from java.awt.event import ActionListener
from javax.swing import JMenuItem
from org.python.core.util import StringUtil

try:
    from burp import IProxyListener, IContextMenuFactory
except ImportError:
    IProxyListener = object
    IContextMenuFactory = object

from inql.constants import *
from inql.utils import string_join, override_headers, make_http_handler, HTTPRequest, is_query
from inql.actions.browser import URLOpener


class OmniMenuItem(IContextMenuFactory):
    """Menu item for burp and inql interface. IT contains same action but it is shown in multiple places"""
    def __init__(self, helpers=None, callbacks=None, text=''):
        self._helpers = helpers
        self._callbacks = callbacks
        self.menuitem = JMenuItem(text)
        self._burp_menuitem = JMenuItem("inql: %s" % text)
        self.set_enabled(False)
        self._callbacks.registerContextMenuFactory(self)

    def add_action_listener(self, action_listener):
        """
        add a new action listener to the given UI items.
        """
        self._action_listener = action_listener
        self.menuitem.addActionListener(action_listener)
        self._burp_menuitem.addActionListener(action_listener)

    def set_enabled(self, enabled):
        """
        Enables or disables the menuitme
        """
        self.menuitem.setEnabled(enabled)
        self._burp_menuitem.setEnabled(enabled)

    def createMenuItems(self, invocation):
        """
        Overrides IContextMenuFactory callback

        :param invocation: handles menu selected invocation
        :return:
        """
        try:
            r = invocation.getSelectedMessages()[0]
            info = self._helpers.analyzeRequest(r)
            url = str(info.getUrl())
            body = r.getRequest()[info.getBodyOffset():].tostring()
            if not is_query(body):
                return None
            for h in info.getHeaders():
                if h.lower().startswith("host:"):
                    domain = h[5:].strip()

            self._action_listener.ctx(fname='dummy.query', host=domain, payload=body)
            mymenu = []
            mymenu.append(self._burp_menuitem)
        except Exception as ex:
            return None
        return mymenu


class SimpleMenuItem:
    """
    An OmniMenuItem implemented on top of a single item entry.
    """
    def __init__(self, text=None):
        self.menuitem = JMenuItem(text)
        self.menuitem.setEnabled(False)

    def add_action_listener(self, action_listener):
        self.menuitem.addActionListener(action_listener)

    def set_enabled(self, enabled):
        self.menuitem.setEnabled(enabled)


class EnhancedHTTPMutator(IProxyListener):
    """
    An implementation of an HTTPMutater which employs the Burp Utilities to enhance the requests
    """
    def __init__(self, callbacks=None, helpers=None, overrideheaders=None, requests=None, stub_responses=None):
        self._requests = requests if requests is not None else {}
        self._overrideheaders = overrideheaders if overrideheaders is not None else {}
        self._overrideheaders = overrideheaders if overrideheaders is not None else {}
        self._index = 0
        self._stub_responses = stub_responses if stub_responses is not None else {}

        if helpers and callbacks:
            self._helpers = helpers
            self._callbacks = callbacks
            self._callbacks.registerProxyListener(self)
            for r in self._callbacks.getProxyHistory():
                self._process_request(self._helpers.analyzeRequest(r), r.getRequest())


    def _process_request(self, reqinfo, reqbody):
        """
        Process request and extract key values

        :param reqinfo:
        :param reqbody:
        :return:
        """
        url = str(reqinfo.getUrl())
        if is_query(reqbody[reqinfo.getBodyOffset():].tostring()):
            for h in reqinfo.getHeaders():
                if h.lower().startswith("host:"):
                    domain = h[5:].strip()

            method = reqinfo.getMethod()
            try:
                self._requests[domain]
            except KeyError:
                self._requests[domain] = {'POST': None, 'PUT': None, 'GET': None, 'url': None}
            self._requests[domain][method] = (reqinfo, reqbody)
            self._requests[domain]['url'] = url

    def processProxyMessage(self, messageIsRequest, message):
        """
        Implements IProxyListener method

        :param messageIsRequest: True if BURP Message is a request
        :param message: message content
        :return: None
        """
        if self._helpers and self._callbacks and messageIsRequest:
            self._process_request(self._helpers.analyzeRequest(message.getMessageInfo()),
                                  message.getMessageInfo().getRequest())

    def get_graphiql_target(self, server_port, host=None, query=None, variables=None):
        base_url = "http://localhost:%s/%s" % (server_port, self._requests[host]['url'])
        arguments = ""
        if query or variables:
            arguments += '?'
            args = []
            if host:
                args.append("query=%s" % urllib_request.quote(query))
            if variables:
                args.append("variables=%s" % urllib_request.quote(json.dumps(variables)))
            arguments += "&".join(args)

        return base_url + arguments

    def has_host(self, host):
        try:
            self._requests[host]
            return True
        except KeyError:
            return False

    def build_python_request(self, endpoint, host, payload):
        req = self._requests[host]['POST'] or self._requests[host]['PUT'] or self._requests[host]['GET']
        if req:
            original_request = HTTPRequest(req[1])
            del original_request.headers['Content-Length']

            # TODO: Implement custom headers in threads. It is not easy to share them with the current architecture.
            return urllib_request.Request(endpoint, payload, headers=original_request.headers)

    def get_stub_response(self, host):
        return self._stub_responses[host] if host in self._stub_responses else None

    def set_stub_response(self, host, payload):
        self._stub_responses[host] = payload

    def send_to_repeater(self, host, payload):
        req = self._requests[host]['POST'] or self._requests[host]['PUT'] or self._requests[host]['GET']
        if req and self._callbacks and self._helpers:
            info = req[0]
            body = req[1]
            nobody = body[:info.getBodyOffset()].tostring()
            rstripoffset = info.getBodyOffset()-len(nobody.rstrip())
            headers = body[:info.getBodyOffset()-rstripoffset].tostring()

            try:
                self._overrideheaders[host]
            except KeyError:
                self._overrideheaders[host] = []

            headers = override_headers(headers, self._overrideheaders[host])
            repeater_body = StringUtil.toBytes(string_join(
                headers,
                body[info.getBodyOffset()-rstripoffset:info.getBodyOffset()].tostring(),
                payload))

            self._callbacks.sendToRepeater(info.getUrl().getHost(), info.getUrl().getPort(),
                                           info.getUrl().getProtocol() == 'https', repeater_body,
                                          'GraphQL #%s' % self._index)
            self._index += 1


class RepeaterSenderAction(ActionListener):
    """
    Class represeintg the action of sending something to BURP Repeater
    """
    def __init__(self, omnimenu, http_mutator):
        self._http_mutator = http_mutator
        self._omnimenu = omnimenu
        self._omnimenu.add_action_listener(self)
        self.menuitem = self._omnimenu.menuitem
        self._host = None
        self._payload = None
        self._fname = None

    def actionPerformed(self, e):
        """
        Overrides ActionListener behaviour. Send current query to repeater.

        :param e: unused
        :return: None
        """
        self._http_mutator.send_to_repeater(self._host, self._payload)

    def ctx(self, host=None, payload=None, fname=None):
        """
        When a fname is specified and is a query file or a request is selected in the other tabs,
        enables the context menu to send to repeater tab

        :param host: should be not null
        :param payload: should be not null
        :param fname: should be not null
        :return: None
        """
        self._host = host
        self._payload = payload
        self._fname = fname

        if not self._fname.endswith('.query'):
            self._omnimenu.set_enabled(False)
            return

        if self._http_mutator.has_host(host):
            self._omnimenu.set_enabled(True)
        else:
            self._omnimenu.set_enabled(False)


class GraphiQLSenderAction(ActionListener):
    """
    Class representing the action of sending something to the provided graphiql server
    """
    def __init__(self, omnimenu, http_mutator):
        self._http_mutator = http_mutator
        self._omnimenu = omnimenu
        self._omnimenu.add_action_listener(self)
        self.menuitem = self._omnimenu.menuitem
        self._server = HTTPServer(('127.0.0.1', 0), make_http_handler(http_mutator))
        t = threading.Thread(target=self._server.serve_forever)
        #t.daemon = True
        t.start()

    def actionPerformed(self, e):
        """
        Override the ActionListener method. Usually setup in combination with a menuitem click.
        :param e: unused
        :return:
        """
        content = json.loads(self._payload)
        if isinstance(content, list):
            content = content[0]

        URLOpener().open(self._http_mutator.get_graphiql_target(
            self._server.server_port, self._host,
            content['query'] if 'query' in content else None,
            content['variables'] if 'variables' in content else None))

    def ctx(self, host=None, payload=None, fname=None):
        """
        When a fname is specified and is a query file or a request is selected in the other tabs,
        enables the context menu to send to repeater tab

        :param host: should be not null
        :param payload: should be not null
        :param fname: should be not null
        :return: None
        """
        self._host = host
        self._payload = payload
        self._fname = fname

        if not self._fname.endswith('.query'):
            self._omnimenu.set_enabled(False)
            return

        if self._http_mutator.has_host(host):
            self._omnimenu.set_enabled(True)
        else:
            self._omnimenu.set_enabled(False)