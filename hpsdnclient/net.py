#!/usr/bin/env python
#
# Copyright (c)  2013 Hewlett-Packard Development Company, L.P.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software  and associated documentation files (the "Software"), to deal
# in the Software without restriction,  including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or  substantial portions of the Software.#
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED,  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR  PURPOSE AND NONINFRINGEMENT.
#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF  OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
#

""" This file implements the Flare Net REST API

/clusters	GET
/clusters/{cluster_uid}/tree	GET
/links	GET
/paths/forward	GET
/arps	GET
/nodes	GET
/lldp	GET
/lldp	POST
/lldp	DELETE
/diag/observations	GET
/diag/observations	POST
/diag/observations	DELETE
/diag/packets	GET
/diag/packets	POST
/diag/packets/{packet_uid}	GET
/diag/packets/{packet_uid}	DELETE
/diag/packets/{packet_uid}/path	GET
/diag/packets/{packet_uid}/nexthop	GET
/diag/packets/{packet_uid}/action	POST

"""

__author__ = 'Dave Tucker, Hewlett-Packard Development Company,'
__version__ = '0.1.0'

import json
import urllib

import rest
import types
from error import FlareApiError

class Net(object):

	def __init__(self):
		pass

	def get_clusters(self):
		""" get_clusters()

			Gets a list of clusters

		"""

		url = 'http://{0}:8080/sdn/v2.0/net/clusters'.format(self.controller)
		r = []
		data = rest.get(url, self.auth_token, 'json')
		for d in data['clusters']:
			r.append(types.JsonObject.factory(d))
		return r

	def get_cluster_tree(self, clusterid):
		""" get_cluster_tree( clusterid)

			Gets the broadcast tree for a specific cluster

		"""
		url = 'http://{0}:8080/sdn/v2.0/net/clusters/{1}/tree'.format(self.controller, clusterid)
		r = []
		data = rest.get(url, self.auth_token, 'json')
		for d in data['cluster']:
			r.append(types.JsonObject.factory(d))
		return r

	def get_links(self):
		""" get_links()

			Returns a list of all links discovered by the SDN controller

		"""
		url = 'http://{0}:8080/sdn/v2.0/net/links'.format(self.controller)
		r = []
		data = rest.get(url, self.auth_token, 'json')
		for d in data['links']:
			r.append(types.JsonObject.factory(d))
		return r

	def get_forward_path(self, src_dpid, dst_dpid):
		""" get_forward_path()

			Gets the shortest computed path between src_dpid and dst_dpid

		"""
		url = 'http://{0}:8080/sdn/v2.0/paths/forward?src_dpid={1}&dst_dpid={2}'.format(self.controller, urllib.quote(src_dpid), urllib.quote(dst_dpid))
		r = []
		data = rest.get(url, self.auth_token, 'json')
		for d in data['path']:
			r.append(types.JsonObject.factory(d))
		return r

	def get_arps(self, vid, ip):
		""" get_arps()

			Provides ARP details for the given IP address and VLAN ID

		"""
		url = 'http://{0}:8080/sdn/v2.0/net/arps'.format(self.controller)
		
		if vid and not ip:
			url = url + "?vid={0}".format(vid, ip)			
		elif vid and ip:
			url = url + "?vid={0}&ip={1}".format(vid, ip)

		data = rest.get(url, self.auth_token, 'json')
		r = []
		
		for d in data['nodes']:
			r.append(types.JsonObject.factory(d))
		return r

	def get_nodes(self, ip=None, vid=None, dpid=None, port=None):
		""" get_nodes()
			
			Provides the end node detail for the given IP address and VID
			Provides the end node list for a given VID
			Provides the end node list for a given datapath ID
			Provides the end node list for a given datapath ID and port
		
		"""
		url = 'http://{0}:8080/sdn/v2.0/net/nodes'.format(self.controller)
		
		if vid and not ip:
			url = url + "?vid={0}".format(vid, ip)			
		elif vid and ip:
			url = url + "?vid={0}&ip={1}".format(vid, ip)
		elif dpid and not port:
			url = url + "?dpid={0}".format(urllib.quote(dpid))
		elif dpid and port:
			url = url + "?dpid={0}&port={1}".format(urllib.quote(dpid),port)

		data = rest.get(url, self.auth_token, 'json')
		r = []
		
		for d in data['nodes']:
			r.append(types.JsonObject.factory(d))
		return r

	def get_lldp(self):
		""" get_lldp()

			Gets a list of LLDP supressed ports from the SDN Controller

		"""
		url = 'http://{0}:8080/sdn/v2.0/lldp'.format(self.controller)
		r = []
		data = rest.get(url, self.auth_token, 'json')
		for d in data['path']:
			r.append(types.JsonObject.factory(d))
		return r

	def set_lldp(self, ports):
		""" set_lldp()

			Puts selected ports in to LLDP suppressed state

		"""
		url = 'http://{0}:8080/sdn/v2.0/lldp'.format(self.controller)
		r = rest.post(url, self.auth_token, json.dumps(ports))

	def delete_lldp(self, ports):
		""" delete_lldp()

			Removes ports from LLDP suppressed state

		"""
		url = 'http://{0}:8080/sdn/v2.0/lldp'.format(self.controller)
		r = rest.delete(url, self.auth_token, json.dumps(ports))

	def get_diag_observations(self):
		""" get_diag_observations()

			Not yet implemented

		"""
		pass

	def set_diag_observations(self):
		""" set_diag_observations()

			Not yet implemented

		"""
		pass

	def delete_diag_observations(self):
		""" delete_diag_observations()

			Not yet implemented

		"""
		pass

	def get_diag_packets(self):
		""" get_diag_packets()

			Not yet implemented

		"""
		pass

	def set_diag_packets(self):
		""" set_diag_packets()

			Not yet implemented

		"""
		pass

	def get_diag_packet_detail(self):
		""" get_diag_packet_detail()

			Not yet implemented

		"""
		pass

	def delete_diag_packet(self):
		""" delete_diag_packet()

			Not yet implemented

		"""
		pass

	def get_diag_packet_path(self):
		""" get_diag_packet_path()

			Not yet implemented

		"""
		pass

	def get_diag_packet_nexthop(self):
		""" get_diag_packet_nexthop()

			Not yet implemented

		"""
		pass

	def set_diag_packet_action(self):
		""" set_diag_packet_action()

			Not yet implemented

		"""
		pass