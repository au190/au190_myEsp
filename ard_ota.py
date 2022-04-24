'''************************************************
by au190 - Kallos Robert 2021.02.06

	ESP8266 serial Gateway - Wifi serial Gateway
	STK500 Aruino protocol
	version of python3.7

	Examples:

	python.exe ard_ota.py -i 192.168.2.39 -f d:\Python\ard_ota\1.hex

  sudo python3 /home/ha/ota/ard_ota/ard_ota.py -i 192.168.2.35 -f /home/ha/ota/ard_ota/a_irrig_v1.hex

  
  
  
pip3 install websockets
pip3 install IntelHex

************************************************'''
import time
import asyncio
import websockets
import sys
import optparse
import random
from datetime import datetime
from intelhex import IntelHex
from arduinobootloader import ArduinoBootloader
from intelhex import AddressOverlapError




'''
  Accepts a float between 0 and 1. Any int will be converted to a float.
  A value under 0 represents a 'halt'.
  A value at 1 or bigger represents 100%
'''
async def my_progress(progress):
	barLength = 50  # Modify this to change the length of the progress bar
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
	block 	= int(round(barLength*progress))
	text 	= "\rUploading:[{0}] {1}% {2}".format( "="*block + " "*(barLength-block), int(progress*100), status)

	if(int(progress*100) % 10 == 0):
		sys.stderr.write(text)
		sys.stderr.flush()

async def test_progress():
	await log("--> Test Progress bar .....")
	#time.sleep(0.005)
	await my_progress(0)
	for i in range(0, 101):
		time.sleep(0.005)
		await my_progress(i / float(100))
	#time.sleep(0.005)
	await log("<-- Test Progress bar .....")

async def log(msg):
	if len(msg) > 1:
		print((datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]) + " " + msg)
	else:
		print("")

async def exit_by_error(ab, prg, websocket, msg):
	print('')
	await log("### " + msg)
	await prg.leave_bootloader()
	await ab.close()
	await websocket.send('{"ard_ota": "0"}')
	await websocket.close(1000, "Ok")
	sys.exit(0)

async def uploadOTA(options, uri):
	#try:
		async with websockets.connect(uri) as websocket:

			await log("")
			ih = IntelHex()
			ab = ArduinoBootloader(websocket)
			protocol = "Stk500v1"

			await log("Set ESP to Arduino OTA mode")
			await websocket.send('cmnd/ws/ard_ota {"ard_ota":"1"}')  # Go to ard_ota mode
			await log("Set Stk500 protocol: " + protocol)

			'''
				Check the firmware file
			'''
			try:
				ih.fromfile(options.image, format='hex')
			except FileNotFoundError:
				await exit_by_error(ab, None, websocket, "Error File not found")
			except AddressOverlapError:
				await exit_by_error(ab, None, websocket, "Error File with address overlapped")

			max_address = ih.maxaddr()
			await log("Flash size: {} bytes".format(max_address))

			'''
				
			'''
			prg = await ab.select_programmer(protocol, websocket)

			if await prg.open():
				await log("*** Ok open")
			else:
				await log("### Err open")


			if await prg.board_request():
				await log("*** Bootloader: {} version: {} hardware version: {}".format(ab.programmer_name, ab.sw_version, ab.hw_version))
			else:
				await log("### Err Board_request")


			if await prg.cpu_signature():
				await log("*** Cpu name: {}".format(ab.cpu_name))
			else:
				await log("### Err cpu_signature")


			''''''
			"""Iterate the firmware file into chunks of the page size in bytes, and use the write flash command to update the cpu."""
			await log("Writing flash: {} bytes".format(max_address))
			await my_progress(0)
			for address in range(0, max_address, ab.cpu_page_size):
				buffer = ih.tobinarray(start=address, size=ab.cpu_page_size)
				if not await prg.write_memory(buffer, address):
					await exit_by_error(ab, prg, websocket, "Error Writing flash memory")
				await my_progress(address / float(max_address))
			await my_progress(1)#Done


			'''

			"""If the write was successful, re-iterate the firmware file, and use the read flash command to update and compare them."""
			await log("Reading flash: {} bytes".format(max_address))
			await my_progress(0)
			for address in range(0, ih.maxaddr(), ab.cpu_page_size):#
				read_buffer = await prg.read_memory(address, ab.cpu_page_size)
				#await log("> " + str(address) + " - " + str(ab.cpu_page_size) + " - " + str(read_buffer))
				#time.sleep(0.05)
				if read_buffer is None:
					await exit_by_error(ab, prg, websocket, "Error Reading flash memory")

				#if read_buffer != ih.tobinarray(start=address, size=ab.cpu_page_size):
					#await exit_by_error(ab, prg, websocket, "Error File not match")
				await my_progress(address / float(max_address))
			await my_progress(1)  # Done
			await log("Flash done: {} bytes".format(my_progress))

			'''


			await prg.leave_bootloader()
			await ab.close()

			await websocket.send('cmnd/ws/ard_ota {"ard_ota":"0"}')  # Go to normal mode
			await websocket.close(1000, "Ok")


def parser(unparsed_args):

	parser = optparse.OptionParser(
	usage = "%prog [options]",
	description = "Transmit image over the air to the esp8266 module with OTA support."
	)

	# destination ip and port
	group = optparse.OptionGroup(parser, "Destination")

	group.add_option("-i", "--ip",
	dest = "ip",
	action = "store",
	help = "IP Address.",
	default = False
	)

	group.add_option("-p", "--port",
	dest = "port",
	type = "int",
	help = "Websocket ota Port. Default 81",
	default = 81
	)

	# image
	group = optparse.OptionGroup(parser, "Image")
	group.add_option("-f", "--file",
	dest = "image",
	help = "Image file.",
	metavar="FILE",
	default = None
	)

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

'''************************************************

    main

************************************************'''
def main(args):

	print("")
	options = parser(args)
	#print("--> main: Options: %s", str(options))

	# check options
	global PROGRESS
	PROGRESS = options.progress
	if (not options.ip or not options.image):
		print("--> main: Options: %s", str(options))
		print("Not enough arguments.")
		return 1

	ws_conn = "ws://" + options.ip + ":" + str(options.port) + "/uc"
	print("--> main: " + str(ws_conn))

	tasks = [
		uploadOTA(options, ws_conn),
	]

	asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
	#asyncio.get_event_loop().run_until_complete(set_normal_mode(ws_conn))

	print("")
	print("<-- main")


'''
	Examples:

	sudo python /home/ha/ota/espota_manual.py -i 192.168.2.30 -f /home/ha/ota/alarm.bin
	python.exe d:\Python\ihs\espota_manual.py -i 192.168.2.7 -f d:\Python\ihs\ota\my_6.2.1_watering.bin

'''
if __name__ == '__main__':
	sys.exit(main(sys.argv))