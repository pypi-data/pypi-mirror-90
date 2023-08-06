# virtual-pi
Virtual Pi Library for mocking Raspberry Pi

The easiest way to use this package is to install using pip3 for python 3

```bash
$ sudo pip3 install virtual-pi
```

To use the mock or virtual pi just type the following at the beginning of your script.

```python
try:
      from RPi.GPIO import GPIO
      import board
      import busio
except:
      from VPi.GPIO import GPIO
      import VPi.board as board
      import VPi.busio as busio
```

## Works with

- [python 3.6.8](https://www.python.org/downloads/release/3.6.8)
### Usage:

``` python
import Mock.GPIO as GPIO
```

## Documentation

- [Library Overview](https://htmlpreview.github.io/?https://github.com/codenio/Mock.GPIO/blob/master/docs/Mock.GPIO.html)
- [Examples](examples)

### Example:

The following python example/test.py

```python

try:
    import RPi.GPIO as GPIO    
except:
    import VPi.GPIO as GPIO

import time

print ("set mode")
GPIO.setmode(GPIO.BCM)
print ("set warning false")
GPIO.setwarnings(False)
GPIO.setup(15,GPIO.OUT)
GPIO.output(15,GPIO.HIGH)
time.sleep(1)
GPIO.output(15,GPIO.LOW)
```

generates following output

```shell
$ export LOG_LEVEL=Info
$ python examples/test.py 
set mode
set warning false
2020-05-07 17:49:23,031:INFO: Set Warings as False
2020-05-07 17:49:23,031:INFO: setup channel : 15 as 0 with intial :0 and pull_up_dowm 20
2020-05-07 17:49:23,032:INFO: output channel : 15 with value : 1
2020-05-07 17:49:24,033:INFO: output channel : 15 with value : 0
```
