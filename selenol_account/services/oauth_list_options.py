# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Selenol service that lists all the OAuth possible services."""

from selenol_python.params import selenol_params
from selenol_python.services import SelenolService

from selenol_account import config
from selenol_account.serializers import oauth_info_serializer


class AccountOAuthListOptions(SelenolService):
    """Returns all the OAuth possible services."""

    def __init__(self, connection=None, session=None):
        """Constructor.

        :param connection: Backend string connection.
        :param session: Database session creator.
        """
        super(AccountOAuthListOptions, self).__init__(
            ['account', 'oauth', 'list_options'], connection, session)

    @selenol_params()
    def on_request(self):
        """Request method."""
        return [oauth_info_serializer(values) for (service, values) in
                config.OAUTH_SETTINGS.items()]
