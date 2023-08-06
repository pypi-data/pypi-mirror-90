import os
import json
import uuid
from time import time, sleep
from kafka_admin import Admin
import confluent_kafka
from threading import Lock, Thread

import signal

class KafkaCompaction:
    def __init__(self,
                 admin_configs,
                 collection_names,
                 db_name='fabrique.configs',
                 on_consumer_kill=lambda: os._exit(0)):

        if not collection_names:
            raise Exception('At least one collection must be set in "collection_names"')

        self.admin = Admin(admin_configs)
        self.db_name = db_name
        self.on_consumer_kill = on_consumer_kill

        cons_conf = admin_configs.copy()
        cons_conf['session.timeout.ms'] = 6000
        cons_conf['auto.offset.reset'] = 'earliest'  # !!!
        cons_conf['enable.auto.commit'] = False
        cons_conf['group.id'] = str(uuid.uuid4())

        self.consumer = confluent_kafka.Consumer(cons_conf)
        self.producer = confluent_kafka.Producer(admin_configs)
        self.locks = {}
        self.collection_callbacks = {}
        self._topics = {f"{db_name}.{n}": {} for n in collection_names}
        for topic in self._topics:
            self.create_compacted_topic(topic)

        self.consumer_num_messages = 1
        self.consumer_timeout_s = 0.1
        self.cons_running = True


        signal.signal(signal.SIGTERM, self.close)
        signal.signal(signal.SIGINT, self.close)

        self.cons_thr = Thread(target=self.start_consumer)
        self.cons_thr.setDaemon(True)
        self.cons_thr.start()

        self._inited = False
        while not self._inited:
            sleep(0.1)
        # print('KafkaCompaction inited')

    def add_collection_callback(self, collection_name, callback):
        topic = f'{self.db_name}.{collection_name}'
        self.collection_callbacks[topic] = callback


    def start_consumer(self, init_timeout=10.0):
        start_time = time()
        already_has_some_messages = False
        topic_list = list(self._topics.keys())
        try:
            self.consumer.subscribe(topic_list)
            print('Consumer topic_list:', topic_list)
            while self.cons_running:
                msgs = self.consumer.consume(num_messages=self.consumer_num_messages, timeout=self.consumer_timeout_s)
                if not msgs:
                    if already_has_some_messages:
                        if not self._inited:
                            print("KafkaCompaction Inited, already has some messages")
                            self._inited = True
                    if time() - start_time > init_timeout:
                         if not self._inited:
                            print("KafkaCompaction Inited, no msg in topics")
                            self._inited = True

                    continue
                # msg = self.consumer.poll(timeout=self.consumer_timeout_s)
                # if msg is None:
                #    continue
                for msg in msgs:
                    if msg.error():
                        if msg.error().code() == confluent_kafka.KafkaError._PARTITION_EOF:
                            pass

                        elif msg.error():
                            raise confluent_kafka.KafkaException(msg.error())
                    else:
                        already_has_some_messages = True
                        topic = msg.topic()
                        # print(f'Consumed mes from topic {topic}')
                        if topic not in self.locks:
                            self.locks[topic] = Lock()
                        # print(f"{topic} {msg.key()} = {msg.value()}")
                        self.locks[topic].acquire()
                        if msg.value() is not b'':
                            self._topics[topic][msg.key()] = msg.value()
                        else:
                            self._topics[topic].pop(msg.key(), 0)
                        self.locks[topic].release()

                        if topic in self.collection_callbacks:
                            if self._inited:
                                self.collection_callbacks[topic]()

        finally:
            # Close down consumer to commit final offsets.
            try:
                self.consumer.close()
                print('Consumer was correctly killed')
            finally:
                self.on_consumer_kill()


    def set_collection_value(self, name, key, value):
        topic = f'{self.db_name}.{name}'
        if topic not in self.locks:
            self.locks[topic] = Lock()

        self.locks[topic].acquire()

        if self._topics.get(topic):
            if self._topics[topic].get(key) == value:
                # print(f'not produce to {topic} with {key}, same value')
                self.locks[topic].release()
                return
        # print(f'produce to {topic} with {key} ', value)
        self.producer.produce(topic, value=value, key=key)
        self.producer.flush()
        self.locks[topic].release()
        sleep(1.0)

    def create_compacted_topic(self, topic):
        self.admin.create_or_update_topic(topic, 1, 3, {"cleanup.policy": "compact",
                                                        "delete.retention.ms": "100",
                                                        "segment.ms": "100",
                                                        "min.cleanable.dirty.ratio": "0.01"})

    def close(self, arg1=None, arg2=None):
        # print(arg1, arg2)
        self.cons_running = False

    def __del__(self):
        self.close()


    def __exit__(self, exception_type=None, exception_value=None, traceback=None):
        self.close()



class KafkaJsonCompaction(KafkaCompaction):
    def get_collections(self):
        return [c.replace(f'{self.db_name}.', '') for c in self._topics]

    def set_collection_value(self, name, key, value):
        if value is None:
            super().set_collection_value(name, key.encode(), b'')
            return
        super().set_collection_value(name, key.encode(), json.dumps(value, default=str))

    def delete_collection_value(self, name, key):
        self.set_collection_value(name, key, None)

    def get_collection_value(self, name, key):
        topic = f'{self.db_name}.{name}'
        try:
            self.locks[topic].acquire()
            js_val = self._topics[topic][key.encode()]
            value = json.loads(js_val)
            #self.locks[topic].release()
            return value

        except KeyError:
            return None

        finally:
            if topic in self.locks:
                self.locks[topic].release()

    def get_collection_keys(self, name):
        topic = f'{self.db_name}.{name}'
        try:
            self.locks[topic].acquire()
            keys = [k.decode() for k in list(self._topics[topic].keys())]
            #self.locks[topic].release()
            return keys

        except KeyError:
            return []

        finally:
            if topic in self.locks:
                self.locks[topic].release()