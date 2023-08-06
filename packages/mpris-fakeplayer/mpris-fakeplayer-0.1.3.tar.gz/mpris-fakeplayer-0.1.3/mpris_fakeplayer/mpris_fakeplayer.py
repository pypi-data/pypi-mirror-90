
import asyncio
import signal

from dbus_next.aio import MessageBus

from .media_player2_interface import MediaPlayer2Interface
from .media_player2_player_interface import MediaPlayer2PlayerInterface

class MprisFakePlayer():

	NAME = 'org.mpris.MediaPlayer2.FakePlayer'
	PATH = '/org/mpris/MediaPlayer2'

	def __init__(self):
		self.loop = None
		self.future = None

		self.bus = None
		self.player2 = MediaPlayer2Interface()
		self.player2_player = MediaPlayer2PlayerInterface()

	async def play(self):
		self.bus = await MessageBus().connect()

		self.bus.export(self.PATH, self.player2)
		self.bus.export(self.PATH, self.player2_player)

		await self.bus.request_name(self.NAME)

		self.loop = asyncio.get_running_loop()

		for signame in {'SIGINT', 'SIGTERM'}:
			self.loop.add_signal_handler(
				getattr(signal, signame),
				self.stop
			)

		self.future = self.loop.create_future()
		await self.future

		self.player2_player.Stop()
		await self.bus.release_name(self.NAME)

	def stop(self, signal_num = 2, frame = None):
		self.future.set_result(True)
