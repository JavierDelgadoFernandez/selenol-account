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

"""Selenol service that return all the group pending requests for a user."""

from selenol_python.params import get_object_from_content, selenol_params
from selenol_python.services import SelenolService

from selenol_account.exceptions import SelenolUnauthorizedException
from selenol_account.models import AccountMembershipRequest, AccountUser
from selenol_account.params import get_user_from_session
from selenol_account.serializers import group_membership_request_serializer


class AccountGroupPendingRequests(SelenolService):
    """Return all the group pending requests for a user."""

    def __init__(self, connection=None, session=None):
        """Constructor.

        :param connection: Backend string connection.
        :param session: Database session creator.
        """
        super(AccountGroupPendingRequests, self).__init__(
            ['account', 'group', 'pending_requests'], connection, session)

    @selenol_params(
        user=get_user_from_session(),
        user_content=get_object_from_content(AccountUser, ['user_id']),
    )
    def on_request(self, user, user_content):
        """Request method.

        :param user: User that is executing the request.
        :param user_content: User to be accepted to the group.
        """
        if user.id != user_content.id:
            raise SelenolUnauthorizedException()

        return [group_membership_request_serializer(unreplied_request)
                for unreplied_request in user.owned_groups.join(
                    AccountMembershipRequest).filter(
                        AccountMembershipRequest.replied_at.is_(None)
                        ).with_entities(AccountMembershipRequest)]
