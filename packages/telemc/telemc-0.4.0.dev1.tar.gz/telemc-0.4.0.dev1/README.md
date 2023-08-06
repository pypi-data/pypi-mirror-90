telemc-py
=========

[![PyPI Version](https://badge.fury.io/py/telemc.svg)](https://badge.fury.io/py/telemc)

Library and client tools for accessing and recording [telemd](https://github.com/edgerun/telemd) monitoring data.


CLI
---

run `make install` and `source .venv/bin/activate` install locally. 

    % telemc --help
    usage: telemc [-h] [--redis-host REDIS_HOST] [--redis-port REDIS_PORT]
                  {list,info,pause,unpause,follow} ...
    
    positional arguments:
      {list,info,pause,unpause,follow}
                            telemc command
        list                list nodes
        info                show node info
        pause               pause telemetry reporting
        unpause             start telemetry reporting
        follow              subscribe to the telemetry data
    
    optional arguments:
      -h, --help            show this help message and exit
      --redis-host REDIS_HOST
                            redis host
      --redis-port REDIS_PORT
                            redis port

Library
-------

Usage examples

### Print telemetry:

```python
import redis
import telemc

rds = redis.Redis(decode_responses=True)

with telemc.TelemetrySubscriber(rds) as sub:
    for telem in sub:
        print(telem.timestamp, telem.node, ...)
```

Or use the higher-level `TelemetryRecorder`, which is a thread and can be extended to implement various recording
tools.

```python
import telemc
recorder = telemc.recorder.TelemetryPrinter(rds)
recorder.start()
``` 

### Pause all telemetry daemons

```python
ctrl = telemc.TelemetryController(rds)
ctrl.pause_all()
```
