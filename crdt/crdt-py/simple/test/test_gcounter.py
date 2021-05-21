#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import unittest

from gcounter import GCounter
from pubsub import PubSub

class GCounterTest(unittest.TestCase):

    def test_integrated(self):
        '''Test some nodes hooked up with a pub/sub'''
        pubsub = PubSub()
        nodes = [GCounter(idx, pubsub) for idx in range(3)]
    
        for i in range(100):
            # Pick a random node and increment it
            node = random.choice(nodes)
            node.increment()
            # All .value() checks should have the same result
            self.assertTrue(all(n.value() == node.value() for n in nodes))
