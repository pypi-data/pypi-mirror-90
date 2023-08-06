
import pulsectl

from avrcp_volume import APP_NAME
from avrcp_volume import AvrcpController
from avrcp_volume.logger import logger

from .sink import Sink

from pprint import pprint

class PaController():

	VOLUME_DELTA = 0.05
	VOLUME_MAX = 1
	VOLUME_MAX_SAFE = 0.99

	def __init__(self, avrcp: AvrcpController):
		self._avrcp = avrcp

		self._pulse_ctl  = pulsectl.Pulse(APP_NAME + '-ctl')

		self._pulse_loop = pulsectl.Pulse(APP_NAME + '-loop')
		self._pulse_loop.event_mask_set('all')
		self._pulse_loop.event_callback_set(self._handle)

		self._last_volume = self._get_sink().get_volume()

	def get_event_loop(self):
		return self._pulse_loop.event_listen

	def stop_event_loop(self):
		self._pulse_loop.event_listen_stop()

	def increase_volume(self):
		sink = self._get_sink()

		sink.set_volume(
			min(
				sink.get_volume() + self.VOLUME_DELTA,
				self.VOLUME_MAX
			)
		)

	def _get_sink(self):
		return Sink(self._pulse_ctl)

	def _handle(self, e):
		sink = self._get_sink()

		if (
			e.facility == pulsectl.PulseEventFacilityEnum.sink
			and e.t == pulsectl.PulseEventTypeEnum.change
			and e.index == sink.index
		):
			self._handle_volume_change(sink)

	def _handle_volume_change(self, sink):
		volume = sink.get_volume()
		logger.debug(sink.name + ': ' + str(volume))

		if (
			self._last_volume == self.VOLUME_MAX_SAFE
			and volume == self.VOLUME_MAX
		):
			self._avrcp.increase_volume_sync()

		if (volume == self.VOLUME_MAX):
			volume = self.VOLUME_MAX_SAFE

		if (
			self._last_volume == self.VOLUME_MAX_SAFE
			and volume < self._last_volume
		):
			volume += self.VOLUME_MAX - self.VOLUME_MAX_SAFE

		self._last_volume = volume
		sink.set_volume(volume)
