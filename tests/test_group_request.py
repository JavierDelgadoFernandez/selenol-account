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

"""Test AccountGroupRequest Selenol service."""

from selenol_python.exceptions import SelenolInvalidArgumentException

from selenol_account.exceptions import SelenolUnauthorizedException
from selenol_account.models import AccountMembershipRequest
from selenol_account.services import AccountGroupRequest


def test_account_group_request_success(
        message, mock_connection, db, default_user, group_factory,
        user_factory):
    """Test that a membership request is created correctly."""
    account_group_request = AccountGroupRequest(mock_connection, db)

    user2 = user_factory("User2")

    group = group_factory('TestGroup', default_user)
    assert db.query(AccountMembershipRequest).count() == 0

    result = account_group_request.on_request(message(
        {
            'user_id': user2.id
        },
        {
            'user_id': user2.id,
            'group_id': group.id
        }))
    assert result['group']['group_id'] == group.id

    assert db.query(AccountMembershipRequest).count() == 1


def test_account_group_request_wrong_user(
        message, mock_connection, db, default_user, user_factory,
        group_factory):
    """Test that the membership request can not be created by other user."""
    account_group_request = AccountGroupRequest(mock_connection, db)

    group = group_factory('TestGroup', default_user)
    user2 = user_factory('User2')
    assert db.query(AccountMembershipRequest).count() == 0

    try:
        account_group_request.on_request(message(
            {
                'user_id': default_user.id
            },
            {
                'user_id': user2.id,
                'group_id': group.id
            }))
        assert False, "User in session and user in content has to be the same."
    except SelenolUnauthorizedException:
        assert db.query(AccountMembershipRequest).count() == 0


def test_account_group_request_group_creator(
        message, mock_connection, db, default_user, group_factory):
    """Test that the request can not be created by the group creator."""
    account_group_request = AccountGroupRequest(mock_connection, db)

    group = group_factory('TestGroup', default_user)
    assert db.query(AccountMembershipRequest).count() == 0

    try:
        account_group_request.on_request(message(
            {
                'user_id': default_user.id
            },
            {
                'user_id': default_user.id,
                'group_id': group.id
            }))
        assert False, "Group creator can not request membership."
    except SelenolInvalidArgumentException as ex:
        assert ex.argument == 'group_id'
        assert db.query(AccountMembershipRequest).count() == 0
