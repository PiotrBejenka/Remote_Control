import ustruct
from machine import Pin, SPI, ADC
from nrf24l01 import NRF24L01

xAxis = ADC(Pin(26))
yAxis = ADC(Pin(27))

pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")
   
csn = Pin(14, mode=Pin.OUT, value=1)
ce = Pin(17, mode=Pin.OUT, value=0)

nrf = NRF24L01(SPI(0), csn, ce, payload_size=8)
nrf.open_tx_pipe(pipes[0])
nrf.open_rx_pipe(1, pipes[1])


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
    
    try:
        nrf.send(ustruct.pack("i", direction))        
    except OSError:
        pass