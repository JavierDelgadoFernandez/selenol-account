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

"""Setup module."""

from setuptools import setup

setup(
    name='selenol-account',
    version='0.1',
    description='Selenol module to user related actions.',
    url='https://github.com/selenol/selenol-account',
    author='Javier Delgado',
    author_email='JavierDelgado@outlook.com',
    license='GPLv3',
    test_suite='tests',
    entry_points={
        'selenol.services': [
            'group_accept_pending_requests='
            'selenol_account.services:AccountGroupAcceptPendingRequest',
            'group_all=selenol_account.services:AccountGroupAll',
            'group_create=selenol_account.services:AccountGroupCreate',
            'group_pending_requests='
            'selenol_account.services:AccountGroupPendingRequests',
            'account_group_info=selenol_account.services:AccountGroupInfo',
            'group_request=selenol_account.services:AccountGroupRequest',
            'group_waiting_requests='
            'selenol_account.services:AccountGroupWaitingRequests',
            'groups_user=selenol_account.services:AccountGroupUser',
            'oauth_login=selenol_account.services:AccountOAuthLogin',
            'token_login=selenol_account.services:AccountTokenLogin',
            'notifications_active='
            'selenol_account.services:AccountNotificationsActive',
            'notification_saw='
            'selenol_account.services:AccountNotificationSaw',
            'oauth_list=selenol_account.services:AccountOAuthListOptions',
            'user_all=selenol_account.services:AccountUserAll',
            'user_info=selenol_account.services:AccountUserInfo',
        ],
        'selenol.fixtures': [
            'admin_user_public_group='
            'selenol_account.fixtures:create_admin_user_public_group',
        ]
    },
    install_requires=[
        'requests>=2.13.0',
        'selenol-platform>=0.1',
        'selenol-python>=0.1',
        'sqlalchemy>=1.1.9',
    ],
    packages=['selenol_account'],
    extras_require={
        'tests': [
            'coverage>=4.0',
            'isort>=4.2.5',
            'mock>=2.0.0',
            'pytest>=3.0.7',
            'pydocstyle>=1.1.1',
            'pytest-cache>=1.0',
            'pytest-cov>=2.4.0',
            'pytest-pep8>=1.0.6',
            'pytest-runner>=2.11.1',
        ],
    },
)
