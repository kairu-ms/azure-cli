# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from azure.cli.core.translator import func_client_factory_wrapper


@func_client_factory_wrapper
def cf_billing(cli_ctx, **_):
    from azure.cli.core.commands.client_factory import get_mgmt_service_client
    from azure.mgmt.billing import BillingManagementClient
    return get_mgmt_service_client(cli_ctx, BillingManagementClient)


@func_client_factory_wrapper
def invoices_mgmt_client_factory(cli_ctx, kwargs):
    return cf_billing(cli_ctx, **kwargs).invoices


@func_client_factory_wrapper
def billing_periods_mgmt_client_factory(cli_ctx, kwargs):
    return cf_billing(cli_ctx, **kwargs).billing_periods


@func_client_factory_wrapper
def enrollment_accounts_mgmt_client_factory(cli_ctx, kwargs):
    return cf_billing(cli_ctx, **kwargs).enrollment_accounts
