#!/usr/bin/env python
#
# Copyright (c)  2013 Hewlett-Packard Development Company, L.P.
#
# Permission is hereby granted, fpenrlowee of charge, to any person
# obtaining a copy of this software  and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Implementation of the Flare OpenFlow REST API"""

__author__ = 'Dave Tucker, Hewlett-Packard Development Company,'
__version__ = '0.2.0'

import json
import urllib

from hpsdnclient.api import ApiBase
import hpsdnclient.rest as rest
import hpsdnclient.datatypes as datatypes
from hpsdnclient.error import FlareApiError

class OfMixin(ApiBase):

    def __init__(self, controller, auth):
        super(OfMixin, self).__init__(controller, auth)
        self._of_base_url = ("https://{0}:8443".format(self.controller) +
                             "/sdn/v2.0/of/")

    # STATS #
    def get_stats(self):
        """List controller statistics for all controllers that are
        part of this controller's team."""
        url = self._of_base_url + 'stats'
        result = []
        try:
            r = rest.get(url, self.auth)
            data = r.json()
        except Exception as e:
            raise FlareApiError('Something went wrong with your request. '
                                '{0}'.format(e))
        for d in data['controller_stats']:
            result.append(datatypes.JsonObject.factory(d))
        return result

    def get_port_stats(self, dpid, port_id=None):
        """List all port statistics for a given datapath or for a
        given datapath and port number"""
        url = (self._of_base_url + 'stats/ports?' +
               'dpid={0}'.format(urllib.quote(dpid)))
        if port_id:
            url = url + '&port_id={0}'.format(port_id)
        result = []
        try:
            r = rest.get(url, self.auth)
            data = r.json()
        except Exception as e:
            raise FlareApiError('Something went wrong with your request. '
                                '{0}'.format(e))

        for d in data['stats']:
            result.append(datatypes.JsonObject.factory(d))
        return result

    def get_group_stats(self, dpid, group_id=None):
        """List group statistics"""
        url = (self._of_base_url + 'stats/groups?' +
               'dpid={0}'.format(urllib.quote(dpid)))
        if group_id:
            url = url + '&port_id={0}'.format(group_id)

        try:
            r = rest.get(url, self.auth)
            data = r.json()
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))
        return datatypes.JsonObject.factory(data)

    def get_meter_stats(self, dpid, meter_id):
        """List meter statistics"""
        url = (self._of_base_url + 'stats/meters?' +
               'dpid={0}&meter={1}'.format(urllib.quote(dpid), meter_id))
        try:
            r = rest.get(url, self.auth)
            data = r.json()
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))
        return datatypes.JsonObject.factory(data)

    def get_datapaths(self):
        """List all datapaths that are managed by this controller."""
        url = self._of_base_url + 'datapaths'
        try:
            r = rest.get(url, self.auth)
            data = r.json()
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))

        result = []
        for d in data['datapaths']:
            result.append(datatypes.JsonObject.factory(d))
        return result

    def get_datapath_detail(self, dpid):
        """Get detail information on a datapath."""
        url = (self._of_base_url + 'datapaths/{0}'.format(urllib.quote(dpid)))
        try:
            r = rest.get(url, self.auth)
            data = r.json()
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))
        return datatypes.JsonObject.factory(data['datapath'])

    def get_datapath_meter_features(self, dpid):
        """Get datapath meter features"""

        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               'features/meter')
        try:
            r = rest.get(url, self.auth)
            data = r.json()
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))
        return datatypes.JsonObject.factory(data['meter_features'])

    def get_datapath_group_features(self, dpid):
        """Get datapath group features"""
        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               '/features/groups')
        try:
            r = rest.get(url, self.auth)
            data = r.json()
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))
        return datatypes.JsonObject.factory(data['group_features'])

    def get_ports(self, dpid):
        """ Gets a list of ports from the specified DPID"""
        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               'ports')
        try:
            r = rest.get(url, self.auth)
            data = r.json()
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))
        result = []
        for d in data['ports']:
            result.append(datatypes.JsonObject.factory(d))
        return result

    def get_port_detail(self, dpid, port_id):
        """Gets detailed port information for the specified port"""
        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               'ports/{0}'.format(port_id))
        try:
            r = rest.get(url, self.auth)
            data = r.json()
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))
        return datatypes.JsonObject.factory(data['port'])

    def get_meters(self, dpid):
        """List all meters configured on the supplied DPID"""
        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               'meters')
        try:
            r = rest.get(url, self.auth)
            data = r.json()
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))
        return datatypes.JsonObject.factory(data)

    def add_meters(self, dpid, meters):
        """Add a new meter to the supplied DPID"""
        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               'meters')
        try:
            rest.post(url, self.auth, json.dumps(meters.to_dict()))
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))

    def get_meter_details(self, dpid, meter_id):
        """Get detailed meter information"""
        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               'meters/{0}'.format(meter_id))
        try:
            r = rest.get(url, self.auth)
            data = r.json()
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))
        return datatypes.JsonObject.factory(data)

    def update_meter(self, dpid, meter_id, meter):
        """ Update the specified meter"""
        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               'meters/{0}'.format(meter_id))
        try:
            rest.put(url, self.auth, meter)
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))

    def delete_meter(self, dpid, meter_id):
        """Delete a meter corresponding to the supplied meter_id"""
        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               'meters/{0}'.format(meter_id))
        try:
            rest.delete(url, self.auth)
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))

    def get_flows(self, dpid):
        """Gets a list of flows on the supplied DPID"""
        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               'flows')
        try:
            r = rest.get(url, self.auth)
            data = r.json()
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))
        result = []
        for d in data['flows']:
            result.append(datatypes.JsonObject.factory(d))
        return result

    def add_flows(self, dpid, flows):
        """Add a flow, or flows to the selected DPID"""
        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               'flows')
        if isinstance(flows, list):
            tmp = []
            for f in flows:
                if isinstance(f, datatypes.Flow):
                    tmp.append(f.to_dict())
                else:
                    raise FlareApiError("Invalid argument. Expected "
                                        "datatypes.Flow or a list of "
                                        "datatypes.Flow")
            data = { "flows" : tmp }
        elif isinstance(flows, datatypes.Flow):
            data = { "flow" : flows.to_dict() }
        else:
            raise FlareApiError("Invalid argument. Expected "
                                "datatypes.Flow or a list of "
                                "datatypes.Flow")
        try:
            rest.post(url, self.auth, json.dumps(data))
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))

    def update_flows(self, dpid, flows):
        """Update a flow, or flows at the selected DPID"""
        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               'flows')
        if isinstance(flows, list):
            tmp = []
            for f in flows:
                if isinstance(f, datatypes.Flow):
                    tmp.append(f.to_dict())
                else:
                    raise FlareApiError("Invalid argument. Expected "
                                        "datatypes.Flow or a list of "
                                        "datatypes.Flow")
            data = { "flows" : tmp }
        elif isinstance(flows, datatypes.Flow):
            data = { "flow" : flows.to_dict() }
        else:
            raise FlareApiError("Invalid argument. Expected "
                                "datatypes.Flow or a list of "
                                "datatypes.Flow")
        try:
            rest.put(url, self.auth, json.dumps(data))
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))

    def delete_flows(self, dpid, flows):
        """ Delete flow, or flows from the specified DPID"""

        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               'flows')
        if isinstance(flows, list):
            tmp = []
            for f in flows:
                if isinstance(f, datatypes.Flow):
                    tmp.append(f.to_dict())
                else:
                    raise FlareApiError("Invalid argument. Expected "
                                        "datatypes.Flow or a list of "
                                        "datatypes.Flow")
            data = { "flows" : tmp }
        elif isinstance(flows, datatypes.Flow):
            data = { "flow" : flows.to_dict() }
        else:
            raise FlareApiError("Invalid argument. Expected "
                                "datatypes.Flow or a list of "
                                "datatypes.Flow")
        try:
            rest.delete(url, self.auth, data)
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))

    def get_groups(self, dpid):
        """Get a list of groups created on the DPID"""
        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               'groups')
        try:
            r = rest.get(url, self.auth)
            data = r.json()
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))
        return datatypes.JsonObject.factory(data)

    def add_groups(self, dpid, groups):
        """Create a group, or groups"""
        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               'groups')
        try:
            rest.post(url, self.auth, json.dumps(groups.to_dict()))
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))

    def get_group_details(self, dpid, group_id):
        """Get group details"""
        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               'groups/{0}'.format(group_id))
        try:
            r = rest.get(url, self.auth)
            data = r.json()
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))

        return datatypes.JsonObject.factory(data)

    def update_groups(self, dpid, group_id, groups):
        """Update a group"""
        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               'groups/{0}'.format(group_id))
        try:
            rest.post(url, self.auth, json.dumps(groups.to_dict()))
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))

    def delete_groups(self, dpid, group_id):
        """Delete a group or groups"""
        url = (self._of_base_url +
               'datapaths/{0}/'.format(urllib.quote(dpid)) +
               'groups/{0}'.format(group_id))
        try:
            rest.delete(url, self.auth)
        except Exception as e:
            raise FlareApiError("Something went wrong with your request. "
                                "{0}".format(e))

