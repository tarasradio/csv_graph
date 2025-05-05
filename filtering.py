import numpy as np
import math

def exponential_smoothing(series, alpha):
  new_data = [series[0]]  # [0] первое значение совпадает со значением временного ряда
  for i in range(1, len(series)):
    new_data.append(series[i] * alpha + (1 - alpha) * new_data[-1])
  return new_data

def moving_average(data, smooth_interval=2):
  if(smooth_interval > len(data)):
    print("Smooth interval > lenght of data")
    return
  
  sum = 0
  new_data = np.zeros(len(data))

  for i in range (smooth_interval):
    for j in range(smooth_interval):
      sum += data[i+j]
    average = sum/smooth_interval
    new_data[i] = average
    sum = 0

  for i in range(len(data)-smooth_interval):
    for j in range(smooth_interval):
      sum += data[i+j]
    average = sum/smooth_interval
    new_data[i+smooth_interval] = average
    sum = 0
  return new_data

def exponential_moving_avereage(data, smooth_interval = 2):

    if smooth_interval >= len(data):
      print("Smooth interval more or equal array lenght!")
      return
    
    alpha = 2.0/(smooth_interval+1)
    filtered_values = np.zeros(len(data))
    sum = 0

    for step in range(smooth_interval):
      sum += data[step]
    previous_ma_value = sum/smooth_interval

    for step in range(smooth_interval-1):
      previous_ma_value = alpha*data[step]+(1-alpha)*previous_ma_value
      filtered_values[step] = previous_ma_value

    sum = 0

    for step in range(smooth_interval):
      sum += data[step]
    previous_ma_value = sum/smooth_interval
    filtered_values[smooth_interval-1] = previous_ma_value

    for step in range(smooth_interval, len(data)):
      previous_ma_value = alpha*data[step]+(1-alpha)*previous_ma_value
      filtered_values[step] = previous_ma_value

    return filtered_values

def weighted_moving_average(data, smooth_interval=2):

    if(smooth_interval > len(data)):
      print("Smooth interval > lenght of data")
      return

    sum = 0
    j_sum = 0
    new_data = np.zeros(len(data))

    for i in range(smooth_interval):
      for j in range(smooth_interval):
        sum += data[i+j]*(j+1)
        j_sum += (j+1)
      average = (sum)/(j_sum)
      new_data[i] = average
      sum = 0
      j_sum = 0

    for i in range(len(data)-smooth_interval):
      for j in range(smooth_interval):
        sum += data[i+j]*(j+1)
        j_sum += (j+1)
      average = (sum)/(j_sum)
      new_data[i+smooth_interval] = average
      sum = 0
      j_sum = 0

    return new_data