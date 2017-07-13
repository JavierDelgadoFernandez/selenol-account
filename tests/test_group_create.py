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

"""Test AccountGroupCreate Selenol service."""

from selenol_python.exceptions import SelenolInvalidArgumentException

from selenol_account.exceptions import SelenolUnauthorizedException
from selenol_account.models import AccountGroup
from selenol_account.services import AccountGroupCreate


def test_account_group_create_success(
        message, mock_connection, db, default_user):
    """Test a group can be created."""
    account_group_create = AccountGroupCreate(mock_connection, db)

    assert db.query(AccountGroup).count() == 0

    group_name = 'TestGroupName'

    result = account_group_create.on_request(message(
        {
            'user_id': default_user.id
        },
        {
            'user_id': default_user.id,
            'name': group_name
        }))
    assert result['name'] == group_name

    assert db.query(AccountGroup).count() == 1


def test_account_group_create_wrong_user(
        message, mock_connection, db, default_user, user_factory):
    """Test that only the current user has to be the owner of the group."""
    account_group_create = AccountGroupCreate(mock_connection, db)

    assert db.query(AccountGroup).count() == 0

    user2 = user_factory('User2')

    try:
        account_group_create.on_request(message(
            {
                'user_id': user2.id
            },
            {
                'user_id': default_user.id,
                'name': 'TestGroupName'
            }))
        assert False, "The owner of the group should be the current user."""
    except SelenolUnauthorizedException:
        assert db.query(AccountGroup).count() == 0


def test_account_group_create_empty_name(
        message, mock_connection, db, default_user):
    """Test that it is not possible to create a group with an empty name."""
    account_group_create = AccountGroupCreate(mock_connection, db)

    assert db.query(AccountGroup).count() == 0

    try:
        account_group_create.on_request(message(
            {
                'user_id': default_user.id
            },
            {
                'user_id': default_user.id,
                'name': ''
            }))
        assert False, "Group name can not be empty."
    except SelenolInvalidArgumentException as ex:
        assert ex.argument == 'name'
        assert db.query(AccountGroup).count() == 0


def test_account_group_create_repeated_name(
        message, mock_connection, db, default_user, group_factory):
    """Test that the group name is unique."""
    account_group_create = AccountGroupCreate(mock_connection, db)

    group_name = 'GroupName'

    assert db.query(AccountGroup).count() == 0
    group_factory(group_name, default_user)
    assert db.query(AccountGroup).count() == 1

    try:
        account_group_create.on_request(message(
            {
                'user_id': default_user.id
            },
            {
                'user_id': default_user.id,
                'name': group_name
            }))
        assert False, "Group name can not be repeated."
    except SelenolInvalidArgumentException as ex:
        assert ex.argument == 'name'
        assert db.query(AccountGroup).count() == 1
