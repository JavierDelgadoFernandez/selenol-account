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

"""Test AccountLoginOAuth Selenol service."""

from mock import patch

from selenol_account.models import (AccountOAuthIdentity, AccountSession,
                                    AccountUser)
from selenol_account.services import AccountOAuthLogin
from selenol_account.services.login_oauth import login_github


def test_account_oauth_login_wrong_service(
        message, mock_connection, db, default_user):
    """Test that the service is crashing if the service is unknown."""
    account_login_oauth = AccountOAuthLogin(mock_connection, db)

    try:
        account_login_oauth.on_request(message(
            {
            },
            {
                'service': 'unknown',
                'code': 'bla',
            }))
        assert False, 'Service is not implemented'
    except NotImplementedError:
        pass


def test_account_oauth_login_success(
        message, mock_connection, db, default_user):
    """Test that the OAuth common implementation works correctly."""
    account_login_oauth = AccountOAuthLogin(mock_connection, db)

    def login_mock(db, code):
        """Simulates the OAuth authentification procedure.

        :param db: Database session.
        :param code: OAuth code returned by the service.
        """
        account_user = AccountUser(name='test', email='test@test.t')
        db.add(account_user)
        db.commit()
        return account_user

    with patch('selenol_account.services.login_oauth.login_github',
               login_mock):
        assert db.query(AccountSession).count() == 0
        result = account_login_oauth.on_request(message(
            {
            },
            {
                'service': 'github',
                'code': 'bla',
            }))
        assert db.query(AccountSession).count() == 1
        assert db.query(AccountSession).first().user_id == result['user_id']
        assert db.query(AccountSession).first().token == result['token']


def request_mock(content):
    """Mock up a requests request.

    :param content: Dictionary simulating the response of the request.
    """
    def request_function(*args, **kwargs):
        """Mock up the requests request function."""
        class request_response(object):
            """Mock up the requests request response."""
            def json(self):
                """Return the original content as dictionary."""
                return content
        return request_response()
    return request_function


@patch('requests.post', request_mock({
    'access_token': 'test_access_token'}))
@patch('requests.get', request_mock({
    'id': 43,
    'name': 'TestOAuth',
    'email': 'test_oatuh@test.test'}))
def test_login_github_new_user(db, public_group):
    """Test that GitHub OAuth login works with a new user."""
    assert db.query(AccountUser).count() == 1
    assert db.query(AccountOAuthIdentity).count() == 0
    assert public_group.users.count() == 0
    account_user = login_github(db, 'test_code')
    assert public_group.users.count() == 1
    assert db.query(AccountOAuthIdentity).count() == 1
    assert db.query(AccountUser).count() == 2


@patch('requests.post', request_mock({
    'access_token': 'test_access_token'}))
@patch('requests.get', request_mock({
    'id': 43,
    'name': 'TestOAuth',
    'email': 'test_oatuh@test.test'}))
def test_login_github_existing_user(db, public_group):
    """Test that GitHub OAuth login works with an existing user."""
    def login_user_oauth():
        account_user = login_github(db, 'test_code')
        assert db.query(AccountUser).count() == 2
        assert db.query(AccountOAuthIdentity).count() == 1
        assert public_group.users.count() == 1
    login_user_oauth()
    login_user_oauth()
