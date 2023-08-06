
APP_NAME = 'avrcp-volume'

import asyncio

from .installer import Installer
from .avrcp_controller import AvrcpController

def main():
	import argparse

	parser = argparse.ArgumentParser(
		prog = APP_NAME,
	)
	parser.add_argument(
		'--install-service',
		dest = 'install',
		action = Installer,
		nargs = 0,
		default = False,
		required = False,
		help = 'install systemd user service',
	)
	parser.parse_args()

	avrcp = AvrcpController()
	asyncio.run(avrcp.start())

if (__name__ == '__main__'):
	main()
