import time
import logging
from ismatec.peristaltic_pump import RegloICC
from ismatec.errors import CommandError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    # connect to pump
    port = 'COM8'
    icc = RegloICC(port)

    # communications management
    icc.set_legacy_mode()
    icc.get_communication_mode()
    icc.set_channel_addressing_mode()
    icc.get_communication_mode()
    icc.enable_event_messaging()
    icc.get_event_messaging_mode()
    icc.disable_event_messaging()
    icc.get_event_messaging_mode()
    icc.get_serial_protocol_version()

    # system
    icc.get_pump_firmware_version()
    icc.save_set_roller_step_settings()
    icc.reset_roller_step_volume()
    original_serial_number = icc.get_pump_serial_number()
    new_serial_number = 'A123456789'
    icc.set_pump_serial_number(new_serial_number)
    icc.set_pump_serial_number(original_serial_number)
    original_language = icc.get_pump_language()
    for i in range(4):
        icc.set_pump_language(i)
        time.sleep(0.1)
    icc.set_pump_language(original_language)
    n_pump_channels = icc.get_n_pump_channels()
    icc.set_n_pump_channels(n_pump_channels)
    for i in range(n_pump_channels):
        channel = i + 1
        n_rollers = icc.get_n_rollers_for_channel(channel)
        icc.set_n_rollers_for_channel(channel, n_rollers)
        icc.get_n_revolutions_since_reset(channel)
        icc.get_volume_pumped_since_reset(channel)
        icc.get_time_pumped_since_reset(channel)

        dispensing_time_s = icc.get_dispensing_time(channel)
        icc.set_dispensing_time_m(10, channel)
        icc.get_dispensing_time(channel)
        icc.set_dispensing_time_h(10, channel)
        icc.get_dispensing_time(channel)
        icc.set_dispensing_time_s(dispensing_time_s, channel)
        icc.get_dispensing_time(channel)

        roller_step_volume = icc.get_roller_step_volume(channel)
        time.sleep(0.1)  # sleep time added to give time to communicate with the pump
        icc.set_roller_step_volume('7.900E+1', pump_channel=channel)
        time.sleep(0.1)
        if icc.get_roller_step_volume(channel) != 79000.0:
            raise Exception('Failed to set roller step volume')
        time.sleep(0.1)
        icc.set_roller_step_volume('7.700E+1', pump_channel=channel)
        time.sleep(0.1)
        icc.get_roller_step_volume(channel)
        time.sleep(0.1)

        pause_time_s = icc.get_pause_time(channel)
        icc.set_pause_time_m(10, channel)
        icc.get_pause_time(channel)
        icc.set_pause_time_h(10, channel)
        icc.get_pause_time(channel)
        icc.set_pause_time_s(pause_time_s, channel)
        icc.get_pause_time(channel)

        icc.get_volume_dispensed_since_reset(channel)

    icc.disable_pump_ui()
    icc.set_pump_name('Lucky ICC')
    icc.write_to_display("Write to pump")
    icc.write_to_display("Write 12.3")
    icc.write_to_display(12.3)
    icc.set_control_from_pump_ui()
    icc.get_pump_info()
    model_type_code = icc.get_pump_head_model_type_code()
    # icc.set_pump_head_model_type_code(model_type_code)  # todo not sure why it isnt working

    low_order_roller_steps = icc.get_low_order_roller_steps()
    icc.set_low_order_roller_steps(100)
    icc.get_low_order_roller_steps()
    icc.set_low_order_roller_steps(low_order_roller_steps)
    icc.get_low_order_roller_steps()
    high_order_roller_steps = icc.get_high_order_roller_steps()
    icc.set_high_order_roller_steps(100)
    icc.get_high_order_roller_steps()
    icc.set_high_order_roller_steps(high_order_roller_steps)
    icc.get_high_order_roller_steps()
    try:
        icc.set_low_order_roller_steps(100000)
    except CommandError as e:
        logger.debug('Successfully caught setting low order roller steps to a too high value')
    try:
        icc.set_high_order_roller_steps(100000)
    except CommandError as e:
        logger.debug('Successfully caught setting high order roller steps to a too high value')

    icc.reset_pump_clear_calibration_data()
    icc.save_pump_settings()
    icc.foot_switch_open()

    # operational modes and settings and pump drive
    error_code, error_value = icc.get_cause_of_run_error()

    for m in RegloICC._PUMP_MODES:
        icc.set_pump_mode(m, pump_channel=1)
        icc.get_pump_mode(pump_channel=1)
        icc.get_max_flow_rate(1)
        icc.get_max_flow_rate_using_calibration(1)

    n_pump_channels = icc.get_n_pump_channels()
    for i in range(n_pump_channels):
        channel = i + 1

        icc.set_counter_clockwise(channel)
        if icc.clockwise(channel) is True:
            raise Exception('Unsuccessfully set rotation direction counter-clockwise')
        icc.set_clockwise(channel)
        if icc.clockwise(channel) is False:
            raise Exception('Unsuccessfully set rotation direction clockwise')

        for mode in [RegloICC._MODE_RPM]:
            icc.set_pump_mode(mode, channel)
            icc.set_flow_rate_rpm(0, channel)
            if icc.get_flow_rate_rpm(channel) != 0:
                raise Exception('Failed to set pump rpm speed to 0 rpm')
            icc.set_flow_rate_rpm(1, channel)
            if icc.get_flow_rate_rpm(channel) != 1:
                raise Exception('Failed to set pump rpm speed to 1 rpm')

        for mode in [RegloICC._MODE_FLOW_RATE, RegloICC._MODE_VOLUME_AND_PAUSE,
                     RegloICC._MODE_VOLUME_AT_RATE, RegloICC._MODE_TIME_AND_PAUSE, RegloICC._MODE_TIME, ]:
            icc.set_pump_mode(mode, channel)
            icc.get_flow_rate_ml_min(channel)
            icc.set_flow_rate_ml_min('5.000E-2', channel)
            if icc.get_flow_rate_ml_min(channel) != 0.05:
                raise Exception('Failed to set pump volume or time flow rate to 0.05 mL/min')
            icc.set_flow_rate_ml_min('7.000E-2', channel)
            if icc.get_flow_rate_ml_min(channel) != 0.07:
                raise Exception('Failed to set pump volume or time flow rate to 0.07 mL/min')

        for mode in [RegloICC._MODE_VOLUME_AT_RATE, RegloICC._MODE_VOLUME_OVER_TIME, RegloICC._MODE_VOLUME_AND_PAUSE]:
            icc.set_pump_mode(mode, channel)
            icc.get_volume(channel)
            icc.set_volume('5.000E-2', channel)
            if icc.get_volume(channel) != 0.05:
                raise Exception('Failed to set pump volume 0.05 mL')
            icc.set_volume('7.000E-2', channel)
            if icc.get_volume(channel) != 0.07:
                raise Exception('Failed to set pump volume 0.07 mL')

        for mode in [RegloICC._MODE_VOLUME_OVER_TIME, RegloICC._MODE_TIME, RegloICC._MODE_TIME_AND_PAUSE]:
            icc.set_pump_mode(mode, channel)
            icc.get_run_time(channel)
            icc.set_run_time(15, channel)
            if icc.get_run_time(channel) != 15:
                raise Exception('Failed to set pump time to 15 seconds')
            icc.set_run_time(3, channel)
            if icc.get_run_time(channel) != 3:
                raise Exception('Failed to set pump time to 3 seconds')

        for mode in [RegloICC._MODE_VOLUME_AND_PAUSE, RegloICC._MODE_TIME_AND_PAUSE]:
            icc.set_pump_mode(mode, channel)
            icc.get_pumping_pause_time(channel)
            icc.set_pumping_pause_time(15, channel)
            if icc.get_pumping_pause_time(channel) != 15:
                raise Exception('Failed to set pause time to 15 seconds')
            icc.set_pumping_pause_time(3, channel)
            if icc.get_pumping_pause_time(channel) != 3:
                raise Exception('Failed to set pause time to 3 seconds')

        for mode in [RegloICC._MODE_VOLUME_AND_PAUSE, RegloICC._MODE_TIME_AND_PAUSE]:
            icc.set_pump_mode(mode, channel)
            icc.get_cycle_count(channel)
            icc.set_cycle_count(15, channel)
            if icc.get_cycle_count(channel) != 15:
                raise Exception('Failed to set cycle count to 15')
            icc.set_cycle_count(0, channel)
            if icc.get_cycle_count(channel) != 0:
                raise Exception('Failed to set cycle count to 0')

        icc.set_mode_pump_rpm(pump_channel=channel, rpm=1)
        icc.running(channel)
        icc.start(channel)
        icc.running(channel)
        time.sleep(1)
        icc.start(channel)
        icc.pause(channel)
        icc.running(channel)
        time.sleep(1)
        icc.start(channel)
        icc.running(channel)
        time.sleep(1)
        icc.stop(channel)
        icc.running(channel)
        icc.set_mode_pump_rpm(pump_channel=channel, rpm=0)

    # configuration and calibration
    n_pump_channels = icc.get_n_pump_channels()
    for i in range(n_pump_channels):
        channel = i + 1

        diameter = icc.get_tubing_inner_diameter(channel)
        icc.set_tubing_inner_diameter(3.17, channel)
        if icc.get_tubing_inner_diameter(channel) != 3.17:
            raise Exception("Failed to set tubing inner diameter")
        icc.set_tubing_inner_diameter(diameter, channel)
        if icc.get_tubing_inner_diameter(channel) != diameter:
            raise Exception("Failed to set tubing inner diameter")

        backsteps = icc.get_backsteps_setting(channel)
        icc.set_backsteps_setting(1, channel)
        if icc.get_backsteps_setting(channel) != 1:
            raise Exception("Failed to set backsteps setting")
        icc.set_backsteps_setting(backsteps, channel)
        if icc.get_backsteps_setting(channel) != backsteps:
            raise Exception("Failed to set backsteps setting")

        icc.set_calibration_direction_clockwise(channel)
        if icc.calibration_direction_clockwise(channel) is False:
            raise Exception("Failed to set calibration direction")
        icc.set_calibration_direction_counter_clockwise(channel)
        if icc.calibration_direction_clockwise(channel):
            raise Exception("Failed to set calibration direction")

        icc.get_target_calibration_volume(channel)
        icc.set_target_calibration_volume('5.000E-0', channel)
        if icc.get_target_calibration_volume(channel) != 5:
            raise Exception("Failed to set target calibration volume")
        icc.set_target_calibration_volume('0.000E-0', channel)
        if icc.get_target_calibration_volume(channel) != 0:
            raise Exception("Failed to set target calibration volume")

        calibration_time = icc.get_calibration_time(channel)
        icc.set_calibration_time(10.5, channel)
        if icc.get_calibration_time(channel) != 10.5:
            raise Exception("Failed to set calibration time")
        icc.set_calibration_time(calibration_time, channel)
        if icc.get_calibration_time(channel) != calibration_time:
            raise Exception("Failed to set calibration time")

        icc.get_run_time_since_last_calibration(channel)

        # numbers picked for sleep time assume it takes 10 seconds to do the calibration
        icc.set_mode_pump_rpm(channel, 5)
        icc.set_target_calibration_volume('1.000E-2', channel)
        icc.set_calibration_time(10, channel)
        icc.start_calibration(channel)
        time.sleep(3)
        icc.cancel_calibration(channel)
        time.sleep(1)
        icc.start_calibration(channel)
        time.sleep(12)
        icc.set_actual_calibration_volume('1.020E-2', channel)
        # icc.get_actual_calibration_volume(channel)  # todo not sure why this doesnt work

    icc.reset_configurable_data_to_default()

    icc.disconnect()
