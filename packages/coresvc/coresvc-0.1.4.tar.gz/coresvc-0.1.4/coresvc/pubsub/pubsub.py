from functools import cached_property
from typing import Iterable, Callable

from coresvc.base.base_service import BaseService
from coresvc.pubsub.consumer import Consumer
from coresvc.pubsub.producer import Producer


class PubSub(BaseService):
    def __init__(self, amqp_url, **kwargs):
        self.amqp_url = amqp_url
        super().__init__(**kwargs)

    def on_init_dependencies(self) -> Iterable[BaseService]:
        return [self.producer, self.consumer]

    async def on_started(self) -> None:
        self.log.info(self.label + 'started')

    async def publish(self, topic: str, msg: dict):
        await self.producer.publish(topic, msg)

    async def subscribe(self, topic: str, handler: Callable):
        await self.consumer.subscribe(topic, handler)

    @cached_property
    def producer(self):
        return Producer(self.amqp_url, loop=self.loop, beacon=self.beacon)

    @cached_property
    def consumer(self):
        return Consumer(self.amqp_url, loop=self.loop, beacon=self.beacon)
