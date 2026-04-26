from machine import Pin, SoftI2C
import time
import ssd1306
    
class MachineState:
    IDLE = "IDLE"
    MOVING_UP = "MOVING_UP"
    MOVING_DOWN = "MOVING_DOWN"
    OPPENING = "OPPENING"
    
def btn_pin(pin_number):
    return Pin(pin_number, Pin.IN, Pin.PULL_DOWN)

def led_pin(pin_number):
    return Pin(pin_number, Pin.OUT)

class Floor:
    def __init__(self, btn_pin: number, led_pin: number):
        self.btn_pin = btn_pin
        self.led_pin = led_pin
        
    def is_pressed(self):
        return self.btn_pin.value() == 1
    
    def led_on(self):
        self.led_pin.value(1)
        
    def led_off(self):
        self.led_pin.value(0)
        
    def blink(self, duration: number = 0.3):
            self.led_on()
            time.sleep(duration)
            self.led_off()
            
floors = {
    5: Floor(btn_pin(15), led_pin(16)),
    4: Floor(btn_pin(14), led_pin(17)),
    3: Floor(btn_pin(13), led_pin(18)),
    2: Floor(btn_pin(12), led_pin(19)),
    1: Floor(btn_pin(11), led_pin(20))
}

def move_one_floor(current, target):
    floors[current].blink()
    return (current + 1, MachineState.MOVING_UP) if target > current else (current - 1, MachineState.MOVING_DOWN)

floors[1].led_on()
machine_state = MachineState.IDLE
current_floor = 1
target_floor = None
moving = False

i2c = SoftI2C(scl=Pin(1), sda=Pin(0))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

printed_floor = 1
oppening_ticks = 30
current_oppening_tick = 0

while True:
    if not moving:
        for number, floor in floors.items():
            if floor.is_pressed():
                target_floor = number
                moving = current_floor != target_floor
                break
    
    if machine_state == MachineState.OPPENING:
        if current_oppening_tick == oppening_ticks:
            machine_state = MachineState.IDLE
            current_oppening_tick = 0
        else:
            current_oppening_tick = current_oppening_tick + 1
            oled.fill(0)
            oled.text(("<" if current_oppening_tick % 5 else " < - ") + ("> " if current_oppening_tick % 5 else ">"), 50, 20)
            oled.show()
    
    if moving:
        current_floor, machine_state = move_one_floor(current_floor, target_floor)
        
        if current_floor == target_floor:
            floors[current_floor].led_on()
            moving = False
            machine_state = MachineState.OPPENING
        
    if(printed_floor != current_floor):
        printed_floor = current_floor
        oled.fill(0)
        oled.show()
        
        
    icon = ""
    if(machine_state == MachineState.MOVING_UP):
        icon = "^"
    elif(machine_state == MachineState.MOVING_DOWN):
        icon = "v"
        
    if machine_state != MachineState.OPPENING:    
        oled.fill(0)
        oled.text(str(current_floor) + " " + icon, 50, 32)
        oled.show()
    
    print(machine_state)
    time.sleep(0.1)
            
