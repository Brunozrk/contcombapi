# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import logging
from contcombapi.exception.ManagerException import ManagerException
from contcombapi.manager.BaseQuerySet import BaseQuerySet

logger = logging.getLogger(__name__)


class BaseManager(models.Manager):
    '''
        Base class for managing the operations to database
    '''

    def get_by_pk(self, pk):
        '''Get Object by pk.

        @param pk: Identifier of the Model. Integer value and greater than zero.

        @return: Object.

        @raise ManagerException: Failed to search for the Object
        '''
        try:

            return self.get(pk=pk)

        except ObjectDoesNotExist, e:
            logger.error(e)
            raise ObjectDoesNotExist(e)

        except Exception, e:
            logger.error(e)
            raise ManagerException(e)

    def get_query_set(self):
        return BaseQuerySet(self.model, using=self._db)
