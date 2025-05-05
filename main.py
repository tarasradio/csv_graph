import matplotlib.pyplot as plt
import sys
import csv

import filtering

time_ms = []
left = []
left_speed = []

right = []
right_speed = []

print(sys.argv)

filename = sys.argv[1]

start_points_x = []
start_points_y = []

with open(filename, 'r') as datafile:
  plotting = csv.reader(datafile, delimiter=';')
  
  x = 0

  left_last = 0
  right_last = 0
  ms_last = 0

  period_ms = 0

  first_string = True

  for encoder_data in plotting:

    data_string = encoder_data[0]
    angle_strings = data_string.split(',')

    ms = int(angle_strings[0])
    
    angle_l = float(angle_strings[1])
    angle_r = float(angle_strings[2])
    
    if(first_string == True):
      first_string = False

      left_last = angle_l
      right_last = angle_r

      ms_last = ms

      speed_l = 0
      speed_r = 0
    else:
      period_ms = 5

      speed_l = (angle_l - left_last) / (period_ms)
      speed_r = (angle_r - right_last) / (period_ms)

      # if speed_l > 0.05:
      #   start_points_x.append(x)
      #   start_points_y.append(angle_l)
      
      left_last = angle_l
      right_last = angle_r
      ms_last = ms
      
      time_ms.append(x)
      
      x += period_ms
      
      left.append(angle_l)
      right.append(angle_r)
      
      left_speed.append(speed_l)
      right_speed.append(speed_r)

filtered_speed = filtering.weighted_moving_average(left_speed, 30)

torque = []

for i in range(len(left_speed)):
  if filtered_speed[i] > 0.15:
    torque.append(5)
  elif filtered_speed[i] < -0.15:
    torque.append(-5)
  else:
    torque.append(0)
    #start_points_x.append(time_ms[i])
    #start_points_y.append(left[i])

fig, ax = plt.subplots(3, sharex=True)

# Добавляем главные grid-линии
ax[0].grid(True, which='major', linestyle='-', linewidth=0.5, color='gray')
ax[1].grid(True, which='major', linestyle='-', linewidth=0.5, color='gray')
ax[2].grid(True, which='major', linestyle='-', linewidth=0.5, color='gray')
# Добавляем второстепенные grid-линии
#ax[0].grid(True, which='minor', linestyle=':', linewidth=0.5, color='gray')
# Включаем второстепенные тики
#ax[0].minorticks_on()

ax[0].set_title("Угол")

#plt.fill_between(time_ms, left, color="tomato", alpha=0.5)
ax[0].plot(time_ms, left)
#plt.plot(start_points_x, start_points_y, 'ro')
#plt.plot(start_points_x, start_points_y)

ax[0].set_ylabel('angle')

ax[1].set_title("Момент")

ax[1].plot(time_ms, torque)

ax[1].set_ylabel('torque')

ax[2].set_title("Скорость")

ax[2].plot(time_ms, left_speed)
ax[2].plot(time_ms, filtered_speed)

ax[2].set_ylabel('speed')

ax[2].set_xlabel("Time, ms")

plt.show()