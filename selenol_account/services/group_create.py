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

"""Selenol service that creates groups."""

from datetime import datetime

from selenol_python.exceptions import SelenolInvalidArgumentException
from selenol_python.params import (get_object_from_content,
                                   get_value_from_content, selenol_params)
from selenol_python.services import SelenolService

from selenol_account.exceptions import SelenolUnauthorizedException
from selenol_account.models import AccountGroup, AccountUser
from selenol_account.params import get_user_from_session
from selenol_account.serializers import group_serializer


class AccountGroupCreate(SelenolService):
    """Creates groups."""

    def __init__(self, connection=None, session=None):
        """Constructor.

        :param connection: Backend string connection.
        :param session: Database session creator.
        """
        super(AccountGroupCreate, self).__init__(
            ['account', 'group', 'create'], connection, session)

    @selenol_params(
        user=get_user_from_session(),
        user_content=get_object_from_content(AccountUser, ['user_id']),
        group_name=get_value_from_content(['name'])
    )
    def on_request(self, user, user_content, group_name):
        """Request method.

        :param user: User that is executing the request.
        :param user_content: User to be accepted to the group.
        :param group_name: Name of the new group.
        """
        if user.id != user_content.id:
            raise SelenolUnauthorizedException()

        if len(group_name) <= 0:
            raise SelenolInvalidArgumentException('name', group_name)

        if self.session.query(AccountGroup).filter(
                AccountGroup.name == group_name).one_or_none():
            raise SelenolInvalidArgumentException('name', group_name)

        group = AccountGroup(name=group_name, created=datetime.now(),
                             creator_id=user_content.id)
        self.session.add(group)
        self.session.commit()

        return group_serializer(group)
