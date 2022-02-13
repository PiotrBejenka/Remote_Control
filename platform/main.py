import ustruct
from machine import Pin, SPI, PWM
from nrf24l01 import NRF24L01

PWM_A = PWM(Pin(8))
A_IN_1 = Pin(10, Pin.OUT)
A_IN_2 = Pin(9, Pin.OUT)

PWM_B = PWM(Pin(15))
B_IN_1 = Pin(12, Pin.OUT)
B_IN_2 = Pin(13, Pin.OUT)

STBY = Pin(11, Pin.OUT)

PWM_A.freq(1000)
PWM_B.freq(1000)
duty = 30000

def Forward():
    A_IN_1.value(1)
    A_IN_2.value(0)
    PWM_A.duty_u16(duty)
    
    B_IN_1.value(0)
    B_IN_2.value(1)
    PWM_B.duty_u16(duty)
   
    STBY.value(1)
    
def Backward():
    A_IN_1.value(0)
    A_IN_2.value(1)
    PWM_A.duty_u16(duty)
    
    B_IN_1.value(1)
    B_IN_2.value(0)
    PWM_B.duty_u16(duty)
   
    STBY.value(1)
    
def Left():
    A_IN_1.value(1)
    A_IN_2.value(0)
    PWM_A.duty_u16(duty)
    
    B_IN_1.value(1)
    B_IN_2.value(0)
    PWM_B.duty_u16(duty)
   
    STBY.value(1)

def Right():
    A_IN_1.value(0)
    A_IN_2.value(1)
    PWM_A.duty_u16(duty)
    
    B_IN_1.value(0)
    B_IN_2.value(1)
    PWM_B.duty_u16(duty)
   
    STBY.value(1)
    
def Stop():
    A_IN_1.value(0)
    A_IN_2.value(0)
    PWM_A.duty_u16(0)
    
    B_IN_1.value(0)
    B_IN_2.value(0)
    PWM_B.duty_u16(0)
    
    STBY.value(0)

pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

csn = Pin(14, mode=Pin.OUT, value=1)
ce = Pin(17, mode=Pin.OUT, value=0)
    
nrf = NRF24L01(SPI(0), csn, ce, payload_size=8)
nrf.open_tx_pipe(pipes[1])
nrf.open_rx_pipe(1, pipes[0])
nrf.start_listening()


while True:
    
    while nrf.any():
        
        buf = nrf.recv()
        dir, = ustruct.unpack("i", buf)
                
        if dir == 0:
            Stop()
        if dir == 8:
            Forward()
        if dir == 2:
            Backward()
        if dir == 4:
            Left()
        if dir == 6:
            Right()