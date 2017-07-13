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

"""Test AccountNotificationsActive Selenol service."""

import json

from pytest import raises
from selenol_python.exceptions import SelenolUnauthorizedException

from selenol_account.services import AccountNotificationSaw


def test_account_notification_saw_success(
        message, mock_connection, db, default_user, notification_factory):
    """Test a notification is marked successfully as saw."""
    account_notification_saw = AccountNotificationSaw(mock_connection, db)

    notification = notification_factory(default_user, "This is a test")

    result = account_notification_saw.on_request(message(
        {
            'user_id': default_user.id
        },
        {
            'notification_id': notification.id
        }))
    assert result['content'] == json.loads(notification.content)
    assert notification.saw_at is not None


def test_account_notification_saw_wrong_user(
        message, mock_connection, db, default_user, notification_factory,
        user_factory):
    """Test that a notification can not be mark as saw by other user."""
    account_notification_saw = AccountNotificationSaw(mock_connection, db)

    notification = notification_factory(default_user, "This is a test")

    user2 = user_factory("User2")

    with raises(SelenolUnauthorizedException):
        account_notification_saw.on_request(message(
            {
                'user_id': user2.id
            },
            {
                'notification_id': notification.id
            }))
