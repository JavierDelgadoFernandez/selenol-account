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

"""Test AccountUserInfo Selenol service."""

from selenol_account.services import AccountUserInfo


def test_account_user_info_success(message, mock_connection, db, default_user):
    """Test that the user information is generated correctly."""
    account_user_info = AccountUserInfo(mock_connection, db)
    result = account_user_info.on_request(message(
        {
        },
        {
            'user_id': default_user.id
        }))
    assert result['user_id'] == default_user.id
    assert result['name'] == default_user.name
    assert result['email'] == default_user.email
