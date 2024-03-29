from gqlalchemy import Memgraph
from gdb_clients import GdbFactory
from configs.conf import config
import time
from gqlalchemy import models


class MemGraph(GdbFactory):
    def __init__(self):
        self.connection = Memgraph(host=config.get("memgraph", "uri"), port=config.getint("memgraph", "port"))
        print(f"Memgraph port={self.connection.port}")
        models.IGNORE_SUBCLASSNOTFOUNDWARNING = True
        self.clear()

    def run(self, query):
        start_time = time.time()
        res = self.connection.execute_and_fetch(query)
        execution_time = time.time() - start_time
        return list(res), execution_time*100000

    def batch_run(self, query):
        for q in query:
            self.connection.execute(q)

    def clear(self):
        self.connection.execute("MATCH (n) DETACH DELETE n")
