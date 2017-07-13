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

"""Test AccountOAuthListOptions Selenol service."""

from mock import patch

from selenol_account.services import AccountOAuthListOptions


def test_account_oath_list_success(message, mock_connection, db, default_user):
    """Test that the OAuth options list is generated correctly."""
    account_oauth_list_options = AccountOAuthListOptions(mock_connection, db)

    sample = 'sample'

    oauths = {
        sample: {
            'name': 'ExampleName',
            'request_url': 'ExampleURL',
        },
    }

    with patch('selenol_account.config.OAUTH_SETTINGS', oauths):
        result = account_oauth_list_options.on_request(message(
            {
            },
            {
            }))
        assert len(result) == 1
        assert result[0]['name'] == oauths[sample]['name']
        assert result[0]['request_url'] == oauths[sample]['request_url']
