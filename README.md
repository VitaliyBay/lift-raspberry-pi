# lift-raspberry-pi

Learning project for basic electronics + MicroPython on a Raspberry Pi Pico.

## Purpose
Build a small “lift panel” (buttons + LEDs + OLED) while learning:
- GPIO inputs (buttons with pull-down)
- GPIO outputs (LEDs with resistors)
- Simple state machines (idle/moving/opening)
- I2C basics (OLED screen)

The repo is split into iterations so it reads like a tutorial: each iteration builds on the previous one.

## Index
- Iteration 1: `iteration1/README.md`
- Iteration 2: `iteration2/README.md`
- Iteration 3: `iteration3/README.md`

## Hardware
Minimum for iterations 1–2:
- Raspberry Pi Pico / Pico W
- 5x push buttons (one per floor)
- 5x LEDs
- 5x resistors for LEDs (typically **220Ω–330Ω**)
- Breadboard + jumper wires

Extra for iteration 3:
- SSD1306 OLED display (commonly 128x64, I2C)
- 4 more jumper wires (VCC, GND, SDA, SCL)

## Pin mapping (Iterations 1–3)
The wiring below matches `iteration1/Lift_v1.py`, `iteration2/Lift_v2.py`, and `iteration3/Lift_v3.py`.

| Floor | Button GPIO | LED GPIO |
|------:|------------:|---------:|
| 1     | GP11        | GP20     |
| 2     | GP12        | GP19     |
| 3     | GP13        | GP18     |
| 4     | GP14        | GP17     |
| 5     | GP15        | GP16     |

OLED (iteration 3):
- `SDA = GP0`
- `SCL = GP1`

## Wiring
### Buttons (inputs)
In code the buttons are created as `Pin.IN` with `Pin.PULL_DOWN`.
That means the input is normally **LOW (0)**, and becomes **HIGH (1)** when you connect it to **3V3**.

Wire each button like this:
- One leg of the button → **3V3(OUT)** on the Pico
- The other leg of the button → the floor’s **Button GPIO** (GP11..GP15)

Notes:
- No external resistor is required for the buttons because the Pico’s internal pull-down is enabled.
- On a 4‑pin tactile button, the two pins on the same side are internally connected; place it across the breadboard gap so you don’t short the same side.

### LEDs (outputs)
Each floor LED is driven from its GPIO as a digital output.

Wire each LED like this (recommended):
- Floor **LED GPIO** → **resistor (220Ω–330Ω)** → **LED anode** (long leg)
- **LED cathode** (short leg) → **GND**

Notes:
- Always use a resistor with an LED to limit current.
- Ensure all grounds are common (LED cathodes go to Pico GND).

### OLED (Iteration 3)
The OLED uses **I2C**, a 2‑wire bus:
- **SDA**: data
- **SCL**: clock

Typical connections (SSD1306 I2C modules):
- OLED `VCC` → Pico `3V3(OUT)`
- OLED `GND` → Pico `GND`
- OLED `SDA` → Pico `GP0`
- OLED `SCL` → Pico `GP1`

## Software setup
This repo uses **MicroPython** on the Pico.

Typical workflow:
1. Flash MicroPython firmware onto the Pico.
2. Copy the iteration script to the Pico as `main.py` (or run it from your IDE).

Scripts:
- Iteration 1: `iteration1/Lift_v1.py`
- Iteration 2: `iteration2/Lift_v2.py`
- Iteration 3: `iteration3/Lift_v3.py`

## Code basics (used in Iteration 1–3)
All iterations share the same small “building blocks” so the code stays easy to evolve.

### `btn_pin(pin_number)`
Creates a GPIO input configured as:
- `Pin.IN` (input)
- `Pin.PULL_DOWN` (internal pull-down resistor enabled)

So the button reads `0` normally, and reads `1` when you press it (because the button connects the GPIO to 3V3).

### `led_pin(pin_number)`
Creates a GPIO output configured as `Pin.OUT`.
The code sets it to `1` to turn the LED on and `0` to turn it off (through your LED+resistor wiring).

### `Floor` class
Represents one floor “station” (a button + an LED).

Methods:
- `is_pressed()` → returns `True` when the button GPIO reads `1`
- `led_on()` / `led_off()` → control the LED GPIO
- `blink()` (iterations 2–3) → briefly turn LED on then off (used for the travel animation)

### `floors` dictionary
`floors` is a dictionary that maps a floor number (1..5) to a `Floor` object:
- Key: floor number (`int`)
- Value: `Floor(btn_pin(...), led_pin(...))`

This makes it easy to loop over all floors, read buttons, and control LEDs without duplicating code.

### OLED driver (Iteration 3)
Iteration 3 adds:
- `SoftI2C` to create an I2C bus on GPIO pins
- `ssd1306.py` driver (`SSD1306_I2C`) to draw text and update the display

## Safety / tips
- The Pico GPIOs are **3.3V** logic (do not use 5V on GPIO pins).
- If an LED doesn’t light: flip it (polarity), check resistor + ground.
- If a button behaves “noisy”: increase the debounce delay in code.
