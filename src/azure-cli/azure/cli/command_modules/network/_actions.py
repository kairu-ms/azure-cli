# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from collections import defaultdict

import argparse
from knack.util import CLIError
from azure.cli.core.azclierror import UnrecognizedArgumentError
from ._validators import read_base_64_file
from azure.cli.core.translator import cls_action_wrapper


# pylint: disable=protected-access
@cls_action_wrapper
class AddBackendAddressCreate(argparse._AppendAction):
    def __call__(self, parser, namespace, values, option_string=None):
        action = self.get_action(values, option_string)
        super(AddBackendAddressCreate, self).__call__(parser, namespace, action, option_string)

    def get_action(self, values, option_string):  # pylint: disable=no-self-use
        try:
            properties = defaultdict(list)
            for (k, v) in (x.split('=', 1) for x in values):
                properties[k].append(v)
            properties = dict(properties)
        except ValueError:
            raise CLIError('usage error: {} [KEY=VALUE ...]'.format(option_string))
        d = {}
        for k in properties:
            kl = k.lower()
            v = properties[k]
            if kl == 'name':
                d['name'] = v[0]
            elif kl == 'ip-address':
                d['ip_address'] = v[0]
            else:
                raise CLIError('key error: key must be one of name and ip-address.')
        return d


@cls_action_wrapper
class AddBackendAddressCreateForCrossRegionLB(argparse._AppendAction):
    def __call__(self, parser, namespace, values, option_string=None):
        action = self.get_action(values, option_string)
        super(AddBackendAddressCreateForCrossRegionLB, self).__call__(parser, namespace, action, option_string)

    def get_action(self, values, option_string):  # pylint: disable=no-self-use
        try:
            properties = defaultdict(list)
            for (k, v) in (x.split('=', 1) for x in values):
                properties[k].append(v)
            properties = dict(properties)
        except ValueError:
            raise CLIError('usage error: {} [KEY=VALUE ...]'.format(option_string))
        d = {}
        for k in properties:
            kl = k.lower()
            v = properties[k]
            if kl == 'name':
                d['name'] = v[0]
            elif kl == 'frontend-ip-address':
                d['frontend_ip_address'] = v[0]
            else:
                raise CLIError('key error: key must be one of name and frontend-ip-address.')
        return d


@cls_action_wrapper
class TrustedClientCertificateCreate(argparse._AppendAction):
    def __call__(self, parser, namespace, values, option_string=None):
        action = self.get_action(values, option_string)
        super(TrustedClientCertificateCreate, self).__call__(parser, namespace, action, option_string)

    def get_action(self, values, option_string):  # pylint: disable=no-self-use
        try:
            properties = defaultdict(list)
            for (k, v) in (x.split('=', 1) for x in values):
                properties[k].append(v)
            properties = dict(properties)
        except ValueError:
            raise UnrecognizedArgumentError('usage error: {} [KEY=VALUE ...]'.format(option_string))
        d = {}
        for k in properties:
            kl = k.lower()
            v = properties[k]
            if kl == 'name':
                d['name'] = v[0]
            elif kl == 'data':
                d['data'] = read_base_64_file(v[0])
            else:
                raise UnrecognizedArgumentError('key error: key must be one of name and data.')
        return d


def _split(param):
    return param.split(',')


@cls_action_wrapper
class SslProfilesCreate(argparse._AppendAction):
    def __call__(self, parser, namespace, values, option_string=None):
        action = self.get_action(values, option_string)
        super(SslProfilesCreate, self).__call__(parser, namespace, action, option_string)

    def get_action(self, values, option_string):  # pylint: disable=no-self-use
        try:
            properties = defaultdict(list)
            for (k, v) in (x.split('=', 1) for x in values):
                properties[k].append(v)
            properties = dict(properties)
        except ValueError:
            raise UnrecognizedArgumentError('usage error: {} [KEY=VALUE ...]'.format(option_string))
        d = {}
        for k in properties:
            kl = k.lower()
            v = properties[k]
            if kl == 'name':
                d['name'] = v[0]
            elif kl == 'policy-type':
                d['policy_type'] = v[0]
            elif kl == 'min-protocol-version':
                d['min_protocol_version'] = v[0]
            elif kl == 'cipher-suites':
                d['cipher_suites'] = _split(v[0])
            elif kl == 'disabled-ssl-protocols':
                d['disabled_ssl_protocols'] = _split(v[0])
            elif kl == 'client-auth-configuration':
                d['client_auth_configuration'] = bool(v[0])
            elif kl == 'trusted-client-certificates':
                d['trusted_client_certificates'] = _split(v[0])
            else:
                raise UnrecognizedArgumentError('key error: key must be one of policy-type, min-protocol-version, '
                                                'cipher-suites, client-auth-configuration, trusted-client-certificates,'
                                                'disabled-ssl-protocols.')
        return d


# pylint: disable=too-few-public-methods
@cls_action_wrapper
class WafConfigExclusionAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        cmd = namespace._cmd  # pylint: disable=protected-access
        ApplicationGatewayFirewallExclusion = cmd.get_models('ApplicationGatewayFirewallExclusion')
        if not namespace.exclusions:
            namespace.exclusions = []
        if isinstance(values, list):
            values = ' '.join(values)
        try:
            variable, op, selector = values.split(' ')
        except (ValueError, TypeError):
            raise CLIError('usage error: --exclusion VARIABLE OPERATOR VALUE')
        namespace.exclusions.append(ApplicationGatewayFirewallExclusion(
            match_variable=variable,
            selector_match_operator=op,
            selector=selector
        ))


# pylint: disable=protected-access,too-few-public-methods
@cls_action_wrapper
class NWConnectionMonitorEndpointFilterItemAction(argparse._AppendAction):
    def __call__(self, parser, namespace, values, option_string=None):
        ConnectionMonitorEndpointFilterItem = namespace._cmd.get_models('ConnectionMonitorEndpointFilterItem')

        if not namespace.filter_items:
            namespace.filter_items = []

        filter_item = ConnectionMonitorEndpointFilterItem()

        for item in values:
            try:
                key, val = item.split('=', 1)

                if hasattr(filter_item, key):
                    setattr(filter_item, key, val)
                else:
                    raise CLIError(
                        "usage error: '{}' is not a valid property of ConnectionMonitorEndpointFilterItem".format(key))
            except ValueError:
                raise CLIError(
                    'usage error: {} PropertyName=PropertyValue [PropertyName=PropertyValue ...]'.format(option_string))

        namespace.filter_items.append(filter_item)


# pylint: disable=protected-access,too-few-public-methods
@cls_action_wrapper
class NWConnectionMonitorTestConfigurationHTTPRequestHeaderAction(argparse._AppendAction):
    def __call__(self, parser, namespace, values, option_string=None):
        HTTPHeader = namespace._cmd.get_models('HTTPHeader')

        if not namespace.http_request_headers:
            namespace.http_request_headers = []

        request_header = HTTPHeader()

        for item in values:
            try:
                key, val = item.split('=', 1)
                if hasattr(request_header, key):
                    setattr(request_header, key, val)
                else:
                    raise CLIError("usage error: '{}' is not a value property of HTTPHeader".format(key))
            except ValueError:
                raise CLIError(
                    'usage error: {} name=HTTPHeader value=HTTPHeaderValue'.format(option_string))

        namespace.http_request_headers.append(request_header)
