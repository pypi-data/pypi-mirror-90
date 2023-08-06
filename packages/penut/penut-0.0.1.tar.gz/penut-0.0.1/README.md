# Penut

## Introduction
+ This package is a collection of my useful functions, including some useful IO operations.

## Installation
+ You can install this package through pip:
  ```bash
  $ pip install penut
  ```

## Usage
+ Easily load or dump and json/pkl/csv/npy file:
  ```python
  import penut.io as pio

  data = pio.load('data.json')
  data = pio.load('data.pkl')
  data = pio.load('data.csv')
  data = pio.load('data.npy')

  pio.dump(data, 'data.json')
  pio.dump(data, 'data.pkl')
  pio.dump(data, 'data.csv')
  pio.dump(data, 'data.npy')
  ```
+ Easily measure the execution time of code:
  ```python
  import time
  from penut import TimeCost

  with TimeCost('Sleep Time'):
      time.sleep(1)
  # Output: Sleep Time: 1.000262s

  # With custom format
  fmt = lambda msg, tts: f'Hello {msg}, you cost {tts:.2f}s!!'
  with TimeCost('Custom Format', verbose_fmt=fmt):
      time.sleep(1)
  # Output: Hello Custom Format, you cost 1.00s!!
  ```
+ Easily convert `datetime.timedelta` to string:
  ```python
  from penut import td2s
  from datetime import datetime

  a = datetime(2021, 1, 6, 11, 32, 23)
  b = datetime(2021, 1, 7, 12, 38, 17)
  d = b - a

  print(td2s(d)) # 62:17:54

  fmt = lambda h, m, s: f'{h}h{m}m{s}s'
  print(td2s(d, fmt)) # 62h17m54s
  ```