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
from datetime import datetime

from selenol_account.models import AccountNotification
from selenol_account.services import AccountNotificationsActive


def test_account_notifications_active_success(
        message, mock_connection, db, default_user):
    """Test that the user notifications are listed correctly."""
    account_notifications_active = AccountNotificationsActive(
        mock_connection, db)

    result = account_notifications_active.on_request(message(
        {
            'user_id': default_user.id
        },
        {
        }))
    assert len(result) == 0

    notification_0 = AccountNotification(user_id=default_user.id,
                                         content=json.dumps({'key': 'value'}),
                                         created_at=datetime.now())
    db.add(notification_0)
    db.commit()

    notification_1 = AccountNotification(user_id=default_user.id,
                                         content=json.dumps({'key': 'value'}),
                                         created_at=datetime.now(),
                                         saw_at=datetime.now())
    db.add(notification_1)
    db.commit()

    result = account_notifications_active.on_request(message(
        {
            'user_id': default_user.id
        },
        {
        }))
    assert len(result) == 1
    assert result[0]['content'] == json.loads(
        notification_0.content)
    assert result[0]['created_at'] == str(
        notification_0.created_at)
