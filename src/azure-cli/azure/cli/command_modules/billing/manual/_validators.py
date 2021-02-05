# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=too-many-lines
# pylint: disable=too-many-statements
from azure.cli.core.translator import func_validator_wrapper


@func_validator_wrapper
def billing_invoice_download_validator(namespace):
    from azure.cli.core.azclierror import (
        RequiredArgumentMissingError,
        MutuallyExclusiveArgumentError,
    )

    valid_combs = (
        "only --account-name, --invoice-name, --download-token / "
        "--account-name, --download-urls / "
        "--download-urls /"
        "--invoice-name, --download-token is valid"
    )

    if namespace.account_name:
        if namespace.download_token is None and namespace.invoice_name is None and namespace.download_urls is None:
            raise RequiredArgumentMissingError(
                "--download-urls / --download-token, --invoice-name is also required"
            )

        if namespace.download_urls is not None:
            if namespace.download_token is not None or namespace.invoice_name is not None:
                raise MutuallyExclusiveArgumentError(valid_combs)
        if namespace.download_urls is None:
            if namespace.download_token is None and namespace.invoice_name is None:
                raise RequiredArgumentMissingError(
                    "--download-token and --invoice-name are also required"
                )
            if namespace.download_token is None:
                raise RequiredArgumentMissingError("--download-token is also required")
            if namespace.invoice_name is None:
                raise RequiredArgumentMissingError("--invoice-name is also required")

    if namespace.invoice_name is not None:
        if namespace.download_urls is not None:
            raise MutuallyExclusiveArgumentError(valid_combs)
        if namespace.download_token is None:
            raise RequiredArgumentMissingError(
                "--account-name, --download-token / --download-token is also required"
            )

    if namespace.download_token is not None:
        if namespace.download_urls is not None:
            raise MutuallyExclusiveArgumentError(valid_combs)
        if namespace.account_name is not None:
            raise RequiredArgumentMissingError("--invoice-name is also required")
        if namespace.invoice_name is None:
            raise RequiredArgumentMissingError(
                "--account-name, --invoice-name / --invoice-name is also required"
            )

    if namespace.download_urls is not None:
        if namespace.download_token is not None:
            raise MutuallyExclusiveArgumentError(
                "--download-urls can't be used with --download-token"
            )
        if namespace.invoice_name is not None:
            raise MutuallyExclusiveArgumentError(
                "--download-urls can't be used with --invoice-name"
            )


@func_validator_wrapper
def billing_invoice_show_validator(namespace):
    from azure.cli.core.azclierror import (
        RequiredArgumentMissingError,
        MutuallyExclusiveArgumentError,
    )

    valid_combs = (
        "only --account-name, --name / --name / --name, --by-subscription is valid"
    )

    if namespace.account_name is not None:
        if namespace.by_subscription is not None:
            raise MutuallyExclusiveArgumentError(valid_combs)
        if namespace.name is None:
            raise RequiredArgumentMissingError("--name is also required")

    if namespace.by_subscription is not None:
        if namespace.name is None:
            raise RequiredArgumentMissingError("--name is also required")


@func_validator_wrapper
def billing_permission_list_validator(namespace):
    from azure.cli.core.azclierror import MutuallyExclusiveArgumentError

    if namespace.customer_name is not None:
        if namespace.invoice_section_name is not None:
            raise MutuallyExclusiveArgumentError(
                "--customer-name can't be used with --invoice-section-name"
            )

        if namespace.profile_name is not None:
            raise MutuallyExclusiveArgumentError(
                "--customer-name can't be used with --profile-name"
            )
