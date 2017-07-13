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

"""Test account fixtures."""

from selenol_account.fixtures import create_admin_user_public_group
from selenol_account.models import AccountGroup, AccountUser


def test_fixtures_creation(db):
    """Test the creation of the fixtures."""
    assert db.query(AccountUser).count() == 0
    assert db.query(AccountGroup).count() == 0

    create_admin_user_public_group(db)

    assert db.query(AccountUser).count() == 1
    assert db.query(AccountGroup).count() == 1
