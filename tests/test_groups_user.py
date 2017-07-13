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

"""Test AccountGroupUser Selenol service."""

from selenol_account.exceptions import SelenolUnauthorizedException
from selenol_account.services import AccountGroupUser


def test_account_group_user_success(
        message, mock_connection, db, default_user, group_factory):
    """Test that the groups of a user are listed correctly."""
    account_group_user = AccountGroupUser(mock_connection, db)

    group = group_factory('Group1', default_user)

    result = account_group_user.on_request(message(
        {
            'user_id': default_user.id
        },
        {
            'user_id': default_user.id
        }))
    assert 'owner' in result
    assert len(result['owner']) == 1
    assert result['owner'][0]['group_id'] == group.id
    assert result['owner'][0]['name'] == group.name
    assert 'member' in result
    assert len(result['member']) == 0


def test_account_group_user_wrong_user(
        message, mock_connection, db, default_user, user_factory,
        group_factory):
    """Test that only the user can list his list of groups."""
    account_group_user = AccountGroupUser(mock_connection, db)

    group_factory('Group1', default_user)

    user2 = user_factory('User2')

    try:
        account_group_user.on_request(message(
            {
                'user_id': user2.id
            },
            {
                'user_id': default_user.id
            }))
        assert False, "A user can not list the groups of another user."
    except SelenolUnauthorizedException:
        pass
