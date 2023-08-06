
APP_NAME = 'mpris-fakeplayer'

import asyncio

from .installer import Installer
from .mpris_fakeplayer import MprisFakePlayer

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

	fake_player = MprisFakePlayer()
	asyncio.run(fake_player.play())
