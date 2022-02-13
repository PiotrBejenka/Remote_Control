import usys
import ustruct as struct
import utime
from machine import Pin, SPI, ADC
from nrf24l01 import NRF24L01
from micropython import const


xAxis = ADC(Pin(26))
yAxis = ADC(Pin(27))
readDelay = 0.1


pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

def master(msg):
    csn = Pin(14, mode=Pin.OUT, value=1)
    ce = Pin(17, mode=Pin.OUT, value=0)

    nrf = NRF24L01(SPI(0), csn, ce, payload_size=8)

    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])
    nrf.start_listening()

    num_needed = 1
    num_successes = 0
    num_failures = 0

    while num_successes < num_needed and num_failures < num_needed:
        nrf.stop_listening()
        millis = utime.ticks_ms()
        print("sending:", msg)
        try:
            nrf.send(struct.pack("ii", msg))
        except OSError:
            pass

        nrf.start_listening()

        start_time = utime.ticks_ms()
        timeout = False
        while not nrf.any() and not timeout:
            if utime.ticks_diff(utime.ticks_ms(), start_time) > 250:
                timeout = True

        if timeout:
            num_failures += 1

        else:
            (got_msg,) = struct.unpack("i", nrf.recv())
            num_successes += 1

        utime.sleep_ms(250)


while True:
    xRef = xAxis.read_u16()
    yRef = yAxis.read_u16()

    direction = 0
    
    if yRef <= 600:
        direction = 2
    elif yRef >= 60000:
        direction = 8
        
    if xRef <= 600:
        direction = 4
    elif xRef >= 60000:
        direction = 6    
    
    master(direction)
    
    utime.sleep(readDelay)