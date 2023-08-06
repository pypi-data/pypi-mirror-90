
import asyncio
import signal
import math

from . import APP_NAME
from .logger import logger

from dbus_next import (
	Variant
)
from dbus_next.constants import (
	BusType
)
import desktop_notify

from .message_bus import MessageBus

class AvrcpController():

	NAME = 'org.bluez'
	PATH = '/'

	OBJECT_MANAGER = 'org.freedesktop.DBus.ObjectManager'
	TRANSPORT = 'org.bluez.MediaTransport1'
	PROPERTIES = 'org.freedesktop.DBus.Properties'

	VOLUME_MAX = 127

	NOTIFY_ICON = 'audio-headphones'
	NOTIFY_TIMEOUT = 2000

	def __init__(self):
		self.loop = None
		self.future = None

		self.bus = None
		self.bluez = None

		self.transports = {}

		server = desktop_notify.aio.Server(APP_NAME)
		self.notify = server.Notify()
		self.notify.set_icon(self.NOTIFY_ICON)
		self.notify.set_timeout(self.NOTIFY_TIMEOUT)
		self.notify.set_on_show(lambda n: (self.free_notify()))
		self.free_notify()

		from .pulse import PaController
		self.pa_controller = PaController(self)

	def free_notify(self):
		self.notify_blocked = False

	async def start(self):
		self.bus = await MessageBus(
			bus_type = BusType.SYSTEM
		)\
			.connect()

		self.bluez = await self.bus.get_proxy_object(
			self.NAME,
			self.PATH
		)
		self.object_manager = self.bluez.get_interface(
			self.OBJECT_MANAGER
		)

		self.loop = asyncio.get_running_loop()
		self.loop.create_task(self.pa_event_loop())
		self.future = self.loop.create_future()

		for signame in {'SIGINT', 'SIGTERM'}:
			self.loop.add_signal_handler(
				getattr(signal, signame),
				self.stop
			)

		await self.init_transports()
		await self.future

	async def pa_event_loop(self):
		await self.loop.run_in_executor(
			None,
			self.pa_controller.get_event_loop()
		)

	async def init_transports(self):
		self.object_manager.on_interfaces_added(
			self.interfaces_added
		)
		self.object_manager.on_interfaces_removed(
			self.interfaces_removed
		)

		objects = await self.object_manager\
			.call_get_managed_objects()

		for path, interfaces in objects.items():
			await self.listen_transport(path, interfaces)

	def interfaces_added(self, path, interfaces):
		self.loop.create_task(
			self.listen_transport(path, interfaces)
		)

	def interfaces_removed(self, path, interfaces):
		if (
			self.TRANSPORT in interfaces
			and path in self.transports
		):
			del self.transports[path]
			logger.info('- ' + path)

	async def listen_transport(self, path, interfaces):
		if (self.TRANSPORT in interfaces):
			transport_obj = await self.bus.get_proxy_object(
				self.NAME,
				path
			)
			transport = transport_obj.get_interface(
				self.TRANSPORT
			)
			self.transports[path] = transport

			properties = transport_obj.get_interface(
				self.PROPERTIES
			)
			properties.on_properties_changed(
				lambda interface, props, invalidated_properties:
					self.properties_changed(
						path,
						interface,
						props,
						invalidated_properties
					)
			)

			logger.info('+ ' + path)

	def properties_changed(self, path, interface_name, changed_properties, invalidated_properties):
		if (
			interface_name == self.TRANSPORT
			and 'Volume' in changed_properties
		):
			self.handle_volume_change(
				path,
				changed_properties['Volume'].value
			)

	def handle_volume_change(self, path, volume):
		logger.debug(path + ': ' + str(volume))

		self.loop.create_task(
			asyncio.wait([
				self.show_notify(volume),
				self.preserve_increase_signal(path, volume),
				self.increase_volume_pa(volume),
			])
		)

	async def show_notify(self, value):
		self.notify.set_hint(
			'value',
			Variant(
				'i',
				math.ceil(
					value / self.VOLUME_MAX * 100
				)
			)
		)
		if (
			not self.notify_blocked
			or self.notify.visible
		):
			self.notify_blocked = True
			await self.notify.show()

	async def preserve_increase_signal(self, path, volume):
		if (
			volume == self.get_volume_max()
			and path in self.transports
		):
			await self.transports[path].set_volume(
				self.get_volume_max_safe()
			)

	async def increase_volume_pa(self, volume):
		if (volume == self.VOLUME_MAX):
			self.pa_controller.increase_volume()

	def increase_volume_sync(self):
		asyncio.run_coroutine_threadsafe(
			self.increase_volume(),
			self.loop
		)

	async def increase_volume(self):
		for transport in self.transports.values():
			value = await transport.get_volume()
			v_delta = self.pa_controller.VOLUME_DELTA
			v_max = self.get_volume_max()

			new_value = min(
				math.ceil(value + v_delta * v_max),
				self.get_volume_max_safe()
			)

			self.loop.create_task(
				asyncio.wait([
					self.show_notify(new_value),
					transport.set_volume(new_value),
				])
			)

	def get_volume_max(self):
		return self.VOLUME_MAX

	def get_volume_max_safe(self):
		return self.get_volume_max() - 1

	def stop(self, signal_num = 2, frame = None):
		self.pa_controller.stop_event_loop()
		self.future.set_result(True)
