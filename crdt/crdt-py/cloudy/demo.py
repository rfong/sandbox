#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Demo script

import logging
import random

from cloudy import CloudyGCounter, CloudyPubSub, CloudyException
from gcounter import GCounter
from pubsub import PubSub


logger = logging.getLogger("main")
logging.basicConfig()
logger.setLevel(logging.INFO)

def latency_demo():
    '''Demo gCRDT with latency'''
    ps = CloudyPubSub(CloudyException)
    nodes = [GCounter(idx, ps) for idx in range(3)]

    for i in range(10):
        node = random.choice(nodes)
        node.increment()
        for n in nodes:
            print("Node %d says %d" % (n.idx, n.value()))


class NodeManager(object):
    '''Fake node manager. Drop crashed nodes and spin up replacements'''
    def __init__(self, capacity):
        self.capacity = capacity
        self.pubsub = PubSub(CloudyException)
        self.nodes = {
            idx: CloudyGCounter(idx, self.pubsub) for idx in range(capacity)}

    def increment(self):
        node = random.choice(list(self.nodes.values()))
        try:
            node.increment()
        except CloudyException:
            logger.error("Node %d crashed while incrementing." % node.idx)
            self.replace_node(node.idx)
            logger.info("Retrying...")
            self.increment()
            return
        for idx, n in self.nodes.items():
            try:
                print("Node %d says %d" % (n.idx, n.value()))
            except CloudyException:
                logger.error("Node %d crashed while checking value." % node.idx)
                self.replace_node(node.idx)

    def replace_node(self, idx):
        '''Spin up a new node (with a new id) to replace node <idx>.'''
        if idx not in self.nodes:
            return
        # Pick an id larger than that of any previously existing node.
        new_idx = max(self.nodes.keys()) + 1
        # Drop crashed node.
        del self.nodes[idx]
        # Set up a new node.
        self.nodes[new_idx] = CloudyGCounter(new_idx, self.pubsub)
        logger.info("Spawned node %d to replace node %d." % (new_idx, idx))


def crashy_demo():
    '''Demo gCRDT with crashing nodes'''

    manager = NodeManager(5)
    for i in range(10):
        manager.increment()


if __name__ == '__main__':
    print("DEMO WITH LATENCY")
    latency_demo()

    print("DEMO WITH CRASHING")
    crashy_demo()
