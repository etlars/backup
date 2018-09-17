#!/usr/bin/env python

"""
NSX-T SDK Sample Code

Copyright 2017 VMware, Inc.  All rights reserved

The BSD-2 license (the "License") set forth below applies to all
parts of the NSX-T SDK Sample Code project.  You may not use this
file except in compliance with the License.

BSD-2 License

Redistribution and use in source and binary forms, with or
without modification, are permitted provided that the following
conditions are met:

    Redistributions of source code must retain the above
    copyright notice, this list of conditions and the
    following disclaimer.

    Redistributions in binary form must reproduce the above
    copyright notice, this list of conditions and the
    following disclaimer in the documentation and/or other
    materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

import requests

from vmware.vapi.lib import connect
from vmware.vapi.security.user_password import \
    create_user_password_security_context
from vmware.vapi.stdlib.client.factories import StubConfigurationFactory


def get_basic_auth_stub_config(user, password, nsx_host, tcp_port=443):
    """
    Create a stub configuration that uses HTTP basic authentication.
    """
    session = requests.session()

    # Since the NSX manager default certificate is self-signed,
    # we disable verification. This is dangerous and real code
    # should verify that it is talking to a valid server.
    session.verify = False
    requests.packages.urllib3.disable_warnings()

    nsx_url = 'https://%s:%s' % (nsx_host, tcp_port)
    connector = connect.get_requests_connector(
        session=session, msg_protocol='rest', url=nsx_url)
    stub_config = StubConfigurationFactory.new_std_configuration(connector)
    security_context = create_user_password_security_context(
        user, password)
    connector.set_security_context(security_context)
    return stub_config


def get_session_auth_stub_config(user, password, nsx_host, tcp_port=443):
    """
    Create a stub configuration that uses session-based authentication.
    Session authentication is more efficient, since the server only
    needs to perform authentication of the username/password one time.
    """
    session = requests.session()

    # Since the NSX manager default certificate is self-signed,
    # we disable verification. This is dangerous and real code
    # should verify that it is talking to a valid server.
    session.verify = False
    requests.packages.urllib3.disable_warnings()
    nsx_url = 'https://%s:%s' % (nsx_host, tcp_port)
    resp = session.post(nsx_url + "/api/session/create",
                        data={"j_username": user, "j_password": password})
    if resp.status_code != requests.codes.ok:
        resp.raise_for_status()

    # Set the Cookie and X-XSRF-TOKEN headers
    session.headers["Cookie"] = resp.headers.get("Set-Cookie")
    session.headers["X-XSRF-TOKEN"] = resp.headers.get("X-XSRF-TOKEN")

    connector = connect.get_requests_connector(
        session=session, msg_protocol='rest', url=nsx_url)
    stub_config = StubConfigurationFactory.new_std_configuration(connector)
    return stub_config
