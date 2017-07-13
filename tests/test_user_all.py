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

"""Test AccountUserAll Selenol service."""

from selenol_account.services import AccountUserAll


def test_account_user_all_success(message, mock_connection, db, default_user):
    """Test that all the system users are listed correctly."""
    account_user_all = AccountUserAll(mock_connection, db)
    result = account_user_all.on_request(message(
        {
        },
        {
        }))
    assert len(result) == 1
    assert result[0]['user_id'] == default_user.id
    assert result[0]['name'] == default_user.name
    assert result[0]['email'] == default_user.email
