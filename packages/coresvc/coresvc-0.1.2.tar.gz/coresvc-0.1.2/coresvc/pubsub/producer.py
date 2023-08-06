from typing import Optional

from aio_pika import connect_robust, Connection, Channel, Message, Exchange, ExchangeType

from coresvc.base.base_service import BaseService
from coresvc.serializers import serializer


class Producer(BaseService):
    def __init__(self, url, **kwargs):
        self.url = url
        self._connection: Optional[Connection] = None
        self._channel: Optional[Channel] = None
        self._exchange: Optional[Exchange] = None
        super().__init__(**kwargs)

    async def on_start(self) -> None:
        await self._wait_for_connection()
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange('pubsub', type=ExchangeType.TOPIC)
        # TODO: Consider if exchange name should be
        #  - a single name for all or
        #  - multiple ones consistent with service namespace
        #  - this also depends on if we need more than one type of exchanges: fanout, direct, topic, etc

    async def on_started(self) -> None:
        self.log.info(self.label + 'started')

    async def on_stop(self) -> None:
        if self._connection:
            await self._connection.close()

    async def publish(self, topic: str, msg: dict):
        if not self.started:
            raise RuntimeError('service not started')
        message = Message(body=serializer.dumps(msg))
        await self._exchange.publish(message, routing_key=topic)

    async def _wait_for_connection(self, retry=0):
        try:
            self._connection = await connect_robust(self.url, loop=self.loop)
        except ConnectionError:
            if retry < 5:
                await self.sleep(3)
                return await self._wait_for_connection(retry+1)
            raise
