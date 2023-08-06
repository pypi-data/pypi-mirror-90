from time import time, sleep
from confluent_kafka.admin import AdminClient, NewTopic, NewPartitions, ConfigResource
import confluent_kafka


class Admin(AdminClient):

    def create_or_update_topic(self, topic, num_partitions, replication_factor, config_dict):
        topic_configs = self.get_topic_configs(topic)

        if not topic_configs:
            self.create_topic_with_params(topic, num_partitions, replication_factor)
            topic_configs = self.get_topic_configs(topic)

        if topic_configs['num_partitions'] < num_partitions:
            self.set_topic_partitions(topic, num_partitions)

        is_equal_cnf = True
        for k, v in config_dict.items():
            if not topic_configs['configs'][k].value == str(v):
                is_equal_cnf = False

        if not is_equal_cnf:
            self.set_topic_configs(topic, {k: str(v) for k, v in config_dict.items()})

    def get_topic_configs(self, topic):
        topics_dict = self.list_topics(timeout=10).topics
        if topic not in topics_dict:
            return {}

        topic_md = topics_dict[topic]

        num_partitions = len(topic_md.partitions)
        replication_factor = len(topic_md.partitions[0].replicas)

        # noinspection PyTypeChecker
        fs = self.describe_configs([ConfigResource('topic', topic), ])

        # Wait for operation to finish.
        configs = {}
        for res, f in fs.items():
            try:
                configs = f.result()
            except confluent_kafka.KafkaException as e:
                print("Failed to describe {}: {}".format(res, e))
                raise
            except Exception:
                raise

        return dict(num_partitions=num_partitions,
                    replication_factor=replication_factor, configs=configs)

    def create_topic_with_params(self, topic, num_partitions, replication_factor, timeout=10):
        topic_md = NewTopic(topic,
                            num_partitions=num_partitions,
                            replication_factor=replication_factor)

        fs = self.create_topics([topic_md, ])

        # Wait for operation to finish.
        # Timeouts are preferably controlled by passing request_timeout=15.0
        # to the create_topics() call.
        # All futures will finish at the same time.
        t = time()
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                while (time() - t) < timeout:
                    topics_dict = self.list_topics(timeout=10).topics
                    if topic in topics_dict:
                        print("Topic {} created".format(topic))
                        return

                    sleep(0.1)

                raise Exception(f'Timeout {timeout}s on creating topic {topic} expired')
            except confluent_kafka.KafkaException as e:
                if e.args[0].name() == 'INVALID_REPLICATION_FACTOR':
                    replication_factor = int(e.args[0].str().split('brokers:')[-1][:-1])
                    print(f"Topic {topic} will created with replication_factor = {replication_factor}")
                    return self.create_topic_with_params(topic, num_partitions, replication_factor, timeout)
                else:
                    raise



            except Exception as e:
                print("Failed to create topic {}: {}".format(topic, e))
                raise

    def set_topic_configs(self, topic, config_dict):
        # noinspection PyTypeChecker
        resource = ConfigResource('topic', topic)
        for k, v in config_dict.items():
            resource.set_config(k, v)
            print(k, v)

        fs = self.alter_configs([resource, ])

        for res, f in fs.items():
            try:
                f.result()  # empty, but raises exception on failure
                print("{} configuration successfully altered".format(res))
            except Exception:
                raise

        return resource

    def set_topic_partitions(self, topic, new_total_count):
        """ create partitions """

        new_parts = [NewPartitions(topic, int(new_total_count))]

        # Try switching validate_only to True to only validate the operation
        # on the broker but not actually perform it.
        fs = self.create_partitions(new_parts, validate_only=False)

        # Wait for operation to finish.
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print(f"Additional partitions created for topic {topic} now there are {new_total_count}")
            except Exception as e:
                print("Failed to add partitions to topic {}: {}".format(topic, e))
