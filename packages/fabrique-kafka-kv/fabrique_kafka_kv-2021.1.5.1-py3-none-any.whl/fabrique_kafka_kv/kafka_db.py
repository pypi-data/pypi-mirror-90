from fabrique_kafka_kv.kafka_compaction import KafkaJsonCompaction

class Kollection:
    def __init__(self, kdb, name):
        self.kdb = kdb
        self.name = name

    def __contains__(self, item):
        return item in self.kdb.get_collection_keys(self.name)

    def items(self):
        return ((key, self.kdb.get_collection_value(self.name, key)) for key in self.kdb.get_collection_keys(self.name))

    def __getitem__(self, key):
        return self.kdb.get_collection_value(self.name, key)

    def __setitem__(self, key, value):
        self.kdb.set_collection_value(self.name, key, value)

    def __delitem__(self, key):
        """del db[][key]"""
        self.kdb.delete_collection_value(self.name, key)


class KafkaDB(KafkaJsonCompaction):
    """если коллекция не залочена, то ее можно читать"""

    #def __new__(cls, *args, **kwargs):
    #    """Singleton"""
    #    if not hasattr(cls, 'instance'):
    #        cls.instance = super(KafkaDB, cls).__new__(cls, *args, **kwargs)
    #    return cls.instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collections = {}

    def __getitem__(self, key):
        if key not in self.collections:
            self.collections[key] = Kollection(self, key)
        return self.collections[key]

    def __setitem__(self, key, value):
        if key not in self.collections:
            self.collections[key] = Kollection(self, key)
        if not isinstance(value, dict):
            raise TypeError
        for k, v in value.items():
            self.collections[key][k] = v