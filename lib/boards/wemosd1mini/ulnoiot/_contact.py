# Contact Device
# author: ulno
# created: 2017-04-08

import machine
from machine import Pin
from ulnoiot.device import Device

####### simple Input, contact devices/push buttons
class Contact(Device):
    # Handle contact or button like devices
    def __init__(self, name, pin, *args,
                 report_high="on", report_low="off",
                 pullup=True, threshold=0):
        if len(args) > 0:
            report_high = args[0]
            if len(args) > 1:
                report_low = args[1]
        Device.__init__(self, name, pin,
                        value_map={True: report_high.encode(), False: report_low.encode()})
        pin.init(Pin.IN);
        if pullup:
            pin.init(Pin.PULL_UP)
        else:
            pin.init(Pin.OPEN_DRAIN)
        self.debouncer = 0
        self.threshold = threshold + 1

    def value(self):
        return self.debouncer >= self.threshold

    def _update(self):
        # Needs to be read in a polling scenario on a regular basis (very frequent)
        if self.pin() == 1:
            self.debouncer += 1
            if self.debouncer > self.threshold * 2:
                self.debouncer = self.threshold * 2
        else:
            self.debouncer -= 1
            if self.debouncer < 0:
                self.debouncer = 0


Button = Contact