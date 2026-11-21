"""Random numbers from the photodiode noise, on the Pico.

Usage (in the REPL or Thonny shell):
    >>> import rng
    >>> rng.print_numbers(20, 100)
    >>> rng.roll_dice()
"""
from machine import ADC
import time

o = ADC(26)
prev = o.read_u16() >> 4


def rand_bit():
    global prev
    time.sleep_us(200)
    x = o.read_u16() >> 4
    b = (x ^ prev) & 1
    prev = x
    return b


def rand_int(n):
    """Uniform integer in [0, n) by rejection sampling."""
    k = 0
    while (1 << k) < n:
        k += 1
    while True:
        v = 0
        for _ in range(k):
            v = (v << 1) | rand_bit()
        if v < n:
            return v


def print_numbers(count=10, upper=100):
    print('Random integers in [0, %d):' % upper)
    print([rand_int(upper) for _ in range(count)])


def roll_dice(rolls=6000):
    counts = [0] * 6
    for _ in range(rolls):
        counts[rand_int(6)] += 1
    expected = rolls / 6
    chi2 = sum((c - expected) ** 2 / expected for c in counts)
    print('Rolled dice %d times' % rolls)
    for face in range(6):
        print('  face %d: %d' % (face + 1, counts[face]))
    print('Chi-square: %.2f (5 degrees of freedom, fair if < 11.07)' % chi2)
