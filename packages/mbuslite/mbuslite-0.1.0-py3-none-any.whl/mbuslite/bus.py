
import logging

logger = logging.getLogger( __name__ )


from collections import defaultdict
from typing import Callable



class Subscription:
    """
    Opaque object allowing the subscriber to unsubscribe.
    """

    def __init__( self, bus, topic, handler ):
        self.bus = bus
        self.topic = topic
        self.handler = handler


    def unsubscribe( self ):
        """
        Remove the subscription created when ``Bus.subscribe`` was called.
        """
        self.bus.subscriptions[self.topic].remove( self )



class MessageBus:
    """
    The message bus. Should be used by importing ``mbuslite.Bus``.
    """

    def __init__( self ):
        self.subscriptions = defaultdict( list )


    def publish( self, topic: str, *args, **kwargs ) -> None:
        """
        Publish a message to the subscribers of the specified ``topic``. All remaining arguments and
        keyword arguments are passed as-is to the subscribed handlers.

        Note that all handlers are called synchronously, in the order they subscribed, before this
        method returns.

        Args:
            topic: the topic name
        """
        if logger.isEnabledFor( logging.DEBUG ):
            logger.debug( f'publishing {topic!r}: {args!r} {kwargs!r}' )
        else:
            logger.info( f'publishing {topic!r}' )

        for subscription in self.subscriptions[topic]:
            try:
                subscription.handler( *args, **kwargs )
            except:
                logger.warning( f'unhandled exception during publish on topic {topic!r}', exc_info = True )


    def subscribe( self, topic: str, handler: Callable ) -> Subscription:
        """
        Subscribe to the specified ``topic``

        Args:
            topic: the topic name
            handler: the handler to be called when a message is published to the topic.

        Returns:
            opaque object allowing unsubscribing
        """
        subscription = Subscription( self, topic, handler )
        self.subscriptions[topic].append( subscription )
        logger.debug( f'subscribing {topic!r}: {handler!r}' )
        return subscription

