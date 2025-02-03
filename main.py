import array, time
from machine import Pin
import rp2

NUM_LEDS = 16
PIN = 6
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2; T2 = 5; T3 = 3
    label("bitloop")
    out(x, 1)               .side(0) [T3 - 1]
    jmp(not_x, "do_zero")   .side(1) [T1 - 1]
    jmp("bitloop")          .side(1) [T2 - 1]
    label("do_zero")
    nop()                   .side(0) [T2 - 1]

state = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN))
state.active(1)

def show(pixels):
    arr = array.array("I", (0 for _ in range(NUM_LEDS)))
    for i, (r,g,b) in enumerate(pixels):
        arr[i] = (g<<16) | (r<<8) | b
    state.put(arr, 8)

def wheel(pos):
    if pos < 85:
        return (pos*3, 255 - pos*3, 0)
    if pos < 170:
        pos -= 85
        return (255 - pos*3, 0, pos*3)
    pos -= 170
    return (0, pos*3, 255 - pos*3)

pixels = [(0,0,0)]*NUM_LEDS
while True:
    for j in range(256):
        for i in range(NUM_LEDS):
            pixels[i] = wheel((i*8 + j) & 255)
        show(pixels)
        time.sleep_ms(20)
