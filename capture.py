"""Capture one million ADC samples (low 8 bits of each) to lon.bin on the Pico.

Takes about 4 minutes. Prints the GP27 level (photocurrent monitor) before and
after, and the noise estimate for each 50 000-sample segment.
"""
from machine import ADC
from array import array
import time

o = ADC(26)  # amplified noise signal (stage B output)
g = ADC(27)  # DC photocurrent monitor (stage A output)
N = 50000


def read_gp27():
    return sum(g.read_u16() for _ in range(200)) / 200 / 65535 * 3.3


def capture(nc=20):
    a = array('H', (0 for _ in range(N)))
    k = 3.3 / 4095 * 1000
    kq = []
    v0 = read_gp27()
    with open('lon.bin', 'wb') as f:
        for c in range(nc):
            for i in range(N):
                a[i] = o.read_u16() >> 4
                time.sleep_us(200)
            f.write(bytes(x & 255 for x in a))
            d = [a[i] - a[i - 1] for i in range(1, 4000)]
            kq.append(round((sum(x * x for x in d) / len(d) / 2) ** 0.5 * k, 1))
    print('GP27 start/end:', round(v0, 2), round(read_gp27(), 2))
    print('noise per segment (mV):', kq)


if __name__ == '__main__':
    capture()
