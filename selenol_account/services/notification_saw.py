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

"""Selenol service that marks a notification as saw."""

from datetime import datetime

from selenol_python.exceptions import SelenolUnauthorizedException
from selenol_python.params import get_object_from_content, selenol_params
from selenol_python.services import SelenolService

from selenol_account.models import AccountNotification
from selenol_account.params import get_user_from_session
from selenol_account.serializers import notification_serializer


class AccountNotificationSaw(SelenolService):
    """Mark a notification as saw."""

    def __init__(self, connection=None, session=None):
        """Constructor.

        :param connection: Backend string connection.
        :param session: Database session creator.
        """
        super(AccountNotificationSaw, self).__init__(
            ['account', 'notification', 'saw'], connection, session)

    @selenol_params(
        user=get_user_from_session(),
        notification=get_object_from_content(
            AccountNotification, ['notification_id']),
    )
    def on_request(self, user, notification):
        """Request method.

        :param user: User that is executing the request.
        :param notification: Notification to be mark as saw.
        """
        if notification.user_id != user.id:
            raise SelenolUnauthorizedException()

        notification.saw_at = datetime.now()
        self.session.commit()

        return notification_serializer(notification)
