# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.commands import AzArgumentContext


class AzTranslatorArgumentContext(AzArgumentContext):

    def __init__(self, command_loader, scope, **kwargs):
        super(AzTranslatorArgumentContext, self).__init__(command_loader=command_loader, scope=scope, **kwargs)
