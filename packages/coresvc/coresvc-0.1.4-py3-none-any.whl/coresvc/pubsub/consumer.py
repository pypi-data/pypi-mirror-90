from typing import Optional, Callable, Any

from aio_pika import connect_robust, Connection, Channel, IncomingMessage, Exchange, ExchangeType

from coresvc.base.base_service import BaseService
from coresvc.serializers import serializer


class Consumer(BaseService):
    def __init__(self, url, **kwargs):
        self.url = url
        self._connection: Optional[Connection] = None
        self._channel: Optional[Channel] = None
        self._exchange: Optional[Exchange] = None
        self._msg_handlers = {}
        super().__init__(**kwargs)

    async def on_start(self) -> None:
        await self._wait_for_connection()
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange('pubsub', type=ExchangeType.TOPIC)

        # Maximum message count which will be
        # processing at the same time.
        # await self._channel.set_qos(prefetch_count=100)

    async def on_started(self) -> None:
        self.log.info(self.label + 'started')

    async def on_stop(self) -> None:
        if self._connection:
            await self._connection.close()

    async def subscribe(self, topic: str, handler: Callable[[dict], Any]):
        if not self.started:
            raise RuntimeError('service not started')

        async def handler_wrapper(message: IncomingMessage):
            obj = serializer.loads(message.body)
            try:
                await handler(obj)
                message.ack()  # msg handled properly and positive acknowledge
            except Exception as e:
                self.log.exception(str(e))
                message.nack()  # msg wasn't handled properly, negative acknowledge and requeue.

        queue = await self._channel.declare_queue()
        await queue.bind(self._exchange, routing_key=topic)
        await queue.consume(handler_wrapper)

    async def _wait_for_connection(self, retry=0):
        try:
            self._connection = await connect_robust(self.url, loop=self.loop)
        except ConnectionError:
            if retry < 5:
                await self.sleep(3)
                return await self._wait_for_connection(retry+1)
            raise
