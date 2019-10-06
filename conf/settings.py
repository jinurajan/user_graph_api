

class AppConfig(object):

    @property
    def cassandra_hosts(self):
        return ["127.0.0.1"]

    @property
    def port(self):
        return 5000


Config = AppConfig()