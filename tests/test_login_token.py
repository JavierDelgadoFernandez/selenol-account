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

"""Test AccountLoginToken Selenol service."""

from selenol_python.exceptions import SelenolInvalidArgumentException

from selenol_account.models import AccountSession
from selenol_account.services import AccountTokenLogin


def test_account_token_login_success(
        message, mock_connection, db, default_user):
    """Test that a user can login using a token."""
    account_token_login = AccountTokenLogin(mock_connection, db)

    token_test = 'TokenTest'

    account_session = AccountSession(user_id=default_user.id, token=token_test)
    db.add(account_session)
    db.commit()

    result = account_token_login.on_request(message(
        {
        },
        {
            'token': token_test
        }))
    assert any([item['reason'] == ['request', 'metadata'] and
                item['content'] == {'user_id': 1}
                for item in mock_connection.received])
    assert default_user.id == result['user_id']
    assert default_user.name == result['name']
    assert default_user.email == result['email']


def test_account_token_login_wrong_token(
        message, mock_connection, db, default_user):
    """Test that a wrong token creates a SelenolInvalidArgumentException."""
    account_token_login = AccountTokenLogin(mock_connection, db)

    try:
        account_token_login.on_request(message(
            {
            },
            {
                'token': 'NoToken'
            }))
        assert False
    except SelenolInvalidArgumentException as ex:
        assert ex.argument == 'token'
        assert not any([item['reason'] == ['request', 'metadata'] and
                        item['content'] == {'user_id': 1}
                        for item in mock_connection.received])
