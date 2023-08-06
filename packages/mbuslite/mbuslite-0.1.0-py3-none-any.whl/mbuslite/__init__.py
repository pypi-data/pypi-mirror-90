
__title__ = 'mbuslite'
__version__ = '0.1.0'
__description__ = 'A small, in-process message bus implementation.'
__author__ = 'Francis Ferrell'
__author_email__ = 'francisferrell@gmail.com'
__copyright__ = f'2020 {__author__}'
__url__ = 'https://gitlab.com/francisferrell/mbuslite'
__license__ = 'MIT'

import logging

logger = logging.getLogger( __name__ )
logger.addHandler( logging.NullHandler() )



from .bus import MessageBus
from .service import Service

Bus = MessageBus()
"""MessageBus: the default, application-wide bus"""

