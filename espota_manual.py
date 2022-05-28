'''
  Examples:
  
  python /home/ha/ota/espota_manual.py -i 192.168.2.30 -f /home/ha/ota/alarm.bin
  python3 /home/ha/ota/espota_manual.py -i 192.168.2.35 -f /home/ha/ota/e_irrig.ino.generic.bin

  python.exe d:\Python\ihs\espota_manual.py -i 192.168.2.7 -f d:\Python\ihs\ota\my_6.2.1_watering.bin
  








  
'''
#!/usr/bin/env python
#
# Original espota.py by Ivan Grokhotkov:
# https://gist.github.com/igrr/d35ab8446922179dc58c
#
# Modified since 2015-09-18 from Pascal Gollor (https://github.com/pgollor)
# Modified since 2015-11-09 from Hristo Gochkov (https://github.com/me-no-dev)
# Modified since 2016-01-03 from Matthew O'Gorman (https://githumb.com/mogorman)
#
# This script will push an OTA update to the ESP
# use it like: python espota.py -i <ESP_IP_address> -I <Host_IP_address> -p <ESP_port> -P <Host_port> [-a password] -f <sketch.bin>
# Or to upload SPIFFS image:
# python espota.py -i <ESP_IP_address> -I <Host_IP_address> -p <ESP_port> -P <HOST_port> [-a password] -s -f <spiffs.bin>
#
# Changes
# 2015-09-18:
# - Add option parser.
# - Add log.
# - Send command to controller to differ between flashing and transmitting SPIFFS image.
#
# Changes
# 2015-11-09:
# - Added digest authentication
# - Enhanced error tracking and reporting
#
# Changes
# 2016-01-03:
# - Added more options to parser.
#

from __future__ import print_function
import socket
import sys
import os
import optparse
import hashlib
import random


import logging as log

# Commands
FLASH = 0
SPIFFS = 100
AUTH = 200
PROGRESS = False

myCallBackFc = None #
myClient = None #

'''
  
'''
def myCallBackFunction(msg):

  if myCallBackFc is not None:
    myCallBackFc(myClient, msg)

'''
  Accepts a float between 0 and 1. Any int will be converted to a float.
  A value under 0 represents a 'halt'.
  A value at 1 or bigger represents 100%
'''
def update_progress(progress):
  if(PROGRESS):
    barLength = 50 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
      progress = float(progress)
    if not isinstance(progress, float):
      progress = 0
      status = "error: progress var must be float\r\n"
    if progress < 0:
      progress = 0
      status = "Halt...\r\n"
    if progress >= 1:
      progress = 1
      status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rUploading:[{0}] {1}% {2}".format( "="*block + " "*(barLength-block), int(progress*100), status)

    if(int(progress*100) % 10 == 0):

      if myCallBackFc is not None:
        myCallBackFunction(text)
      else:
        sys.stderr.write(text)
        sys.stderr.flush()

  else:
    sys.stderr.write('.')
    sys.stderr.flush()

def serve(remoteAddr, localAddr, remotePort, localPort, password, filename, command = FLASH):

  # Create a TCP/IP socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_address = (localAddr, localPort)
  log.info('Starting on %s:%s', str(server_address[0]), str(server_address[1]))

  try:
    sock.bind(server_address)
    sock.listen(1)
  except:
    log.error("Listen Failed")
    return 1

  content_size = os.path.getsize(filename)
  f = open(filename,'rb')
  file_md5 = hashlib.md5(f.read()).hexdigest()
  f.close()
  log.info('Upload size: %d', content_size)
  message = '%d %d %d %s\n' % (command, localPort, content_size, file_md5)

  myCallBackFunction("Test msg ....")

  # Wait for a connection
  log.info('Sending invitation to: %s', remoteAddr)
  sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  remote_address = (remoteAddr, int(remotePort))
  sent = sock2.sendto(message.encode(), remote_address)
  sock2.settimeout(10)
  try:
    data = sock2.recv(128).decode()
  except:
    log.error('No Answer')
    myCallBackFunction('No Answer')

    sock2.close()
    return 1
  if (data != "OK"):
    if(data.startswith('AUTH')):
      nonce = data.split()[1]
      cnonce_text = '%s%u%s%s' % (filename, content_size, file_md5, remoteAddr)
      cnonce = hashlib.md5(cnonce_text.encode()).hexdigest()
      passmd5 = hashlib.md5(password.encode()).hexdigest()
      result_text = '%s:%s:%s' % (passmd5 ,nonce, cnonce)
      result = hashlib.md5(result_text.encode()).hexdigest()
      sys.stderr.write('Authenticating...')
      sys.stderr.flush()
      message = '%d %s %s\n' % (AUTH, cnonce, result)
      sock2.sendto(message.encode(), remote_address)
      sock2.settimeout(10)
      try:
        data = sock2.recv(32).decode()
      except:
        sys.stderr.write('FAIL\n')
        log.error('No Answer to our Authentication')
        sock2.close()
        return 1
      if (data != "OK"):
        sys.stderr.write('FAIL\n')
        log.error('%s', data)
        sock2.close()
        sys.exit(1);
        return 1
      sys.stderr.write('OK\n')
    else:
      log.error('Bad Answer: %s', data)
      sock2.close()
      return 1
  sock2.close()

  log.info('Waiting for device...')
  try:
    sock.settimeout(10)
    connection, client_address = sock.accept()
    sock.settimeout(None)
    connection.settimeout(None)
  except:
    log.error('No response from device')
    sock.close()
    return 1

  try:
    f = open(filename, "rb")
    if (PROGRESS):
      update_progress(0)
    else:
      sys.stderr.write('Uploading')
      sys.stderr.flush()

    offset = 0
    while True:

      chunk = f.read(1460)
      if not chunk: break
      offset += len(chunk)
      update_progress(offset/float(content_size))
      connection.settimeout(10)
      try:
        connection.sendall(chunk)
        res = connection.recv(4)
      except:
        sys.stderr.write('\n')
        log.error('Error Uploading')
        connection.close()
        f.close()
        sock.close()
        return 1

    sys.stderr.write('\n')
    log.info('Waiting for result...')
    # libraries/ArduinoOTA/ArduinoOTA.cpp L311 L320
    # only sends digits or 'OK'. We must not not close
    # the connection before receiving the 'O' of 'OK'
    try:
      connection.settimeout(60)
      while True:
        if connection.recv(32).decode().find('O') >= 0: break
      log.info('Result: OK')
      connection.close()
      f.close()
      sock.close()
      if (data != "OK"):
        sys.stderr.write('\n')
        log.error('%s', data)
        return 1;
      return 0
    except:
      log.error('No Result!')
      connection.close()
      f.close()
      sock.close()
      return 1

  finally:
    connection.close()
    f.close()

  sock.close()
  return 1
# end serve


def parser(unparsed_args):

  parser = optparse.OptionParser(
    usage = "%prog [options]",
    description = "Transmit image over the air to the esp8266 module with OTA support."
  )

  # destination ip and port
  group = optparse.OptionGroup(parser, "Destination")
  group.add_option("-i", "--ip",
    dest = "esp_ip",
    action = "store",
    help = "ESP8266 IP Address.",
    default = False
  )
  group.add_option("-I", "--host_ip",
    dest = "host_ip",
    action = "store",
    help = "Host IP Address.",
    default = "0.0.0.0"
  )
  group.add_option("-p", "--port",
    dest = "esp_port",
    type = "int",
    help = "ESP8266 ota Port. Default 8266",
    default = 8266
  )
  group.add_option("-P", "--host_port",
    dest = "host_port",
    type = "int",
    help = "Host server ota Port. Default random 10000-60000",
    default = random.randint(10000,60000)
  )
  parser.add_option_group(group)

  # auth
  group = optparse.OptionGroup(parser, "Authentication")
  group.add_option("-a", "--auth",
    dest = "auth",
    help = "Set authentication password.",
    action = "store",
    default = ""
  )
  parser.add_option_group(group)

  # image
  group = optparse.OptionGroup(parser, "Image")
  group.add_option("-f", "--file",
    dest = "image",
    help = "Image file.",
    metavar="FILE",
    default = None
  )
  group.add_option("-s", "--spiffs",
    dest = "spiffs",
    action = "store_true",
    help = "Use this option to transmit a SPIFFS image and do not flash the module.",
    default = False
  )
  parser.add_option_group(group)

  # output group
  group = optparse.OptionGroup(parser, "Output")
  group.add_option("-d", "--debug",
    dest = "debug",
    help = "Show debug output. And override loglevel with debug.",
    action = "store_true",
    default = False
  )
  group.add_option("-r", "--progress",
    dest = "progress",
    help = "Show progress output. Does not work for ArduinoIDE",
    action = "store_true",
    default = True
  )
  parser.add_option_group(group)

  (options, args) = parser.parse_args(unparsed_args)

  return options
# end parser


def main(args):

  options = parser(args)
  log.debug("Options: %s", str(options))

  # check options
  global PROGRESS
  PROGRESS = options.progress
  if (not options.esp_ip or not options.image):
    log.critical("Not enough arguments.")
    return 1

  command = FLASH
  if(options.spiffs):
    command = SPIFFS

  serve(options.esp_ip, options.host_ip, options.esp_port, options.host_port, options.auth, options.image, command)
# end main

'''

  Must enabled the firewall to run this program !!!
  
  
  This script will push an OTA update to the ESP
  use it like: python espota.py -i <ESP_IP_address> -I <Host_IP_address> -p <ESP_port> -P <Host_port> [-a password] -f <sketch.bin>
  python.exe C:\\Users\\admin\\Documents\\ArduinoData\\packages\\esp8266\\hardware\\esp8266\\2.4.1/tools/espota.py -i 192.168.2.6 -p 8266 --auth= -f C:\\Users\\admin\\AppData\\Local\\Temp\\arduino_build_494594/ParadoxAlarmSystemOTA.ino.bin
  "c:\Program Files\Python36\python.exe" d:\Python\ihs\espota.py
  
  
  
  kwargs = {}
  kwargs['ESP_IP_address'] = "192.168.2.7"
  kwargs['sketch'] = "D:\\Python\\ihs\\ota\\3.bin"
  
  startOTA(**kwargs)

  
'''
def startOTA(ESP_IP_address, sketch, ESP_port = 8266, pw = "", callBackFc = None, client = None):

  argv = []
  argv.append("This_program_path")
  argv.append("-i")         # ESP_IP_address
  argv.append(ESP_IP_address)
  #argv.append("-p")        # ESP_port
  #argv.append(ESP_port)
  #argv.append("-I")        # host_ip
  #argv.append("")
  #argv.append("-P")        # host_port
  #argv.append("")
  argv.append("-a")        # auth
  argv.append(pw)
  argv.append("-f")         # sketch
  argv.append(sketch)
  argv.append("-r")         # Show progress
  argv.append("true")
  #argv.append("-s")        # "Use this option to transmit a SPIFFS image and do not flash the module.",
  #argv.append(sketch)

  global myCallBackFc, myClient
  myCallBackFc = callBackFc
  myClient = client


  #log.info('--> start [' + str(argv) + ']')
  main(argv)


'''
  Examples:
  
  sudo python /home/pi/ota/espota_manual.py -i 192.168.2.30 -f /home/pi/ota/alarm.bin
  sudo python /home/ha/ota/espota_manual.py -i 192.168.2.30 -f /home/ha/ota/alarm.bin
  

  python.exe d:\Python\ihs\espota_manual.py -i 192.168.2.7 -f d:\Python\ihs\ota\my_6.2.1_watering.bin
  

  
'''
if __name__ == '__main__':

  sys.exit(main(sys.argv))
