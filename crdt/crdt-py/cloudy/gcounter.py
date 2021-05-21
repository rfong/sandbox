#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# A simple growth-only CRDT.
# See acobster's notes: https://acobster.keybase.pub/recurse/crdts

import logging

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.INFO)

class GCounter(object):
    '''An increment-only CRDT store.'''

    def __init__(self, idx, pubsub):
        self.idx = idx
        self.ps = pubsub

        # State is a map of known node IDs to node values.
        self._state = {self.idx: 0}

        # Subscribe self for state updates
        self.ps.subscribe(self.idx, self._join)

    # Public interface

    def increment(self):
        '''Increment the counter for this instance.'''
        logger.info("Increment Node %d" % self.idx)
        self._state[self.idx] += 1
        self.ps.publish(state=self._state)

    def value(self):
        '''Request the current global "value", or sum of state counts'''
        return sum(v for k, v in self._state.items())

    # Internal state management

    def _join(self, state):
        '''Merge a published state update into our internal state.'''
        logger.debug("Node %d %s - received %s" % (self.idx, str(self._state), str(state)))
        self._state = {
            idx: max(state.get(idx, 0), self._state.get(idx, 0))
            for idx in set(state.keys()).union(self._state.keys())
        }
        logger.debug("\t->", self._state)
