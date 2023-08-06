"""Amplitude subsystem"""
from rsfsup.common import Subsystem, validate


class Amplitude(Subsystem, kind="AMPT"):
    """Amplitude subsystem

    Attributes:
        instr (Fsup)
    """

    # def __init__(self, instr):
    #     super().__init__(instr)
    #     # For now, set the input attenuation to automatic to track the REF LEVEL.
    #     # This will automatically adjust the attenuation to keep the maximum signal
    #     # level (REF LEVEL) at the mixer to the default level of -25 dBm.
    #     self._visa.write("INPUT:ATTENUATION:AUTO ON")
    #     self._visa.write("INPUT:MIXER:AUTO ON")

    @property
    def coupling(self):
        """value (str): RF input coupling {AC, DC}"""
        return self._visa.query("INPUT:COUPLING?")

    @coupling.setter
    @validate
    def coupling(self, value):
        self._visa.write(f"INPUT:COUPLING {value}")

    @property
    def ref_level(self):
        """value (int or str): reference level as integer in unit dBm or 'x dBm'"""
        return self._visa.query(f"DISPLAY:WINDOW{self._screen()}:TRACE:Y:RLEVEL?")

    @ref_level.setter
    @validate
    def ref_level(self, value):
        self._visa.write(f"DISP:WIND{self._screen()}:TRAC:Y:RLEV {value}")

    @property
    def attenuation(self):
        """value (str): attenuation in dB or 'AUTO'"""
        value = self._visa.query(f"INPUT{self._screen()}:ATTENUATION?")
        return f"{value} dB"

    @attenuation.setter
    @validate
    def attenuation(self, value):
        if value == "AUTO":
            timeout = self._visa.timeout
            self._visa.timeout = 5000  # ms
            self._visa.write(f"INPUT{self._screen()}:ATTENUATION:AUTO ON")
            self._visa.timeout = timeout
        else:
            self._visa.write(f"INPUT{self._screen()}:ATTENUATION {value}")

    @property
    def mixer_power(self):
        """value (str): mixer power level in dBm or 'AUTO'"""
        value = self._visa.query(f"INPUT{self._screen()}:MIXER:POWER?")
        return f"{value} dBm"

    @mixer_power.setter
    @validate
    def mixer_power(self, value):
        if value == "AUTO":
            timeout = self._visa.timeout
            self._visa.timeout = 5000  # ms
            self._visa.write(f"INPUT{self._screen()}:MIXER:AUTO ON")
            self._visa.timeout = timeout
        else:
            self._visa.write(f"INPUT{self._screen()}:MIXER {value}")
