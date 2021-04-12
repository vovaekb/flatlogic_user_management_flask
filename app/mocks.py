#
# Use: mock.js in NodeJS backend
#

import math
from random import random

def get_revenue_data():
    print('get_revenue_data')
    data = []
    series_count = 3
    accessories = ['SMX', 'Direct', 'Networks']

    for i in range(series_count):
        data.append({
            'label': accessories[i],
            'data': math.floor(random() * 100) + 1,
        })
    return data


def get_random_data(length, min, max, multiplier = 10, max_diff = 10):
    array = []
    last_value = None

    for i in range(length):
        random_value = math.floor(random() * multiplier + 1)
        while random_value <= min or \
            random_value >= max or \
                    (last_value and random_value - last_value > max_diff):
            random_value = math.floor(random() * multiplier + 1)

        last_value = random_value
        array.append(random_value)

    return array


def get_main_chart_data():
    d1 = get_random_data(31, 3500, 6500, 7500, 1000)
    d2 = get_random_data(31, 1500, 7500, 7500, 1500)
    d3 = get_random_data(31, 1500, 7500, 7500, 1500)
    return [d1, d2, d3]

mock = {
  'analytics': {
      'visits': {
          'count': 4.332,
          'logins': 830,
          'sign_out_pct': 0.5,
          'rate_pct': 4.5
      },
      'performance': {
          'sdk': {
              'this_period_pct': 60,
              'last_period_pct': 30,
          },
          'integration': {
              'this_period_pct': 40,
              'last_period_pct': 55,
          }
      },
      'server': {
          '1': {
              'pct': 60,
              'temp': 37,
              'frequency': 3.3
          },
          '2': {
              'pct': 54,
              'temp': 31,
              'frequency': 3.3
          }
      },
      'revenue': get_revenue_data(),
      'mainChart': get_main_chart_data()
  }
}