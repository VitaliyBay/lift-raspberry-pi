from machine import Pin
import time
    
def btn_pin(pin_number: int):
    return Pin(pin_number, Pin.IN, Pin.PULL_DOWN)

def led_pin(pin_number: int):
    return Pin(pin_number, Pin.OUT)

class Floor:
    def __init__(self, btn_pin: Pin, led_pin: Pin):
        self.btn_pin = btn_pin
        self.led_pin = led_pin
        
    def is_pressed(self):
        return self.btn_pin.value() == 1
    
    def led_on(self):
        self.led_pin.value(1)
        
    def led_off(self):
        self.led_pin.value(0)
            
floors = {
    5: Floor(btn_pin(15), led_pin(16)),
    4: Floor(btn_pin(14), led_pin(17)),
    3: Floor(btn_pin(13), led_pin(18)),
    2: Floor(btn_pin(12), led_pin(19)),
    1: Floor(btn_pin(11), led_pin(20))
}


floors[1].led_on()
current_floor = 1

while True:
    
    for number, floor in floors.items():
        if floor.is_pressed():
            floor.led_on()
            current_floor = number
        elif number is not current_floor:
            floor.led_off()

    print(current_floor)
    time.sleep(0.1)
            
