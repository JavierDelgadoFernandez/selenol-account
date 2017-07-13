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

"""Test AccountGroupInfo Selenol service."""

from selenol_account.services import AccountGroupInfo


def test_account_group_info_success(message, mock_connection, db,
                                    default_group):
    """Test that the group information is generated correctly."""
    account_group_info = AccountGroupInfo(mock_connection, db)
    result = account_group_info.on_request(message(
        {
        },
        {
            'group_id': default_group.id
        }))
    assert result['group_id'] == default_group.id
    assert result['name'] == default_group.name
    assert len(result['members']) == 0
