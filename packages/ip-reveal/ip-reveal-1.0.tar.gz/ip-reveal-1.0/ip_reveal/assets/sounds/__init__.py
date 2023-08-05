from ip_reveal.assets.sounds import alerts
import simpleaudio as sa


class Alerts(object):
    def __init__(self):
        """
        Initialize an "Alerts" class that contains sounds for alerts.
        """
        self.asset_fp = alerts.ALERT_AUDIO_FP
        self.o_pulse_fp = alerts.O_PULSE_FP
        self.o_pulse_alert = sa.WaveObject.from_wave_file(self.o_pulse_fp)

    def play(self):
        self.o_pulse_alert.play()
