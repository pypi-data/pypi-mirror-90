"""Bandwidth subsystem"""
from rsfsup.common import Subsystem, scale_frequency, validate


class Bandwidth(Subsystem, kind="BW"):
    """Bandwidth subsystem

    Attributes:
        instr (Fsup)
    """

    # def __init__(self, instr):
    #     super().__init__(instr)
    #     # For now, adjust resolution and video bandwidths automatically according to
    #     # the span.
    #     self._visa.write("BANDWIDTH:RESOLUTION:AUTO ON")
    #     self._visa.write("BANDWIDTH:RESOLUTION:TYPE NORMAL")
    #     self._visa.write("BANDWIDTH:VIDEO:AUTO ON")

    @property
    def resolution_bandwidth(self):
        """Resolution bandwidth

        Parameters
        ----------
        value : str {AUTO, 10 Hz to 50 MHz}
            When set to AUTO, RBW is based on the RBW/SPAN ratio.
        """
        value = self._visa.query(f"SENSE{self._screen()}:BANDWIDTH:RESOLUTION?")
        return scale_frequency(float(value))

    @resolution_bandwidth.setter
    @validate
    def resolution_bandwidth(self, value):
        if value == "AUTO":
            self._visa.write(f"SENSE{self._screen()}:BAND:RES:AUTO ON")
        else:
            self._visa.write(f"SENSE{self._screen()}:BAND:RES:AUTO OFF")
            self._visa.write(f"SENSE{self._screen()}:BAND:RES {value}")

    @property
    def filter_type(self):
        """value : str {NORM, CFIL, FFT, RRC, P5, P5D}"""
        return self._visa.query(f"SENSE{self._screen()}:BANDWIDTH:RESOLUTION:TYPE?")

    @filter_type.setter
    @validate
    def filter_type(self, value):
        self._visa.write(f"SENSE{self._screen()}:BANDWIDTH:RESOLUTION:TYPE {value}")

    @property
    def video_bandwidth(self):
        """Video bandwidth

        Parameters
        ----------
        value : str {AUTO, 1 Hz to 10 MHz
            When set to AUTO, video bandwidth is based on the VideoBandwidth/RBW ratio.
        """
        value = self._visa.query(f"SENSE{self._screen()}:BANDWIDTH:VIDEO?")
        return scale_frequency(float(value))

    @video_bandwidth.setter
    @validate
    def video_bandwidth(self, value):
        if value == "AUTO":
            self._visa.write(f"SENSE{self._screen()}:BAND:VID:AUTO ON")
        else:
            self._visa.write(f"SENSE{self._screen()}:BAND:VID:AUTO OFF")
            self._visa.write(f"SENSE{self._screen()}:BAND:VID {value}")
