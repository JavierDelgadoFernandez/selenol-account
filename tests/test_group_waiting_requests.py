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

"""Test AccountGroupWaitingRequests Selenol service."""

from selenol_account.exceptions import SelenolUnauthorizedException
from selenol_account.services import AccountGroupWaitingRequests


def test_account_group_waiting_requests_success(
        message, mock_connection, db, default_user, default_group,
        add_group_request, user_factory):
    """Test that the group waiting request are properly listed correctly."""
    account_group_waiting_requests = AccountGroupWaitingRequests(
        mock_connection, db)

    user2 = user_factory("User2")

    result = account_group_waiting_requests.on_request(message(
        {
            'user_id': user2.id
        },
        {
            'user_id': user2.id
        }))
    assert len(result) == 0

    add_group_request(message, mock_connection, db, default_group,
                      user2)

    result = account_group_waiting_requests.on_request(message(
        {
            'user_id': user2.id
        },
        {
            'user_id': user2.id
        }))
    assert len(result) == 1
    assert result[0]['user']['user_id'] == user2.id
    assert result[0]['group']['group_id'] == default_group.id


def test_account_group_waiting_requests_wrong_user(
        message, mock_connection, db, default_user, user_factory):
    """Test that only the owner of the group can list the waiting requests."""
    account_group_waiting_requests = AccountGroupWaitingRequests(
        mock_connection, db)

    user2 = user_factory('User2')

    try:
        account_group_waiting_requests.on_request(message(
            {
                'user_id': default_user.id
            },
            {
                'user_id': user2.id
            }))
        assert False, "Only the group owner can list the waiting requests."
    except SelenolUnauthorizedException:
        pass
