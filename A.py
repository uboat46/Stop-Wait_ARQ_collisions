import serial, time, random, struct


def numTobyte(num):
  res = ''
  for digit in num:
    res += digit
  return res

s = serial.Serial('/dev/ttys001')
s.is_open
seq = 0
for n in range(1000):
  waiting_time = random.randrange(1, 5)
  time.sleep(waiting_time /1000*50)
  strToWrite = 'TA:' + numTobyte(str(seq)) + '\n'
  s.write(strToWrite.encode())
  seq += 1
  print(seq)
s.close()
