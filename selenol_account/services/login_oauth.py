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

"""Selenol service that logs in a user using OAuth."""

import json
import uuid
from datetime import datetime

import requests
from selenol_python.params import (get_request_id, get_value_from_content,
                                   selenol_params)
from selenol_python.services import SelenolService

from selenol_account import config
from selenol_account.models import (AccountGroup, AccountMembershipRequest,
                                    AccountNotification, AccountOAuthIdentity,
                                    AccountSession, AccountUser)
from selenol_account.serializers import (login_serializer,
                                         notification_serializer)


def login_github(session, code):
    """Oauth log in using GitHub service."""
    client_id = config.OAUTH_SETTINGS['github']['client_id']
    client_secret = config.OAUTH_SETTINGS['github']['client_secret']

    resp = requests.post('https://github.com/login/oauth/access_token?'
                         'client_id={0}&client_secret={1}&code={2}'.format(
                             client_id, client_secret, code),
                         headers={'Accept': 'application/json'}).json()
    access_token = resp['access_token']

    user_info = requests.get('https://api.github.com/user',
                             headers={'Authorization': 'token {0}'.format(
                                 access_token)}).json()

    oauth_identity_query = session.query(AccountOAuthIdentity).filter(
        AccountOAuthIdentity.user_identifier == str(user_info['id'])).filter(
            AccountOAuthIdentity.service == 'github')

    new_user = oauth_identity_query.count() == 0

    if new_user:
        account_user = AccountUser(name=user_info['name'],
                                   email=user_info['email'])
        session.add(account_user)
        session.commit()

        public_group = session.query(AccountGroup).filter(
            AccountGroup.name == 'public').one()

        membership = AccountMembershipRequest(user_id=account_user.id,
                                              group_id=public_group.id,
                                              requested_at=datetime.now(),
                                              replied_at=datetime.now())
        session.add(membership)
        session.commit()
        session.commit()
    else:
        account_user = oauth_identity_query.first().user

    if session.query(AccountOAuthIdentity).filter(
            AccountOAuthIdentity.access_token == access_token).filter(
                AccountOAuthIdentity.service == 'github').count() == 0:
        account_oauth_identity = AccountOAuthIdentity(
            service='github', user_identifier=str(user_info['id']),
            access_token=access_token, user_id=account_user.id,
            created=datetime.now())
        session.add(account_oauth_identity)

    return account_user


class AccountOAuthLogin(SelenolService):
    """Logs in user using a OAuth."""

    def __init__(self, connection=None, session=None):
        """Constructor.

        :param connection: Backend string connection.
        :param session: Database session creator.
        """
        super(AccountOAuthLogin, self).__init__(
            ['account', 'login', 'oauth'], connection, session)

    @selenol_params(
        request_id=get_request_id(),
        code=get_value_from_content(['code']),
        service=get_value_from_content(['service'])
    )
    def on_request(self, request_id, code, service):
        """Request method.

        :param request_id: ID of the current request.
        :param token: User token that identifies the unique user.
        """
        if service == 'github':
            account_user = login_github(self.session, code)
        else:
            raise NotImplementedError()

        token = str(uuid.uuid4())
        account_session = AccountSession(user_id=account_user.id, token=token)
        self.session.add(account_session)

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
            'user_id': account_user.id
        })

        return login_serializer(account_session.user, token)
