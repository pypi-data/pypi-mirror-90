import json

import msgpack
import logging
import kafka

from .helpers import collect_tasks

FORMAT = '[%(asctime)-15s] [%(levelname)s:%(name)s] %(message)s'

logging.getLogger(kafka.__name__).setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.INFO, format=FORMAT)

logger = logging.getLogger('Kafka-Task-Handler')


def json_loader(json_text):  # TODO: Temporary fix
    return msgpack.loads(json_text, strict_map_key=False)


class KafkaHandler:

    _topics = None
    _group_name = None
    _consumer = None
    _handlers_map = None
    _ips = None
    log = logger

    def __init__(self, settings, consumer_kwargs=None):
        self._topics = getattr(settings, 'KAFKA_TOPICS', [])
        self._group_name = getattr(settings, 'KAFKA_GROUP', [])
        self._ips = getattr(settings, 'KAFKA_SERVERS', [])
        if not consumer_kwargs:
            consumer_kwargs = {}
        self._consumer = kafka.KafkaConsumer(value_deserializer=json_loader, bootstrap_servers=self._ips, **consumer_kwargs)
        modules = getattr(settings, 'KAFKA_TASKS_MODULES', [])
        self._handlers_map = collect_tasks(modules=modules, base_dir=getattr(settings, 'BASE_DIR', ''), logger=self.log)

    def __call__(self):
        self._consumer.subscribe(self._topics)
        self.log.info(f'Starting MS-Payment')
        for msg in self._consumer:
            self.handle(msg.value)
            self.log.info(f'Finished')

    def handle(self, value):
        """
        :var tasks: should set globally, only once, on handler start
        :param value: message from kafka
        """
        processors = self._handlers_map.get(value.get('action'), [])
        self.process_response(value, processors)

    def process_response(self, data, processors):
        try:
            if not processors:
                return
            if isinstance(processors, list):
                self.log.info(f'Got: {json.dumps(data, indent=4)}')
                [process(data) for process in processors]
            elif callable(processors):
                processors(data)
        except Exception as e:
            self.log.error(e)
