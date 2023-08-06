import logging
import time
import threading
import atexit
import math
from typing import Union, Tuple
from ftdi_serial import Serial
from ismatec.errors import PumpError, CommandError


class RegloICC:
    """
    This module is for the pump software version 3.0.
    The pump: http://www.ismatec.com/images/pdf/manuals/14-036_E_ISMATEC_REGLO_ICC_ENGLISH_REV.%20C.pdf


    """
    _CONNECTION_SETTINGS = {'baudrate': 9600, 'data_bits': Serial.DATA_BITS_8, 'stop_bits': Serial.STOP_BITS_1}
    # hex command characters for data transmission
    _CR_HEX = "\x0D"  # carriage return
    _LF_HEX = "\x0A"  # line feed
    _SP_HEX = "\x20"  # space
    _VB_HEX = "\x7c"  # vertical bar

    # data type formats
    _FALSE = 0
    _TRUE = 1
    _CLOCKWISE = "J"
    _COUNTER_CLOCKWISE = 'K'

    # request message terminators
    _COMMAND_LINE_ENDING = _CR_HEX + _LF_HEX  # each individual command is terminated with CRLF
    _SET_PUMP_ADDRESS_LINE_ENDING = _CR_HEX  # unique line ending for setting the pump address

    # response messages
    # data response
    _DATA_RESPONSE_LINE_ENDING = _CR_HEX + _LF_HEX
    _MULTI_DIGIT_RESPONSE_LINE_ENDING_ENCODED = _DATA_RESPONSE_LINE_ENDING.encode()
    # status responses
    _SR_SUCCESS = '*'
    _SR_FAIL = "#"
    _SR_POSITIVE = "+"
    _SR_NEGATIVE = "-"

    # constants for commands
    _SET_ADDRESS = "@"
    # ------------------------------------
    # commands - communications management
    _CHANNEL_ADDRESS_ENABLED = "~"
    _EVENT_MESSAGES_ENABLED = "xE"
    _SERIAL_PROTOCOL_VERSION = "x!"
    # ------------------------------------
    # commands - pump drive
    _START = 'H'
    _STOP = 'I'
    _PAUSE = "xI"  # STOP in RPM or flow rate mode
    _GET_PUMP_DIRECTION = "xD"
    _SET_ROTATION_CLOCKWISE = 'J'
    _SET_ROTATION_COUNTER_CLOCKWISE = 'K'
    _GET_CAUSE_OF_RUN_ERROR = "xe"
    # ------------------------------------
    # commands - operational modes and settings
    _GET_CURRENT_MODE = "xM"
    _MODE_RPM = 'L'
    _MODE_FLOW_RATE = 'M'
    _MODE_VOLUME_AT_RATE = 'O'
    _MODE_VOLUME_OVER_TIME = 'G'
    _MODE_VOLUME_AND_PAUSE = 'Q'
    _MODE_TIME = 'N'
    _MODE_TIME_AND_PAUSE = 'P'
    _GET_FLOW_RATE = "xF"  # when mode is not RPM or flow rate mode
    _SET_FLOW_RATE = "xF"  # not in RPM or flow rate mode
    _GET_RPM_SPEED = "S"  # in RMP
    _SET_RPM_SPEED = 'S'  # RPM mode flow rate setting (0.01 RPM)
    _GET_FLOW_RATE_VOLUME_TIME_MODE = 'f'
    _SET_FLOW_RATE_VOLUME_TIME_MODE = 'f'
    _GET_VOLUME = 'v'
    _SET_VOLUME = 'v'
    _GET_PUMP_RUN_TIME = 'xT'
    _SET_PUMP_RUN_TIME = 'xT'
    _GET_PUMP_PAUSE_TIME = 'xP'
    _SET_PUMP_PAUSE_TIME = 'xP'
    _GET_PUMP_CYCLE_COUNT = '"'
    _SET_PUMP_CYCLE_COUNT = '"'
    _GET_MAX_FLOW_RATE = "?"
    _GET_MAX_FLOW_RATE_USING_CALIBRATION = "!"
    _GET_TIME_TO_DISPENSE_VOLUME_AT_FLOW_RATE = 'xv'
    _GET_TIME_TO_DISPENSE_VOLUME_AT_RPM = 'xw'
    # ------------------------------------
    # commands - configuration
    _GET_TUBING_INNER_DIAMETER = '+'
    _SET_TUBING_INNER_DIAMETER = '+'
    _GET_BACKSTEPS_SETTING = '%'
    _SET_BACKSTEPS_SETTING = '%'
    _RESET_CONFIGURABLE_DATA_TO_DEFAULT = '0'
    # ------------------------------------
    # commands - calibration
    _GET_CALIBRATION_DIRECTION = 'xR'
    _SET_CALIBRATION_DIRECTION = 'xR'
    _GET_CALIBRATION_TARGET_VOLUME_TO_PUMP = 'xU'
    _SET_CALIBRATION_TARGET_VOLUME_TO_PUMP = 'xU'
    _GET_CALIBRATION_ACTUAL_VOLUME_MEASURE = 'xV'
    _SET_CALIBRATION_ACTUAL_VOLUME_MEASURE = 'xV'
    _GET_CALIBRATION_TIME = 'xW'
    _SET_CALIBRATION_TIME = 'xW'
    _GET_CHANNEL_RUN_TIME_SINCE_LAST_CALIBRATION = 'xX'
    _START_CALIBRATION = 'xY'
    _CANCEL_CALIBRATION = 'xZ'
    # ------------------------------------
    # commands - system
    _GET_PUMP_FIRMWARE_VERSION = '('
    _SET_FACTORY_ROLLER_STEP_VOLUME = 'xt'
    _SAVE_SET_ROLLER_STEP_SETTINGS = 'xs'
    _RESET_ROLLER_STEP_VOLUME_TO_DEFAULTS = 'xu'
    _SET_PUMP_NAME = 'xN'
    _GET_PUMP_SERIAL_NUMBER = 'xS'
    _SET_PUMP_SERIAL_NUMBER = 'xS'
    _GET_PUMP_LANGUAGE = 'xL'
    _SET_PUMP_LANGUAGE = 'xL'
    _GET_N_PUMP_CHANNELS = 'xA'
    _SET_N_PUMP_CHANNELS = 'xA'
    _GET_N_ROLLERS_FOR_CHANNEL = 'xB'
    _SET_N_ROLLERS_FOR_CHANNEL = 'xB'
    _GET_N_REVOLUTIONS_SINCE_RESET = 'xC'
    _GET_CHANNEL_TOTAL_VOLUME_PUMPED_SINCE_RESET = 'xG'
    _GET_TOTAL_TIME_PUMPED_SINCE_RESET = 'xJ'
    _SET_CONTROL_FROM_PUMP_UI = 'A'
    _DISABLE_CONTROL_FROM_PUMP_UI = 'B'
    _WRITE_NUMBERS_TO_PUMP_DISPLAY = 'D'
    _WRITE_LETTERS_TO_PUMP_DISPLAY = 'DA'
    _CHECK_PUMP_RUNNING = 'E'
    _GET_PUMP_INFO = '#'
    _GET_PUMP_HEAD_MODEL_TYPE = ')'
    _SET_PUMP_HEAD_MODEL_TYPE = ')'
    _GET_CURRENT_SETTING_PUMP_TIME_IN_TENTHS_SEC = 'V'
    _SET_CURRENT_SETTING_PUMP_TIME_IN_TENTHS_SEC = 'V'
    _SET_CURRENT_RUN_TIME_SETTINGS_IN_MINS = 'VM'
    _SET_CURRENT_RUN_TIME_SETTINGS_IN_HOURS = 'VH'
    _GET_LOW_ORDER_ROLLER_STEPS = 'U'
    _SET_LOW_ORDER_ROLLER_STEPS = 'U'
    _GET_HIGH_ORDER_ROLLER_STEPS = 'u'
    _SET_HIGH_ORDER_ROLLER_STEPS = 'u'
    _GET_CURRENT_ROLLER_STEP_VOLUME = 'r'
    _SET_CURRENT_ROLLER_STEP_VOLUME = 'r'
    _RESET_PUMP_CLEAR_CALIBRATION_DATA = '000000'
    _GET_CURRENT_PAUSE_TIME_SETTINGS_IN_TENTHS_S = 'T'
    _SET_CURRENT_PAUSE_TIME_SETTINGS_IN_TENTHS_S = 'T'
    _SET_CURRENT_PAUSE_TIME_SETTINGS_IN_MINS = 'TM'
    _SET_CURRENT_PAUSE_TIME_SETTINGS_IN_HOURS = 'TH'
    _GET_TOTAL_VOL_DISPENSED_SINCE_RESET = ':'
    _SAVE_CURRENT_PUMP_SETTINGS_TO_MEMORY = '*'
    _GET_FOOT_SWITCH_STATE = 'C'

    # pump modes
    _MODE_CHANNEL_ADDRESSING = 1
    _MODE_LEGACY = 0
    _PUMP_MODES = [_MODE_RPM, _MODE_FLOW_RATE, _MODE_VOLUME_AT_RATE, _MODE_VOLUME_OVER_TIME,
                   _MODE_VOLUME_AND_PAUSE, _MODE_TIME, _MODE_TIME_AND_PAUSE]

    def __init__(self, device_port: str, address: int = 1):
        self._device_port = device_port
        self._pump_address = address
        self.ser: Serial = None
        self._lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
        self.connect()
        self.communication_mode = self._MODE_CHANNEL_ADDRESSING
        self.communication_mode = self.get_communication_mode()
        self.set_channel_addressing_mode()
        self.disable_event_messaging()
        self.event_messaging_mode = self.get_event_messaging_mode()

        # todo support reading event messages

    @property
    def device_port(self) -> str:
        return self._device_port

    @property
    def pump_address(self) -> int:
        # used to send commands to the pump while it is in legacy mode
        return self._pump_address

    @pump_address.setter
    def pump_address(self, value: int):
        response = self._send_and_receive(self._SET_ADDRESS, str(value))
        self.logger.debug(f'Set pump address to {value}')
        self._pump_address = value

    def running(self, pump_channel: int) -> bool:
        """
        Return true if the pump is currently running
        :return:
        """
        response = self._send_and_receive(self._CHECK_PUMP_RUNNING, pump_channel=pump_channel)
        if response == self._SR_POSITIVE:
            r = True
        else:
            r = False
        self.logger.debug(f'Pump channel {pump_channel} running: {r}')
        return r

    def connect(self):
        """Connect to the RegloICC"""
        try:
            if self.ser is None:
                cn = Serial(device_port=self.device_port,
                            **self._CONNECTION_SETTINGS,
                            )
                self.ser = cn
            else:
                self.ser.connect()
            self.pump_address = self.pump_address
            self.logger.debug(f'Connected to RegloICC, port: {self.device_port}, pump address: {self.pump_address}')
            # Ensure that the serial port is closed on system exit
            atexit.register(self.disconnect)
        except Exception as e:
            self.logger.warning("Could not connect to an RegloICC, make sure the right port was selected")
            raise PumpError("Could not connect to an RegloICC, make sure the right port was selected")

    def disconnect(self):
        """Disconnect from the RegloICC"""
        if self.ser is None:
            # if RegloICC is already disconnected then self.ser is None
            return
        try:
            self.ser.disconnect()
            self.ser = None
            self.logger.debug('Disconnected from RegloICC')
        except Exception as e:
            self.logger.warning("Could not disconnect from RegloICC")
            raise PumpError("Could not disconnect from RegloICC")

    # pump drive commands
    def start(self, pump_channel: int) -> str:
        """
        :return: * if successful
        """
        if self.running(pump_channel):
            self.logger.info(f'Pump channel {pump_channel} is already running')
            return ""
        response = self._send_and_receive(self._START, pump_channel=pump_channel)
        if response == self._SR_NEGATIVE:
            raise PumpError(f'Failed to start RegloICC pump_channel {pump_channel}, pump_channel settings are unavailable '
                            f'or not achievable')
        self.logger.debug(f'Start pump channel: {pump_channel}')
        return response

    def stop(self, pump_channel: int) -> str:
        """
        :return: * if successful
        """
        response = self._send_and_receive(self._STOP, pump_channel=pump_channel)
        self.logger.debug(f'Stop pump channel: {pump_channel}')
        return response

    def pause(self, pump_channel: int) -> str:
        """
        :return: * if successful
        """
        response = self._send_and_receive(self._PAUSE, pump_channel=pump_channel)
        self.logger.debug(f'Pause pump channel: {pump_channel}')
        return response

    def clockwise(self, pump_channel: int) -> bool:
        """

        :param pump_channel:

        :return: true if rotation direction for the pump channel is clockwise
        """
        response = self._send_and_receive(self._GET_PUMP_DIRECTION, pump_channel=pump_channel)
        if response == self._CLOCKWISE:
            cw = True
            direction = 'clockwise'
        else:
            cw = False
            direction = 'counter-clockwise'
        self.logger.debug(f'Rotation direction for pump channel {pump_channel}: {direction}')
        return cw

    def set_clockwise(self, pump_channel: int) -> str:
        """
        Set rotation direction to clockwise.
        :param pump_channel:
        :return:
        """
        response = self._send_and_receive(self._SET_ROTATION_CLOCKWISE, pump_channel=pump_channel)
        self.logger.debug(f'Set rotation direction for pump channel {pump_channel}: clockwise')
        return response

    def set_counter_clockwise(self, pump_channel: int) -> str:
        """
        Set rotation direction to counter-clockwise.
        :param pump_channel:
        :return:
        """
        response = self._send_and_receive(self._SET_ROTATION_COUNTER_CLOCKWISE, pump_channel=pump_channel)
        self.logger.debug(f'Set rotation direction for pump channel {pump_channel}: counter-clockwise')
        return response

    def get_cause_of_run_error(self) -> Tuple[str, float]:
        """
        Cause of ” –“ cannot run response = Parameter #1,
        Limiting value that was exceeded = Parameter #2
        Parameter #1:
            C = Cycle count of 0
            R = Max flow rate exceeded or flow is set to 0
            V = Max volume exceeded
        Parameter #2: Limiting value:
            C = Value is undefined
            R = Max flow (mL/min)
            V = Max vol (mL)
        :return: (parameter_1, parameter_2)
        """
        response = self._send_and_receive(self._GET_CAUSE_OF_RUN_ERROR)
        parameter_1 = response.split(' ')[0]
        parameter_2 = float(response.split(' ')[1])
        if parameter_1 == 'C':
            p1_str = "Cycle count of 0"
        elif parameter_1 == "R":
            p1_str = 'Max flow rate exceeded or flow is set to 0'
        else:
            p1_str = 'Max volume exceeded'
        self.logger.debug(f'Cause of run error: {p1_str}, value: {parameter_2}')
        return parameter_1, parameter_2

    # operational modes and settings

    def get_pump_mode(self, pump_channel: int) -> _PUMP_MODES:
        response = self._send_and_receive(self._GET_CURRENT_MODE, pump_channel=pump_channel)
        if response == self._MODE_RPM:
            mode = 'RPM'
        elif response == self._MODE_FLOW_RATE:
            mode = 'FLOW RATE'
        elif response == self._MODE_VOLUME_AT_RATE:
            mode = 'VOLUME AT RATE'
        elif response == self._MODE_VOLUME_OVER_TIME:
            mode = 'VOLUME OVER TIME'
        elif response == self._MODE_VOLUME_AND_PAUSE:
            mode = 'VOLUME AND PAUSE'
        elif response == self._MODE_TIME:
            mode = 'TIME'
        elif response == self._MODE_TIME_AND_PAUSE:
            mode = 'TIME AND PAUSE'
        self.logger.debug(f'Pump mode of pump channel {pump_channel}: {mode}')
        return response

    def set_pump_mode(self, mode: _PUMP_MODES, pump_channel: int):
        if mode == self._MODE_RPM:
            self.set_mode_pump_rpm(pump_channel)
        elif mode == self._MODE_FLOW_RATE:
            self.set_mode_pump_flow_rate(pump_channel)
        elif mode == self._MODE_VOLUME_AT_RATE:
            self.set_mode_pump_volume_at_rate(pump_channel)
        elif mode == self._MODE_VOLUME_OVER_TIME:
            self.set_mode_pump_volume_over_time(pump_channel)
        elif mode == self._MODE_VOLUME_AND_PAUSE:
            self.set_mode_pump_volume_and_pause(pump_channel)
        elif mode == self._MODE_TIME:
            self.set_mode_pump_time(pump_channel)
        elif mode == self._MODE_TIME_AND_PAUSE:
            self.set_mode_pump_time_and_pause(pump_channel)

    def set_mode_pump_rpm(self, pump_channel: int, rpm: float = None) -> str:
        """
        Set pump mode to RPM for the pump channel

        :return: * if successful
        """
        response = self._send_and_receive(self._MODE_RPM, pump_channel=pump_channel)
        self.logger.debug(f'Set mode of pump channel {pump_channel} to: RPM')
        if rpm is not None:
            self.set_flow_rate_rpm(rpm, pump_channel)
        return response

    def set_mode_pump_flow_rate(self, pump_channel: int, flow_rate: str = None) -> str:
        """
        Set pump mode to flow rate for the pump channel

        :param pump_channel:
        :param flow_rate:

        :return: * if successful
        """
        response = self._send_and_receive(self._MODE_FLOW_RATE, pump_channel=pump_channel)
        self.logger.debug(f'Set mode of pump channel {pump_channel} to: FLOW RATE')
        if flow_rate is not None:
            self.set_flow_rate_ml_min(flow_rate, pump_channel)
        return response

    def set_mode_pump_volume_at_rate(self, pump_channel: int, flow_rate: str = None, volume: str = None) -> str:
        """
        Set pump mode to volume (at rate) for the pump channel

        :return: * if successful
        """
        response = self._send_and_receive(self._MODE_VOLUME_AT_RATE, pump_channel=pump_channel)
        self.logger.debug(f'Set mode of pump channel {pump_channel} to: VOLUME (AT RATE)')
        if flow_rate is not None:
            self.set_flow_rate_ml_min(flow_rate, pump_channel)
        if volume is not None:
            self.set_volume(volume, pump_channel)
        return response

    def set_mode_pump_volume_over_time(self, pump_channel: int, volume: str = None, run_time: float = None) -> str:
        """
        Set pump mode to volume (over time) for the pump channel

        :return: * if successful
        """
        response = self._send_and_receive(self._MODE_VOLUME_OVER_TIME, pump_channel=pump_channel)
        if response == self._SR_NEGATIVE:
            raise CommandError(f'Fail to set pump mode to volume (over time) for pump channel {pump_channel}. Channel '
                               f'setting(s) are not correct or unachievable')
        self.logger.debug(f'Set mode of pump channel {pump_channel} to: VOLUME (OVER TIME)')
        if volume is not None:
            self.set_volume(volume, pump_channel)
        if run_time is not None:
            self.set_run_time(run_time, pump_channel)
        return response

    def set_mode_pump_volume_and_pause(self, pump_channel: int, flow_rate: str = None, volume: str = None,
                                       pause_time: float = None) -> str:
        """
        Set pump mode to volume and pause for the pump channel

        :return: * if successful
        """
        response = self._send_and_receive(self._MODE_VOLUME_AND_PAUSE, pump_channel=pump_channel)
        self.logger.debug(f'Set mode of pump channel {pump_channel} to: VOLUME AND PAUSE')
        if flow_rate is not None:
            self.set_flow_rate_ml_min(flow_rate, pump_channel)
        if volume is not None:
            self.set_volume(volume, pump_channel)
        if pause_time is not None:
            self.set_pumping_pause_time(pause_time, pump_channel)
        if volume is not None:
            self.set_volume(volume, pump_channel)
        return response

    def set_mode_pump_time(self, pump_channel: int, flow_rate: str = None, run_time: float = None) -> str:
        """
        Set pump mode to time for the pump channel

        :return: * if successful
        """
        response = self._send_and_receive(self._MODE_TIME, pump_channel=pump_channel)
        self.logger.debug(f'Set mode of pump channel {pump_channel} to: TIME')
        if flow_rate is not None:
            self.set_flow_rate_ml_min(flow_rate, pump_channel)
        if run_time is not None:
            self.set_run_time(run_time, pump_channel)
        return response

    def set_mode_pump_time_and_pause(self, pump_channel: int, flow_rate: str = None, run_time: float = None,
                                     pause_time: float = None) -> str:
        """
        Set pump mode to time and pause for the pump channel

        :return: * if successful
        """
        response = self._send_and_receive(self._MODE_TIME_AND_PAUSE, pump_channel=pump_channel)
        self.logger.debug(f'Set mode of pump channel {pump_channel} to: TIME AND PAUSE')
        if flow_rate is not None:
            self.set_flow_rate_ml_min(flow_rate, pump_channel)
        if run_time is not None:
            self.set_run_time(run_time, pump_channel)
        if pause_time is not None:
            self.set_pumping_pause_time(pause_time, pump_channel)
        return response

    # todo not sure about implementing this
    # def get_flow_rate(self, pump_channel: int):
    #     """
    #     Get flow rate from RPM (S) or flow rate (f) when mode is not RPM or flow rate
    #
    #     :param pump_channel:
    #     :return:
    #     """
    #     response = self._send_and_receive(self._GET_FLOW_RATE, pump_channel=pump_channel)
    #     self.logger.debug(f'Pump firmware version for pump channel {pump_channel}: {response}')
    #     return int(response)

    # todo not sure about implementing this
    # def set_flow_rate(self, flow_rate: int, pump_channel: int) -> str:
    #     """
    #     Set RPM flow rate not in RPM or flow rate mode
    #
    #     :param int, flow_rate: integer 0-999999
    #     :param pump_channel:
    #     :return:
    #     """
    #     response = self._send_and_receive(self._SET_FLOW_RATE, str(flow_rate).zfill(6),
    #                                       pump_channel=pump_channel)
    #     self.logger.debug(f'Set flow rate for pump channel {pump_channel}: {response} mL/min')
    #     return response

    def get_flow_rate_rpm(self, pump_channel: int) -> float:
        """
        Gets the current speed setting in RPM.
        :param pump_channel:
        :return:
        """
        response = float(self._send_and_receive(self._GET_RPM_SPEED, pump_channel=pump_channel))
        self.logger.debug(f'Speed for pump channel {pump_channel}: {response} rpm')
        return response

    def set_flow_rate_rpm(self, rpm: float, pump_channel: int) -> str:
        """
        RPM mode flow rate setting (RPM)
        For modes: [RegloICC._MODE_RPM]

        :param float, rpm: 0-9999.99
        :param pump_channel:
        :return:
        """
        if rpm > 9999.99:
            raise CommandError(f'RPM mode flow rate speed cannot be set to > 9999.99 rpm')
        formatted_rpm = str(int(rpm / 0.01)).zfill(6)
        response = self._send_and_receive(self._SET_RPM_SPEED, formatted_rpm, pump_channel=pump_channel)
        self.logger.debug(f'Set RPM mode flow rate speed for pump channel {pump_channel}: {rpm} rpm')
        return response

    def get_flow_rate_ml_min(self, pump_channel: int) -> float:
        """
        Get current volume/time flow rate (uL/min)
        :param pump_channel:
        :return:
        """
        response = self._send_and_receive(self._GET_FLOW_RATE_VOLUME_TIME_MODE, pump_channel=pump_channel)
        # response is in the form mmmmEse; Represents the scientific notation of m.mmm x 10se.
        # For example, 1.200 x 10-2 is represented with 1200E-2
        # units is L/min
        response = float(response)/1000
        self.logger.debug(f'Current volume/time flow rate for pump channel {pump_channel}: {response} mL/min')
        return response

    def set_flow_rate_ml_min(self, flow_rate: str, pump_channel: int) -> str:
        """
        Set RPM flow rate in volume/time mode (mL/min).
        For modes: [RegloICC._MODE_FLOW_RATE, RegloICC._MODE_VOLUME_AND_PAUSE, RegloICC._MODE_VOLUME_AT_RATE,
        RegloICC._MODE_TIME_AND_PAUSE, RegloICC._MODE_TIME]

        :param float, flow_rate: in the form m.mmmEse, which represents the scientific notation of m.mmm x 10se. For
            example, 1.200 x 10-2 is represented with 1.200E-2. Units is mL/min.
        :param pump_channel:
        :return:
        """
        if type(flow_rate) != str:
            raise CommandError('Volume must be a string in the format m.mmmEse, which represents the scientific '
                               'notation of m.mmm x 10se. For example, 1.200 x 10-2 is represented with 1.200E-2.')
        if len(flow_rate) != 8:
            raise CommandError('Volume must be a string in the format m.mmmEse, which represents the scientific '
                               'notation of m.mmm x 10se. For example, 1.200 x 10-2 is represented with 1.200E-2.')
        value = flow_rate.replace('.', '')
        value = value.replace('E', '')
        response = self._send_and_receive(self._SET_FLOW_RATE_VOLUME_TIME_MODE, value, pump_channel=pump_channel)
        self.logger.debug(f'Set volume for pump channel {pump_channel} to: {flow_rate} mL')
        return response

    def get_volume(self, pump_channel: int) -> float:
        """
        Get the current setting for volume in mL
        :param pump_channel:
        :return:
        """
        response = self._send_and_receive(self._GET_VOLUME, pump_channel=pump_channel)
        # response is in the form mmmmEse; Represents the scientific notation of m.mmm x 10se.
        # For example, 1.200 x 10-2 is represented with 1200E-2
        # units is L
        response = float(response) / 1000
        self.logger.debug(f'Current volume for pump channel {pump_channel}: {response} mL')
        return response

    def set_volume(self, volume: str, pump_channel: int) -> str:
        """
        Set the current setting for volume in mL.
        f=For modes: [RegloICC._MODE_VOLUME_AT_RATE, RegloICC._MODE_VOLUME_OVER_TIME, RegloICC._MODE_VOLUME_AND_PAUSE]

        :param float, volume: in the form m.mmmEse, which represents the scientific notation of m.mmm x 10se. For
            example, 1.200 x 10-2 is represented with 1.200E-2. Units is mL
        :param pump_channel:
        :return:
        """
        if type(volume) != str:
            raise CommandError('Volume must be a string in the format m.mmmEse, which represents the scientific '
                               'notation of m.mmm x 10se. For example, 1.200 x 10-2 is represented with 1.200E-2.')
        if len(volume) != 8:
            raise CommandError('Volume must be a string in the format m.mmmEse, which represents the scientific '
                               'notation of m.mmm x 10se. For example, 1.200 x 10-2 is represented with 1.200E-2.')
        value = volume.replace('.', '')
        value = value.replace('E', '')
        response = self._send_and_receive(self._SET_VOLUME, value, pump_channel=pump_channel)
        self.logger.debug(f'Set volume for pump channel {pump_channel} to: {volume} mL')
        return response

    def get_run_time(self, pump_channel: int) -> float:
        """
        Get the current pump run time in s
        :param pump_channel:
        :return:
        """
        response = self._send_and_receive(self._GET_PUMP_RUN_TIME, pump_channel=pump_channel)
        # units of response is 0.1 s
        t = float(response) * 0.1
        self.logger.debug(f'Current run time for pump channel {pump_channel}: {t} s')
        return t

    def set_run_time(self, run_time: float, pump_channel: int) -> str:
        """
        Set the current pump run time in s.
        For modes: [RegloICC._MODE_VOLUME_OVER_TIME, RegloICC._MODE_TIME, RegloICC._MODE_TIME_AND_PAUSE]

        :param float, run_time: float between 0-3596400
        :param pump_channel:
        :return:
        """
        if run_time > 3596400:
            raise CommandError("Cannot set pump run time > 3596400 s")
        t = int(run_time / 0.1)
        n_digits = 8
        t = str(t).zfill(n_digits)
        response = self._send_and_receive(self._SET_PUMP_RUN_TIME, t, pump_channel=pump_channel)
        self.logger.debug(f'Set run time for pump channel {pump_channel} to: {run_time} seconds')
        return response

    def get_pumping_pause_time(self, pump_channel: int) -> float:
        """
        Get the pumping pump pause time in s
        :param pump_channel:
        :return:
        """
        response = self._send_and_receive(self._GET_PUMP_PAUSE_TIME, pump_channel=pump_channel)
        # units of response is 0.1 s
        t = float(response) * 0.1
        self.logger.debug(f'Current pause time for pump channel {pump_channel}: {t} s')
        return t

    def set_pumping_pause_time(self, pause_time: float, pump_channel: int) -> str:
        """
        Set the pumping pump pause time in s.
        For modes: [RegloICC._MODE_VOLUME_AND_PAUSE, RegloICC._MODE_TIME_AND_PAUSE]

        :param float, run_time: float between 0-3596400
        :param pump_channel:
        :return:
        """
        if pause_time > 3596400:
            raise CommandError("Cannot set pump pause time > 3596400 s")
        t = int(pause_time / 0.1)
        n_digits = 8
        t = str(t).zfill(n_digits)
        response = self._send_and_receive(self._SET_PUMP_PAUSE_TIME, t, pump_channel=pump_channel)
        self.logger.debug(f'Set pause time for pump channel {pump_channel} to: {pause_time} seconds')
        return response

    def get_cycle_count(self, pump_channel: int) -> int:
        """
        Get pump cycle count

        :param pump_channel:
        :return:
        """
        response = int(self._send_and_receive(self._GET_PUMP_CYCLE_COUNT, pump_channel=pump_channel))
        self.logger.debug(f'Cycle count for pump channel {pump_channel}: {response}')
        return response

    def set_cycle_count(self, count: int, pump_channel: int) -> str:
        """
        Set pump cycle count.
        For modes: [RegloICC._MODE_VOLUME_AND_PAUSE, RegloICC._MODE_TIME_AND_PAUSE]

        :param float, count: int between 0-9999
        :param pump_channel:
        :return:
        """
        if count > 9999:
            raise CommandError("Cannot set cycle count > 9999")
        n_digits = 4
        c = str(count).zfill(n_digits)
        response = self._send_and_receive(self._SET_PUMP_CYCLE_COUNT, c, pump_channel=pump_channel)
        self.logger.debug(f'Set cycle count for pump channel {pump_channel} to: {count}')
        return response

    def get_max_flow_rate(self, pump_channel: int) -> float:
        """
        Max flow rate achievable with current settings mL/min.

        :param pump_channel:
        :return:
        """
        response = self._send_and_receive(self._GET_MAX_FLOW_RATE, pump_channel=pump_channel)
        rate = float(response.split(' ')[0])
        self.logger.debug(f'Max flow rate achievable with current settings for pump channel {pump_channel}: '
                          f'{rate} mL/min')
        return rate

    def get_max_flow_rate_using_calibration(self, pump_channel: int) -> float:
        """
        Max flow rate achievable with current settings using calibration mL/min

        :param pump_channel:
        :return:
        """
        response = self._send_and_receive(self._GET_MAX_FLOW_RATE_USING_CALIBRATION, pump_channel=pump_channel)
        rate = float(response.split(' ')[0])
        self.logger.debug(f'Max flow rate achievable with current settings from calibration for pump channel'
                          f' {pump_channel}: {rate} mL/min')
        return rate

    # todo _GET_TIME_TO_DISPENSE_VOLUME_AT_FLOW_RATE

    # todo _GET_TIME_TO_DISPENSE_VOLUME_AT_RPM

    # configuration
    def get_tubing_inner_diameter(self, pump_channel: int) -> float:
        """
        Get the current tubing inside diameter in mm.

        :param pump_channel:
        :return:
        """
        response = self._send_and_receive(self._GET_TUBING_INNER_DIAMETER, pump_channel=pump_channel)
        diameter = float(response.split(' ')[0])
        self.logger.debug(f'Tubing inner diameter for pump channel {pump_channel}: {diameter} mm')
        return diameter

    def set_tubing_inner_diameter(self, diameter: float, pump_channel: int) -> str:
        """
        Set tubing inside diameter, mm

        :param float, diameter:
        :param pump_channel:
        :return:
        """
        n_digits = 4
        d = round(diameter, 2)
        d = str(d).replace('.', '')
        d = d.zfill(n_digits)
        response = self._send_and_receive(self._SET_TUBING_INNER_DIAMETER, d, pump_channel=pump_channel)
        self.logger.debug(f'Set tubing inner diameter for pump channel {pump_channel} to: {diameter} mm')
        return response

    def get_backsteps_setting(self, pump_channel: int) -> int:
        """
        Get the current backsteps setting

        :param pump_channel:
        :return:
        """
        response = int(self._send_and_receive(self._GET_BACKSTEPS_SETTING, pump_channel=pump_channel))
        self.logger.debug(f'Backsteps setting for pump channel {pump_channel}: {response}')
        return response

    def set_backsteps_setting(self, backsteps: int, pump_channel: int) -> str:
        """
        Set the current backsteps setting

        :param float, backsteps:
        :param pump_channel:
        :return:
        """
        n_digits = 4
        b = str(backsteps).zfill(n_digits)
        response = self._send_and_receive(self._SET_BACKSTEPS_SETTING, b, pump_channel=pump_channel)
        self.logger.debug(f'Set backsteps setting for pump channel: {pump_channel} to: {b} ')
        return response

    def reset_configurable_data_to_default(self) -> str:
        response = self._send_and_receive(self._RESET_CONFIGURABLE_DATA_TO_DEFAULT)
        self.logger.debug(f'Reset all user configurable data to default values')
        return response

    # calibration
    def calibration_direction_clockwise(self, pump_channel: int) -> bool:
        """

        :param pump_channel:

        :return: true if rotation direction for the pump channel is clockwise for calibration
        """
        response = self._send_and_receive(self._GET_CALIBRATION_DIRECTION, pump_channel=pump_channel)
        if response == self._CLOCKWISE:
            cw = True
            direction = 'clockwise'
        else:
            cw = False
            direction = 'counter-clockwise'
        self.logger.debug(f'Rotation direction for calibration for pump channel {pump_channel}: {direction}')
        return cw

    def set_calibration_direction_clockwise(self, pump_channel: int) -> str:
        """
        Set calibration rotation direction to clockwise.
        :param pump_channel:
        :return:
        """
        response = self._send_and_receive(self._SET_CALIBRATION_DIRECTION, self._CLOCKWISE, pump_channel=pump_channel)
        self.logger.debug(f'Set calibration rotation direction for pump channel {pump_channel}: clockwise')
        return response

    def set_calibration_direction_counter_clockwise(self, pump_channel: int) -> str:
        """
        Set calibration rotation direction to counter-clockwise.
        :param pump_channel:
        :return:
        """
        response = self._send_and_receive(self._SET_CALIBRATION_DIRECTION, self._COUNTER_CLOCKWISE,
                                          pump_channel=pump_channel)
        self.logger.debug(f'Set calibration rotation direction for pump channel {pump_channel}: counter-clockwise')
        return response

    def get_target_calibration_volume(self, pump_channel: int) -> float:
        """
        Get the target volume to pump for calibrating, mL
        :param pump_channel:
        :return:
        """
        response = self._send_and_receive(self._GET_CALIBRATION_TARGET_VOLUME_TO_PUMP, pump_channel=pump_channel)
        # response is in the form mmmmEse; Represents the scientific notation of m.mmm x 10se.
        # For example, 1.200 x 10-2 is represented with 1200E-2
        # units is L
        response = float(response) / 1000
        self.logger.debug(f'Target calibration volume for pump channel {pump_channel}: {response} mL')
        return response

    def set_target_calibration_volume(self, volume: str, pump_channel: int) -> str:
        """
        Set the target volume to pump for calibrating in mL.

        :param float, volume: in the form m.mmmEse, which represents the scientific notation of m.mmm x 10se. For
            example, 1.200 x 10-2 is represented with 1.200E-2. Units is mL
        :param pump_channel:
        :return:
        """
        if type(volume) != str:
            raise CommandError('Volume must be a string in the format m.mmmEse, which represents the scientific '
                               'notation of m.mmm x 10se. For example, 1.200 x 10-2 is represented with 1.200E-2.')
        if len(volume) != 8:
            raise CommandError('Volume must be a string in the format m.mmmEse, which represents the scientific '
                               'notation of m.mmm x 10se. For example, 1.200 x 10-2 is represented with 1.200E-2.')
        value = volume.replace('.', '')
        value = value.replace('E', '')
        response = self._send_and_receive(self._SET_CALIBRATION_TARGET_VOLUME_TO_PUMP, value, pump_channel=pump_channel)
        self.logger.debug(f'Set target calibration volume for pump channel {pump_channel} to: {volume} mL')
        return response

    def get_actual_calibration_volume(self, pump_channel: int) -> float:
        """
        Get the actual calibration volume, mL
        :param pump_channel:
        :return:
        """
        response = self._send_and_receive(self._GET_CALIBRATION_ACTUAL_VOLUME_MEASURE, pump_channel=pump_channel)
        # response is in the form mmmmEse; Represents the scientific notation of m.mmm x 10se.
        # For example, 1.200 x 10-2 is represented with 1200E-2
        # units is L
        response = float(response) / 1000
        self.logger.debug(f'Actual measured calibration volume for pump channel {pump_channel}: {response} mL')
        return response

    def set_actual_calibration_volume(self, volume: str, pump_channel: int) -> str:
        """
        Set the measured calibration volume during calibration, mL

        :param float, volume: in the form m.mmmEse, which represents the scientific notation of m.mmm x 10se. For
            example, 1.200 x 10-2 is represented with 1.200E-2. Units is mL
        :param pump_channel:
        :return:
        """
        if type(volume) != str:
            raise CommandError('Volume must be a string in the format m.mmmEse, which represents the scientific '
                               'notation of m.mmm x 10se. For example, 1.200 x 10-2 is represented with 1.200E-2.')
        if len(volume) != 8:
            raise CommandError('Volume must be a string in the format m.mmmEse, which represents the scientific '
                               'notation of m.mmm x 10se. For example, 1.200 x 10-2 is represented with 1.200E-2.')
        value = volume.replace('.', '')
        value = value.replace('E', '')
        response = self._send_and_receive(self._SET_CALIBRATION_ACTUAL_VOLUME_MEASURE, value, pump_channel=pump_channel)
        self.logger.debug(f'Set actual measured calibration volume for pump channel {pump_channel} to: {volume} mL')
        return response

    def get_calibration_time(self, pump_channel: int) -> float:
        """Get the current calibration time in seconds"""
        response = self._send_and_receive(self._GET_CALIBRATION_TIME, pump_channel=pump_channel)  # returned
        # in 1/10 sec
        t = float(response) * 0.1
        self.logger.debug(f'Calibration time for pump channel {pump_channel}: {t} seconds')
        return t

    def set_calibration_time(self, t: float, pump_channel: int) -> str:
        """
        Set the current calibration time using seconds, between 0 and 999.9 seconds
        Command that gets sent to the pump can be sent as 0000-9999 1/10 sec

        :param float, t: dispensing time in seconds between 0 and 999.9 seconds
        :param int, pump_channel:
        """
        if type(t) != int or type(t) != float:
            try:
                t = float(t)
            except Exception:
                raise CommandError('Calibration time must be an integer')
        if t > 999.9 or t < 0:
            raise CommandError('Calibration time must be between 0 and 999.9 s')
        # convert to 1/10 sec
        t = int(t / 0.1)
        n_digits = 8
        t = str(t).zfill(n_digits)
        response = self._send_and_receive(self._SET_CALIBRATION_TIME, t, pump_channel=pump_channel)
        self.logger.debug(f'Set calibration time for pump channel {pump_channel} to {int(t) * 0.1} seconds')
        return response

    def get_run_time_since_last_calibration(self, pump_channel: int) -> float:
        """Get the channel run time since last calibration"""
        response = self._send_and_receive(self._GET_CHANNEL_RUN_TIME_SINCE_LAST_CALIBRATION, pump_channel=pump_channel)
        # returned in 1/10 sec
        t = float(response) * 0.1
        self.logger.debug(f'Run time since last calibration for pump channel {pump_channel}: {t} seconds')
        return t

    def start_calibration(self, pump_channel: int) -> str:
        """Start calibration on a channel"""
        response = self._send_and_receive(self._START_CALIBRATION, pump_channel=pump_channel)
        self.logger.debug(f'Start calibration for pump channel {pump_channel}')
        return response

    def cancel_calibration(self, pump_channel: int) -> str:
        """Cancel calibration on a channel"""
        response = self._send_and_receive(self._CANCEL_CALIBRATION, pump_channel=pump_channel)
        self.logger.debug(f'Cancel calibration for pump channel {pump_channel}')
        return response

    # system commands
    def get_pump_firmware_version(self) -> int:
        response = int(self._send_and_receive(self._GET_PUMP_FIRMWARE_VERSION))
        self.logger.debug(f'Pump firmware version: {response}')
        return response

    # todo set factory roller step vol

    def save_set_roller_step_settings(self) -> str:
        response = self._send_and_receive(self._SAVE_SET_ROLLER_STEP_SETTINGS)
        self.logger.debug(f'Save set roller step settings')
        return response

    def reset_roller_step_volume(self) -> str:
        response = self._send_and_receive(self._RESET_ROLLER_STEP_VOLUME_TO_DEFAULTS)
        self.logger.debug(f'Reset roller step volume table to defaults')
        return response

    def set_pump_name(self, name: str) -> str:
        """
        Text gets shown when the pump UI is disabled
        :param name:
        :return:
        """
        response = self._send_and_receive(self._SET_PUMP_NAME, name)
        self.logger.debug(f'Set pump temporary display name to {name}')
        return response

    def get_pump_serial_number(self) -> str:
        response = self._send_and_receive(self._GET_PUMP_SERIAL_NUMBER)
        self.logger.debug(f'Pump serial number: {response}')
        return response

    def set_pump_serial_number(self, serial_number: str) -> str:
        response = self._send_and_receive(self._SET_PUMP_SERIAL_NUMBER, serial_number)
        self.logger.debug(f'Set pump serial number: {serial_number}')
        return response

    def get_pump_language(self) -> int:
        """
        Response mapping:
            0 - English
            1 - French
            2 - Spanish
            3 - German
        :return:
        """
        response = int(self._send_and_receive(self._GET_PUMP_LANGUAGE))
        if response == 0:
            l = 'English'
        elif response == 1:
            l = 'French'
        elif response == 2:
            l = 'Spanish'
        else:
            l = 'German'
        self.logger.debug(f'Pump language: {l}')
        return response

    def set_pump_language(self, language: int) -> str:
        """
        Language  mapping:
            0 - English
            1 - French
            2 - Spanish
            3 - German
        :param language: 0 to 3
        :return:
        """
        response = self._send_and_receive(self._GET_PUMP_LANGUAGE, str(language))
        if language == 0:
            l = 'English'
        elif language == 1:
            l = 'French'
        elif language == 2:
            l = 'Spanish'
        else:
            l = 'German'
        self.logger.debug(f'Set pump language: {l}')
        return response

    def get_n_pump_channels(self) -> int:
        response = int(self._send_and_receive(self._GET_N_PUMP_CHANNELS))
        self.logger.debug(f'Number of pump channels: {response}')
        return response

    def set_n_pump_channels(self, n: int) -> str:
        response = self._send_and_receive(self._SET_N_PUMP_CHANNELS, str(n).zfill(4))
        self.logger.debug(f'Set number of pump channels: {n}')
        return response

    def get_n_rollers_for_channel(self, pump_channel: int) -> int:
        response = int(self._send_and_receive(self._GET_N_ROLLERS_FOR_CHANNEL, pump_channel=pump_channel))
        self.logger.debug(f'Number of rollers for pump_channel {pump_channel}: {response}')
        return response

    def set_n_rollers_for_channel(self, pump_channel: int, n: int) -> str:
        response = self._send_and_receive(self._SET_N_ROLLERS_FOR_CHANNEL, str(n).zfill(4), pump_channel=pump_channel)
        self.logger.debug(f'Set number of rollers for pump_channel {pump_channel}: {n}')
        return response

    def get_n_revolutions_since_reset(self, pump_channel: int) -> int:
        response = int(self._send_and_receive(self._GET_N_REVOLUTIONS_SINCE_RESET, pump_channel=pump_channel))
        self.logger.debug(f'Number of revolutions since last reset for pump channel {pump_channel}: {response}')
        return response

    def get_volume_pumped_since_reset(self, pump_channel: int) -> int:
        response = int(self._send_and_receive(self._GET_CHANNEL_TOTAL_VOLUME_PUMPED_SINCE_RESET, pump_channel=pump_channel))
        self.logger.debug(f'Total volume pumped since last reset for pump channel {pump_channel}: {response} mL')
        return response

    def get_time_pumped_since_reset(self, pump_channel: int) -> float:
        response = float(self._send_and_receive(self._GET_TOTAL_TIME_PUMPED_SINCE_RESET, pump_channel=pump_channel))
        # units of response is 0.1 s
        t = float(response) * 0.1
        self.logger.debug(f'Total time pumped since last reset for pump channel {pump_channel}: {t} s')
        return response

    def set_control_from_pump_ui(self) -> str:
        response = self._send_and_receive(self._SET_CONTROL_FROM_PUMP_UI)
        self.logger.debug(f'Set control from the pump UI')
        return response

    def disable_pump_ui(self) -> str:
        response = self._send_and_receive(self._DISABLE_CONTROL_FROM_PUMP_UI)
        self.logger.debug(f'Disable pump UI')
        return response

    def write_to_display(self, text: Union[str, float]) -> Union[str, None]:
        """
        Max 16 characters. Writes text to pump display while the pump UI is disabled

        :return: * if successful
        """
        if type(text) == str:
            command = self._WRITE_LETTERS_TO_PUMP_DISPLAY
            if len(text) > 16:
                text = text[:16]
        elif type(text) == float or type(text) == int:
            command = self._WRITE_NUMBERS_TO_PUMP_DISPLAY
            if len(str(text)) > 16:
                text = str(str(text)[:16])
        else:
            self.logger.warning(f'Cannot write {text} to the display, it must be letters or numbers only')
            return
        response = self._send_and_receive(command, text)
        self.logger.debug(f'Write {text} to the display')
        return response

    def get_pump_info(self) -> Tuple[str, int, int]:
        """
        Returns the following fields, each separated by a space:
            Pump model description: A text field describing the model of pump. This description may contain spaces.
            Pump software version: The version of software currently running in the pump.
            Pump head model type code: A code describing the type of pump head installed. The first digit represents
                the number of channels for the pump, and the second 2 digits represent the number of rollers. XX if
                channels do not have the same number of rollers.

        :return: Return a tuple of: (pump model description: str, pump software version: int, pump head model type
            code: str)

        """
        response = self._send_and_receive(self._GET_PUMP_INFO)
        response = response.rsplit(sep=' ', maxsplit=2)
        response[1] = int(response[1])
        response[2] = int(response[2])
        response = tuple(response)
        self.logger.debug(f'Pump model description: {response[0]} - Pump software version: {response[1]} - Pump head '
                          f'model type code: {response[2]}')
        return response

    def get_pump_head_model_type_code(self) -> int:
        """
        Returns the pump head model type code–A 4 digit code indicating the ID number of the pump head. The first two
        digits represent the number of channels on the head, and the second 2 digits represent the number of rollers.

        :return:
        """
        response = int(self._send_and_receive(self._GET_PUMP_HEAD_MODEL_TYPE))
        self.logger.debug(f'Pump head model type code: {response}')
        return response

    def set_pump_head_model_type_code(self, code: int) -> str:
        """
        Sets the pump head model type code –An up-to 4 digit code setting the ID number of the pump head. The first two
         digits encode the number of channels on the head, the second two digits encode the number of rollers on the
         head. This command sets all roller counts to the same value. To individually set roller counts for each
         channel, use the non-legacy command designed for this operation

        :param int, code: A 4 digit code indicating the ID number of the pump head. The first two digits represent
            the number of channels on the head, and the second 2 digits represent the number of rollers.
        :return:
        """
        response = self._send_and_receive(self._SET_PUMP_HEAD_MODEL_TYPE, str(code).zfill(4))
        self.logger.debug(f'Set pump head model type code to: {code}')
        return response

    def get_dispensing_time(self, pump_channel: int) -> float:
        """Get the current setting for pump dispensing time in seconds"""
        response = self._send_and_receive(self._GET_CURRENT_SETTING_PUMP_TIME_IN_TENTHS_SEC, pump_channel=pump_channel) # returned
        # in 1/10 sec
        t = float(response) * 0.1
        self.logger.debug(f'Pump dispensing time for pump channel {pump_channel}: {t} seconds')
        return t

    def set_dispensing_time_s(self, t: float, pump_channel: int) -> str:
        """
        Set the pump dispensing time in seconds, between 0 and 999.9 seconds
        Command that gets sent to the pump can be sent as 0000-9999 1/10 sec

        :param float, t: dispensing time in seconds between 0 and 999.9 seconds
        """
        if type(t) != int or type(t) != float:
            try:
                t = float(t)
            except Exception:
                raise CommandError('Dispensing time must be an integer')
        if t > 999.9 or t < 0:
            raise CommandError('Dispensing time must be between 0 and 999.9 s')
        # convert to 1/10 sec
        t = int(t / 0.1)
        n_digits = 4
        t = str(t).zfill(n_digits)
        response = self._send_and_receive(self._SET_CURRENT_SETTING_PUMP_TIME_IN_TENTHS_SEC, t, pump_channel=pump_channel)
        self.logger.debug(f'Set dispensing time for pump channel {pump_channel} to {int(t) * 0.1} seconds')
        return response

    def set_dispensing_time_m(self, t: int, pump_channel: int) -> str:
        """
        Set the pump dispensing time in minutes, between 0 and 999 minutes
        Command that gets sent to the pump can be sent as 000-999 minutes

        :param float, t: dispensing time in min between 0 and 999 minutes
        """
        if type(t) != int:
            try:
                t = int(t)
            except Exception:
                raise CommandError('Dispensing time must be an integer')
        if t > 999 or t < 0:
            raise CommandError('Dispensing time must be between 0 and 999')
        n_digits = 3
        t = str(t).zfill(n_digits)
        response = self._send_and_receive(self._SET_CURRENT_RUN_TIME_SETTINGS_IN_MINS, t, pump_channel=pump_channel)
        self.logger.debug(f'Set dispensing time for pump channel {pump_channel} to: {int(t)} minutes')
        return response

    def set_dispensing_time_h(self, t: int, pump_channel: int) -> str:
        """
        Set the pump dispensing time in hours, between 0 and 999 hours
        Command that gets sent to the pump can be sent as 000-999 hours

        :param float, t: dispensing time in hours between 0 and 999 hours
        """
        if type(t) != int:
            try:
                t = int(t)
            except Exception:
                raise CommandError('Dispensing time must be an integer')
        if t > 999 or t < 0:
            raise CommandError('Dispensing time must be between 0 and 999')
        n_digits = 3
        t = str(t).zfill(n_digits)
        # response is * if successful
        response = self._send_and_receive(self._SET_CURRENT_RUN_TIME_SETTINGS_IN_HOURS, t, pump_channel=pump_channel)
        self.logger.debug(f'Set dispensing time for pump channel {pump_channel} to: {int(t)} hours')
        return response

    def get_low_order_roller_steps(self) -> int:
        """
        Get the low order roller steps. The total number of roller steps which are dispensed during an
        operation is computed as:[(u*65536]+(U)]

        :return:
        """
        response = int(self._send_and_receive(self._GET_LOW_ORDER_ROLLER_STEPS))
        self.logger.debug(f'Low order roller steps: {response}')
        return response

    def set_low_order_roller_steps(self, n_steps: int):
        if n_steps > 99999:
            raise CommandError(f'Value to set as the low order roller steps must be <= 99999')
        response = self._send_and_receive(self._SET_LOW_ORDER_ROLLER_STEPS, str(n_steps).zfill(5))
        self.logger.debug(f'Set low order roller steps to: {n_steps}')
        return response

    def get_high_order_roller_steps(self) -> int:
        """
        Get the low order roller steps. The total number of roller steps which are dispensed during an
        operation is computed as:[(u*65536]+(U)]

        :return:
        """
        response = int(self._send_and_receive(self._GET_HIGH_ORDER_ROLLER_STEPS))
        self.logger.debug(f'High order roller steps: {response}')
        return response

    def set_high_order_roller_steps(self, n_steps: int):
        if n_steps > 99999:
            raise CommandError(f'Value to set as the high order roller steps must be <= 99999')
        response = self._send_and_receive(self._SET_HIGH_ORDER_ROLLER_STEPS, str(n_steps).zfill(5))
        self.logger.debug(f'Set high order roller steps to: {n_steps}')
        return response

    def get_roller_step_volume(self, pump_channel: int) -> float:
        """
        Get the current roller step volume based on the current calibration, tubing diameter and roller count.
        If no calibration has been performed the default volume is returned.

        :return:
        """
        response = self._send_and_receive(self._GET_CURRENT_ROLLER_STEP_VOLUME, pump_channel=pump_channel)
        # response is in the form mmmmEse; Represents the scientific notation of m.mmm x 10se.
        # units is nL
        # For example, 1.200 x 10-2 is represented with 1200E-2
        response = float(response)
        self.logger.debug(f'Roller step volume for pump channel {pump_channel}: {response} nL')
        return response

    def set_roller_step_volume(self, volume: str, pump_channel: int) -> str:
        """
        Set the calibrated roller step volume to use for this pump or channel. This value is used as the calibrated
        value and is overwritten by subsequent calibrations and reset by changing tubing diameter.

        :param str, volume: in the form m.mmmEse, which represents the scientific notation of m.mmm x 10se. For
            example, 1.200 x 10-2 is represented with 1.200E-2. Units is uL.
        :param pump_channel:
        :return:
        """
        if type(volume) != str:
            raise CommandError('Volume must be a string in the format m.mmmEse, which represents the scientific '
                               'notation of m.mmm x 10se. For example, 1.200 x 10-2 is represented with 1200E-2.')
        if len(volume) != 8:
            raise CommandError('Volume must be a string in the format m.mmmEse, which represents the scientific '
                               'notation of m.mmm x 10se. For example, 1.200 x 10-2 is represented with 1200E-2.')
        value = volume.replace('.', '')
        value = value.replace('E', '')
        response = self._send_and_receive(self._SET_CURRENT_ROLLER_STEP_VOLUME, value, pump_channel=pump_channel)
        self.logger.debug(f'Set roller step volume for pump channel {pump_channel}: {volume} uL')
        return response

    def reset_pump_clear_calibration_data(self) -> str:
        """
        Reset the pump to discard calibration data, use default roller step volume
        :return:
        """
        response = self._send_and_receive(self._RESET_PUMP_CLEAR_CALIBRATION_DATA)
        self.logger.debug(f'Reset the pump to discard calibration data, use default roller step volume')
        return response

    def get_pause_time(self, pump_channel: int) -> float:
        """Get the current setting for pause time in seconds"""
        response = self._send_and_receive(self._GET_CURRENT_PAUSE_TIME_SETTINGS_IN_TENTHS_S, pump_channel=pump_channel)  # returned
        # in 1/10 sec
        t = float(response) * 0.1
        self.logger.debug(f'Pump pause time for pump channel {pump_channel}: {t} seconds')
        return t

    def set_pause_time_s(self, t: float, pump_channel: int) -> str:
        """
        Set the pump pause time in seconds, between 0 and 999.9 seconds
        Command that gets sent to the pump can be sent as 0000-9999 1/10 sec

        :param float, t: pause time in seconds between 0 and 999.9 seconds
        """
        if type(t) != int or type(t) != float:
            try:
                t = float(t)
            except Exception:
                raise CommandError('Pause time must be an integer')
        if t > 999.9 or t < 0:
            raise CommandError('Pause time must be between 0 and 999.9 s')
        # convert to 1/10 sec
        t = int(t / 0.1)
        n_digits = 4
        t = str(t).zfill(n_digits)
        response = self._send_and_receive(self._SET_CURRENT_PAUSE_TIME_SETTINGS_IN_TENTHS_S, t, pump_channel=pump_channel)
        self.logger.debug(f'Set pause time for pump channel {pump_channel} to {int(t) * 0.1} seconds')
        return response

    def set_pause_time_m(self, t: int, pump_channel: int) -> str:
        """
        Set the pump pause time in minutes, between 0 and 999 minutes
        Command that gets sent to the pump can be sent as 000-999 minutes

        :param float, t: pause time in min between 0 and 999 minutes
        """
        if type(t) != int:
            try:
                t = int(t)
            except Exception:
                raise CommandError('Pause time must be an integer')
        if t > 999 or t < 0:
            raise CommandError('Pause time must be between 0 and 999')
        n_digits = 3
        t = str(t).zfill(n_digits)
        response = self._send_and_receive(self._SET_CURRENT_PAUSE_TIME_SETTINGS_IN_MINS, t, pump_channel=pump_channel)
        self.logger.debug(f'Set pause time for pump channel {pump_channel} to: {int(t)} minutes')
        return response

    def set_pause_time_h(self, t: int, pump_channel: int) -> str:
        """
        Set the pump pause time in hours, between 0 and 999 hours
        Command that gets sent to the pump can be sent as 000-999 hours

        :param float, t: pause time in hours between 0 and 999 hours
        """
        if type(t) != int:
            try:
                t = int(t)
            except Exception:
                raise CommandError('Pause time must be an integer')
        if t > 999 or t < 0:
            raise CommandError('Pause time must be between 0 and 999')
        n_digits = 3
        t = str(t).zfill(n_digits)
        # response is * if successful
        response = self._send_and_receive(self._SET_CURRENT_PAUSE_TIME_SETTINGS_IN_HOURS, t, pump_channel=pump_channel)
        self.logger.debug(f'Set pause time for pump channel {pump_channel} to: {int(t)} hours')
        return response

    def get_volume_dispensed_since_reset(self, pump_channel: int) -> float:
        """
        Get the total volume dispensed since the last reset in mL
        :return:
        """
        response = self._send_and_receive(self._GET_TOTAL_VOL_DISPENSED_SINCE_RESET)
        volume = float(response.split(' ')[0])
        units = response.split(' ')[1]
        if units == 'ul':
            volume = volume * 1000
        elif units == 'l':
            volume = volume / 1000
        self.logger.debug(f'Volume dispensed since last reset for pump channel {pump_channel}: {volume} mL')
        return volume

    def save_pump_settings(self) -> str:
        """Saves the current pump settings values to memory"""
        response = self._send_and_receive(self._SAVE_CURRENT_PUMP_SETTINGS_TO_MEMORY)
        self.logger.debug(f'Saved the current pump settings values to memory')
        return response

    def foot_switch_open(self) -> bool:
        """
        Get the current state of the foot switch
        :return: Return true if the foot switch is open, return false if it is grounded
        """
        response = self._send_and_receive(self._GET_FOOT_SWITCH_STATE)
        if response == self._SR_POSITIVE:
            switch_open = True
            state = 'open'
        else:
            switch_open = False
            state = 'grounded'
        self.logger.debug(f'Foot switch state: {state}')
        return switch_open

    # communications management commands
    def get_communication_mode(self) -> [1, 2]:
        response = int(self._send_and_receive(self._CHANNEL_ADDRESS_ENABLED))
        mode = 'pump_channel addressing' if response == 1 else 'legacy'
        self.logger.debug(f'Pump communication mode: {mode}')
        return response

    def set_channel_addressing_mode(self):
        response = self._send_and_receive(self._CHANNEL_ADDRESS_ENABLED, str(self._TRUE))
        self.logger.debug(f'Set pump communication mode: pump_channel addressing')
        return response

    def set_legacy_mode(self):
        response = self._send_and_receive(self._CHANNEL_ADDRESS_ENABLED, str(self._FALSE))
        self.logger.debug(f'Set pump communication mode: legacy')
        return response

    def get_event_messaging_mode(self) -> [0, 1]:
        response = int(self._send_and_receive(self._EVENT_MESSAGES_ENABLED))
        mode = 'on' if response == self._TRUE else 'off'
        self.logger.debug(f'Event messaging: {mode}')
        return response

    def enable_event_messaging(self):
        response = self._send_and_receive(self._EVENT_MESSAGES_ENABLED, str(self._TRUE))
        self.logger.debug(f'Enable event messaging')
        return response

    def disable_event_messaging(self):
        response = self._send_and_receive(self._EVENT_MESSAGES_ENABLED, str(self._FALSE))
        self.logger.debug(f'Disable event messaging')
        return response

    def get_serial_protocol_version(self) -> int:
        response = self._send_and_receive(self._SERIAL_PROTOCOL_VERSION)
        self.logger.debug(f'Serial protocol version: {response}')
        return int(response)

    # serial communication
    def _send_and_receive(self,
                          command: str,
                          parameter: str = None,
                          pump_channel: int = 1,
                          ) -> str:
        """
        Send a command, get a response back, and return the response.

        Setting the pump address has a different command format: @AddrCR
        from device commands: AddrCommand[param|param|...]CRLF
            In channel addressing mode the Addr is the pump channel, but in legacy mode it is the address of the pump

        :param str, command: the string command to send to the RegloCPF
        :param str, parameter: optional data parameter for the command. If a command takes more than one data
            parameter, format the parameter to be a single string with vertical bars separating each parameter for
            the command. If setting the pump address, this parameter is the new pump address
        :param int, pump_channel: address of a pump channel, 1-4. For commands that interact with parameters of a
            per-pump instead of a per-pump_channel basis, use a place holder value address of 0. However on testing,
            using a default value of 0 doesn't work but a value of 1 does

        :return:
        """
        if parameter is not None and type(parameter) != str:
            parameter = str(parameter)
        with self._lock:
            original_command = command
            # format the command if it should have the address in front of the command
            if command != self._SET_ADDRESS:
                if self.communication_mode == self._MODE_CHANNEL_ADDRESSING:
                    command: str = str(pump_channel) + command
                else:
                    command: str = str(self.pump_address) + command
            # format the command if it has some parameter
            if parameter is not None:
                command: str = command + str(parameter)
            # format the command to have the command line ending
            if original_command == self._SET_ADDRESS:
                command: str = command + self._SET_PUMP_ADDRESS_LINE_ENDING
            else:
                command: str = command + self._COMMAND_LINE_ENDING
            command_encoded = command.encode()

            self.ser.write(data=command_encoded)
            response = self._read()
            if response == self._SR_FAIL:
                raise CommandError(f"Command {original_command} with parameters {parameter} was not executed "
                                   f"successfully on pump channel/address {pump_channel}")
            if response.count(self._DATA_RESPONSE_LINE_ENDING) == 1:
                response = response.strip(self._DATA_RESPONSE_LINE_ENDING)
            return response

    def _read(self):
        time.sleep(0.055)
        num_bytes = self.ser.in_waiting
        # always read at least 1 byte, because that is the minimum response back from the pump
        bytes_to_read = num_bytes if num_bytes != 0 else 1
        data = self.ser.read(bytes_to_read)
        response = data.decode()
        return response












