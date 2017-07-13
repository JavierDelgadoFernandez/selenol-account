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

"""Test AccountGroupAcceptPendingRequest Selenol service."""

from selenol_python.exceptions import SelenolInvalidArgumentException

from selenol_account.exceptions import SelenolUnauthorizedException
from selenol_account.services import AccountGroupAcceptPendingRequest


def test_account_group_accept_pending_requests_success(
        message, mock_connection, db, default_user, default_group,
        user_factory, add_group_request):
    """Test that a membership acceptation is working."""
    account_group_accept_pending_request = AccountGroupAcceptPendingRequest(
        mock_connection, db)

    user2 = user_factory('User2')

    membership_request = add_group_request(message, mock_connection, db,
                                           default_group, user2)
    assert membership_request.replied_at is None
    assert default_group.users.count() == 0

    result = account_group_accept_pending_request.on_request(message(
        {
            'user_id': default_user.id,
        },
        {
            'membership_request_id': membership_request.id,
        }))
    assert result['group_id'] == default_group.id
    assert len(result['members']) == 1
    assert user2.id in result['members']
    assert default_group.users.count() == 1
    assert membership_request.replied_at is not None


def test_account_group_accept_pending_requests_not_group_owner(
        message, mock_connection, db, default_user, default_group,
        user_factory, add_group_request):
    """Test that user has to be the owner of the group to accept a request."""
    account_group_accept_pending_request = AccountGroupAcceptPendingRequest(
        mock_connection, db)

    user2 = user_factory('User2')
    user3 = user_factory('User3')

    membership_request = add_group_request(message, mock_connection, db,
                                           default_group, user2)

    try:
        account_group_accept_pending_request.on_request(message(
            {
                'user_id': user3.id,
            },
            {
                'membership_request_id': membership_request.id,
            }))
        assert False
    except SelenolUnauthorizedException:
        assert default_group.users.count() == 0
        assert membership_request.replied_at is None


def test_account_group_accept_pending_requests_already_added(
        message, mock_connection, db, default_user, default_group,
        user_factory, add_group_request):
    """Test that a memebership request can not be accepted twice."""
    account_group_accept_pending_request = AccountGroupAcceptPendingRequest(
        mock_connection, db)

    user2 = user_factory('User2')
    membership_request = add_group_request(message, mock_connection, db,
                                           default_group, user2)

    account_group_accept_pending_request.on_request(message(
        {
            'user_id': default_user.id,
        },
        {
            'membership_request_id': membership_request.id,
        }))
    try:
        account_group_accept_pending_request.on_request(message(
            {
                'user_id': default_user.id,
            },
            {
                'membership_request_id': membership_request.id
            }))
        assert False, 'It can not accept the same request twice.'
    except SelenolInvalidArgumentException as ex:
        assert ex.argument == 'membership_request_id'
        assert default_group.users.count() == 1
