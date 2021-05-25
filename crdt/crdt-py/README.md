crdt-py
-----

Simple grow-only counter CRDT exploration (nonconcurrent) written in Python. All counters will eventually converge on the same value.

Thanks to [`acobster`](https://github.com/acobster) for pairing on a [clj gcounter](https://github.com/acobster/recurse/blob/master/crdt/gcounter.clj) and sharing [these excellent notes](https://acobster.keybase.pub/recurse/crdts) on John Mumm's [Defanging Order Theory](https://www.youtube.com/watch?v=OOlnp2bZVRs) talk.

# Demo

Basic demo:
```
python simple/demo.py
```

With fake latency & robustness to nodes "crashing":
```
python cloudy/demo.py
```

# Unit tests

```
cd ..
python -m unittest discover crdt-py
```
