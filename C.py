import serial, struct, signal

seq = 0
collision_number = 0
seq_correct = True
seq_last_byte = ''
seq_last_byte_num = ''
decodedByte = ''

def setGoodDataFrame():
  global seq
  global seq_last_byte
  global seq_last_byte_num
  if (seq_last_byte == 'TA:' and seq_last_byte_num.isdecimal()):
    seq += 1
    print(seq_last_byte + seq_last_byte_num + ': ' + str(seq))
    seq_last_byte = ''
    seq_last_byte_num = ''

def checkSeqNumber():
  global decodedByte
  global seq_last_byte_num
  if (seq_correct and seq_last_byte == 'TA:'):
    if decodedByte.isdigit():
      seq_last_byte_num += decodedByte

def setSeqLastByte():
  global decodedByte
  global collision_number
  global seq_correct
  global seq_last_byte
  global seq_last_byte_num
  if decodedByte == 'T':
    seq_last_byte = ''
    seq_correct = True
  if decodedByte == 'A':
    if seq_last_byte != 'T':
      seq_correct = False
  if decodedByte == ':':
    if seq_last_byte != 'TA':
      seq_correct = False
  if seq_correct:
    seq_last_byte += decodedByte
  else:
    collision_number += 1
    seq_last_byte = ''
    seq_last_byte_num = ''
    print('collisions =' + str(collision_number))

def switch():
  global decodedByte
  sw = {
    'T': setSeqLastByte,
    'A': setSeqLastByte,
    ':': setSeqLastByte,
    '\n': setGoodDataFrame,
  }
  sw.get(decodedByte, checkSeqNumber)()

def decodeByte(byte):
  global decodedByte
  decodedByte = byte.decode()
  switch()
    

s = serial.Serial('/dev/ttys002')
s.is_open

def handle_exit():
  s.close()  

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

while True:
  decodeByte(s.read(1))
