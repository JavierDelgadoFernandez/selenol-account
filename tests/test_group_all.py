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

"""Test AccountGroupAll Selenol service."""

from selenol_account.services import AccountGroupAll


def test_account_group_all_success(
        message, mock_connection, db, default_user, group_factory):
    """Test the result of list all the group requests."""
    account_group_all = AccountGroupAll(mock_connection, db)

    empty_message = message({}, {})

    result = account_group_all.on_request(empty_message)
    assert len(result) == 0

    group = group_factory('TestGroup', default_user)

    result = account_group_all.on_request(empty_message)
    assert len(result) == 1
    assert result[0]['group_id'] == group.id
    assert result[0]['name'] == group.name
