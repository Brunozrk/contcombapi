# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

# -*- coding:utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
import logging
import hashlib
from contcombapi.exception.ManagerException import ManagerException
from contcombapi.manager.BaseManager import BaseManager


logger = logging.getLogger(__name__)


class UserManager(BaseManager):
    '''
        Base class for managing the operations to database
    '''

    def authenticate_user(self, username, password):
        '''Authenticate user root

        @param username: Username.
        @param password: Password.

        @return: User.

        @raise ManagerException: Failed to authenticate for the User
        '''
        try:
            password = hashlib.md5(password).hexdigest()
            user = self.get(username=username, password=password)

            return user

        except ObjectDoesNotExist, e:
            return None

        except Exception, e:
            logger.error(e)
            raise ManagerException(e)

    def get_by_username(self, username):
        '''Get User by username.

        @param username:

        @return: User.

        @raise ManagerException: Failed to search for the User
        '''
        try:

            return self.get(username=username)

        except ObjectDoesNotExist, e:
            logger.error(e)
            raise ObjectDoesNotExist(e)

        except Exception, e:
            logger.error(e)
            raise ManagerException(e)
