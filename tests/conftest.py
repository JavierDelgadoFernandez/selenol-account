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

"""Test fixtures."""

import json
from datetime import datetime

import pytest
from selenol_python.data_structures import SelenolMessage
from selenol_python.exceptions import SelenolWebSocketClosedException
from selenol_python.persistences import Base, get_engine
from sqlalchemy.orm import sessionmaker

from selenol_account.models import (AccountGroup, AccountMembershipRequest,
                                    AccountNotification, AccountUser)
from selenol_account.services import AccountGroupRequest


@pytest.fixture
def message():
    """Create a message factory."""
    def factory(session, content):
        """Message factory.

        :param session: Message session.
        :param content: Message content.
        """
        return SelenolMessage({
            'content': {
                'session': session,
                'content': content,
            },
            'request_id': 0,
        })
    return factory


@pytest.fixture
def mock_connection():
    """Fixture for creating mock connections."""
    class MockConnection(object):
        """Mock backend connection for logging messages."""

        def __init__(self):
            """Default constructor."""
            self.received = []
            self.to_be_sent = []
            self.closed = False

        def send(self, message):
            """Saves the message inside received array."""
            if self.closed:
                raise SelenolWebSocketClosedException()
            self.received.append(message)

        def recv(self):
            """Return an empty array."""
            if self.closed:
                raise SelenolWebSocketClosedException()
            try:
                return self.to_be_sent.pop()
            except IndexError:
                raise SelenolWebSocketClosedException()

        def close(self):
            """Simulate the connection close."""
            self.closed = True

    return MockConnection()


@pytest.yield_fixture
def db(request):
    """Fixture that creates the database."""
    engine = get_engine('sqlite://')
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine)()


@pytest.fixture
def user_factory(db):
    """User creation fixture."""
    def factory(name):
        """Create a user with the given name.

        :param name: Name of the user.
        """
        result = AccountUser(name=name, email='{0}@test.test'.format(name))
        db.add(result)
        db.commit()
        return result
    return factory


@pytest.fixture
def default_user(db, user_factory):
    """Default user fixture."""
    return user_factory('test')


@pytest.fixture
def group_factory(db):
    """Group creation fixture."""
    def factory(name, user):
        """Create a group with the given name.

        :param name: Name of the new group.
        :param user: User creator of the group.
        """
        result = AccountGroup(name=name, creator_id=user.id)
        db.add(result)
        db.commit()
        return result
    return factory


@pytest.fixture
def notification_factory(db):
    """Notification creation fixture."""
    def factory(user, content):
        """Create a notification to the given user.

        :param user: User that will receive the notification.
        :param content: Content of the notification.
        """
        result = AccountNotification(
            user_id=user.id, content=json.dumps({'content': content}),
            created_at=datetime.now())
        db.add(result)
        db.commit()
        return result
    return factory


@pytest.fixture
def default_group(db, group_factory, default_user):
    """Default group fixture."""
    return group_factory('test', default_user)


@pytest.fixture
def public_group(db, group_factory, default_user):
    """Public group fixture."""
    return group_factory('public', default_user)


@pytest.fixture
def add_group_request():
    """Function factory to create group requests."""
    def factory(message, mock_connection, db, group, user):
        """Utility function to create a group request."""
        account_group_request = AccountGroupRequest(mock_connection, db)

        result = account_group_request.on_request(message(
            {
                'user_id': user.id
            },
            {
                'user_id': user.id,
                'group_id': group.id
            }))
        return db.query(AccountMembershipRequest).get(
            result['membership_request_id'])
    return factory
