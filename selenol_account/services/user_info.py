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

"""Selenol service that returns information about a sepecific user."""

from selenol_python.params import get_object_from_content, selenol_params
from selenol_python.services import SelenolService

from selenol_account.models import AccountUser
from selenol_account.serializers import user_serializer


class AccountUserInfo(SelenolService):
    """Returns information about a sepecific user."""

    def __init__(self, connection=None, session=None):
        """Constructor.

        :param connection: Backend string connection.
        :param session: Database session creator.
        """
        super(AccountUserInfo, self).__init__(
            ['account', 'user', 'info'], connection, session)

    @selenol_params(
        user=get_object_from_content(AccountUser, ['user_id'])
    )
    def on_request(self, user):
        """Request method.

        :param user: User that is executing the request.
        """
        return user_serializer(user)
