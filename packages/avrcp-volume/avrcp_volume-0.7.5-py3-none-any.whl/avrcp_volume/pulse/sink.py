
import pulsectl

class Sink(pulsectl.PulseSinkInfo):

	def __init__(self, pulse: pulsectl.Pulse):
		self._pulse = pulse
		self._sink = self._pulse.get_sink_by_name(
			self._pulse.server_info().default_sink_name
		)

	def __getattr__(self, name):
		return getattr(self._sink, name)

	def set_volume(self, value):
		volume = self._sink.volume
		volume.value_flat = value

		self._pulse.volume_set(self._sink, volume)

	def get_volume(self):
		return round(self._sink.volume.value_flat, 2)
