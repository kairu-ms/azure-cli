# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core import AzCommandsLoader


class AzTranslatorCommandsLoader(AzCommandsLoader):

    def __init__(self, cli_ctx=None, command_group_cls=None, argument_context_cls=None,
                 suppress_extension=None, **kwargs):
        super(AzTranslatorCommandsLoader, self).__init__(
            cli_ctx=cli_ctx, command_group_cls=command_group_cls, argument_context_cls=argument_context_cls,
            suppress_extension=suppress_extension, **kwargs)
