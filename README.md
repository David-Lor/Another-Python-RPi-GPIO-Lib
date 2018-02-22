# Another-Python-RPi-GPIO-Lib

A very simple Python script for using Raspberry Pi GPIO. I wrote it because I coudln't install the widely used RPi-GPIO library on OpenWRT/LEDE.

Pins are initialized as objects. You can read and write digital values, as well as attach some sort of "interrupts" to the read pins (it's actually a looped polling over the pin value).

## Examples

### Write

```python
from GPIO import *

p4 = Pin(4, OUTPUT)

p4.write(HIGH)
p4.write(LOW)
p4.write(True)
p4.write(False)
p4.write(1)
p4.write(0)
```

### Read

```python
from GPIO import *

p4 = Pin(4, INPUT)

if p4.read():
    print("Pin is HIGH")
else:
    print("Pin is LOW")
```

### Interrupt

```python
from GPIO import *

def mydef():
    print("Pin changed!")

p4 = Pin(4, INPUT)

int_falling = p4.attach_interrupt(mydef, FALLING)
int_rising = p4.attach_interrupt(mydef, RISING)
int_both = p4.attach_interrupt(mydef, BOTH)

int_falling.start()
#mydef() will be executed when pin changes HIGH -> LOW
int_falling.stop()

int_rising.start()
#mydef() will be executed when pin changes LOW -> HIGH
int_rising.stop()

int_both.start()
#mydef() will be executed when pin changes any state (HIGH -> LOW or LOW -> HIGH)
int_both.stop()
```

### Interrupt with args

```python
from GPIO import *

def mydef(edgetype):
    print("Pin changed with edgetype:", edgetype)

p4 = Pin(4, INPUT)

int_falling = p4.attach_interrupt(mydef, FALLING, ("Falling (high to low)",))
int_rising = p4.attach_interrupt(mydef, RISING, ("Rising (low to high)",))
int_both = p4.attach_interrupt(mydef, BOTH, ("Both (pin changed value)",))

int_falling.start()
#mydef() will be executed when pin changes HIGH -> LOW
int_falling.stop()

int_rising.start()
#mydef() will be executed when pin changes LOW -> HIGH
int_rising.stop()

int_both.start()
#mydef() will be executed when pin changes any state (HIGH -> LOW or LOW -> HIGH)
int_both.stop()
```
