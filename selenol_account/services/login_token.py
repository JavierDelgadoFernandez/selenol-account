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

"""Selenol service that logs in user using a token."""

import json
from datetime import datetime

from selenol_python.exceptions import SelenolInvalidArgumentException
from selenol_python.params import (get_request_id, get_value_from_content,
                                   selenol_params)
from selenol_python.services import SelenolService

from selenol_account.models import AccountNotification, AccountSession
from selenol_account.serializers import (login_serializer,
                                         notification_serializer)


class AccountTokenLogin(SelenolService):
    """Logs in user using a token."""

    def __init__(self, connection=None, session=None):
        """Constructor.

        :param connection: Backend string connection.
        :param session: Database session creator.
        """
        super(AccountTokenLogin, self).__init__(
            ['account', 'login', 'token'], connection, session)

    @selenol_params(
        request_id=get_request_id(),
        token=get_value_from_content(['token'])
    )
    def on_request(self, request_id, token):
        """Request method.

        :param request_id: ID of the current request.
        :param token: User token that identifies the unique user.
        """
        account_session = self.session.query(AccountSession).filter(
            AccountSession.token == token).one_or_none()

        if not account_session:
            raise SelenolInvalidArgumentException('token', token)

        notification = AccountNotification(
            user_id=account_session.user_id, created_at=datetime.now(),
            content=json.dumps({
                'module': 'account',
                'title': 'New connection on {0}'.format(datetime.now()),
                'code': 200,
            })
        )
        self.session.add(notification)
        self.session.commit()
        self.notify(['account', 'notification', 'user', str(
            notification.user_id)], notification_serializer(notification))

        self.metadata(request_id, {
            'user_id': account_session.user_id
        })

        return login_serializer(account_session.user)
