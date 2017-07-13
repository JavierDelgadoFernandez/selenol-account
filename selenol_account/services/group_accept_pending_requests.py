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

"""Selenol service that accepts a group pending request."""

from datetime import datetime

from selenol_python.exceptions import SelenolInvalidArgumentException
from selenol_python.params import get_object_from_content, selenol_params
from selenol_python.services import SelenolService

from selenol_account.exceptions import SelenolUnauthorizedException
from selenol_account.models import AccountMembershipRequest
from selenol_account.params import get_user_from_session
from selenol_account.serializers import group_serializer


class AccountGroupAcceptPendingRequest(SelenolService):
    """Accepts a group pending request."""

    def __init__(self, connection=None, session=None):
        """Constructor.

        :param connection: Backend string connection.
        :param session: Database session creator.
        """
        super(AccountGroupAcceptPendingRequest, self).__init__(
            ['account', 'group', 'accept_pending_request'],
            connection, session)

    @selenol_params(
        user=get_user_from_session(),
        membership_request=get_object_from_content(
            AccountMembershipRequest, ['membership_request_id'])
    )
    def on_request(self, user, membership_request):
        """Request method.

        :param message: Original message.
        :param user: User that is executing the request.
        :param user_content: User to be accepted to the group.
        :param group: Group where the user was requesting membership.
        """
        if membership_request.group.creator_id != user.id:
            raise SelenolUnauthorizedException()

        if membership_request.replied_at:
            raise SelenolInvalidArgumentException(
                "membership_request_id", membership_request.id)

        membership_request.replied_at = datetime.now()
        self.session.commit()

        return group_serializer(membership_request.group)
