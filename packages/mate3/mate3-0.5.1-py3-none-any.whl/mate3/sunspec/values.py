"""This file is auto generated, do not edit. The generation code can be found in code_generator.py"""

from dataclasses import dataclass

from mate3.field_values import FieldValue, ModelValues
from mate3.sunspec import models


@dataclass
class SunSpecHeaderValues(ModelValues):
    did: FieldValue
    model_id: FieldValue
    length: FieldValue
    manufacturer: FieldValue
    model: FieldValue
    options: FieldValue
    version: FieldValue
    serial_number: FieldValue


@dataclass
class SunSpecEndValues(ModelValues):
    did: FieldValue
    length: FieldValue


@dataclass
class SunSpecCommonValues(ModelValues):
    did: FieldValue
    length: FieldValue
    manufacturer: FieldValue
    model: FieldValue
    options: FieldValue
    version: FieldValue
    serial_number: FieldValue
    device_address: FieldValue


@dataclass
class SunSpecInverterSinglePhaseValues(ModelValues):
    did: FieldValue
    length: FieldValue
    ac_current: FieldValue
    ac_current_a: FieldValue
    ac_current_b: FieldValue
    ac_current_c: FieldValue
    ac_current_scale_factor: FieldValue
    ac_voltage_ab: FieldValue
    ac_voltage_bc: FieldValue
    ac_voltage_ca: FieldValue
    ac_voltage_an: FieldValue
    ac_voltage_bn: FieldValue
    ac_voltage_cn: FieldValue
    ac_voltage_scale_factor: FieldValue
    ac_power: FieldValue
    ac_power_scale_factor: FieldValue
    ac_frequency: FieldValue
    ac_frequency_scale_factor: FieldValue
    ac_va: FieldValue
    ac_va_scale_factor: FieldValue
    ac_var: FieldValue
    ac_var_scale_factor: FieldValue
    ac_pf: FieldValue
    ac_pf_scale_factor: FieldValue
    ac_energy_wh: FieldValue
    ac_energy_wh_scale_factor: FieldValue
    dc_current: FieldValue
    dc_current_scale_factor: FieldValue
    dc_voltage: FieldValue
    dc_voltage_scale_factor: FieldValue
    dc_power: FieldValue
    dc_power_scale_factor: FieldValue
    temp_cab: FieldValue
    temp_sink: FieldValue
    temp_trans: FieldValue
    temp_other: FieldValue
    temp_scale_factor: FieldValue
    status: FieldValue
    status_vendor: FieldValue
    event_1: FieldValue
    event_2: FieldValue
    event_1_vendor: FieldValue
    event_2_vendor: FieldValue
    event_3_vendor: FieldValue
    event_4_vendor: FieldValue


@dataclass
class SunSpecInverterSplitPhaseValues(ModelValues):
    did: FieldValue
    length: FieldValue
    ac_current: FieldValue
    ac_current_a: FieldValue
    ac_current_b: FieldValue
    ac_current_c: FieldValue
    ac_current_scale_factor: FieldValue
    ac_voltage_ab: FieldValue
    ac_voltage_bc: FieldValue
    ac_voltage_ca: FieldValue
    ac_voltage_an: FieldValue
    ac_voltage_bn: FieldValue
    ac_voltage_cn: FieldValue
    ac_voltage_scale_factor: FieldValue
    ac_power: FieldValue
    ac_power_scale_factor: FieldValue
    ac_frequency: FieldValue
    ac_frequency_scale_factor: FieldValue
    ac_va: FieldValue
    ac_va_scale_factor: FieldValue
    ac_var: FieldValue
    ac_var_scale_factor: FieldValue
    ac_pf: FieldValue
    ac_pf_scale_factor: FieldValue
    ac_energy_wh: FieldValue
    ac_energy_wh_scale_factor: FieldValue
    dc_current: FieldValue
    dc_current_scale_factor: FieldValue
    dc_voltage: FieldValue
    dc_voltage_scale_factor: FieldValue
    dc_power: FieldValue
    dc_power_scale_factor: FieldValue
    temp_cab: FieldValue
    temp_sink: FieldValue
    temp_trans: FieldValue
    temp_other: FieldValue
    temp_scale_factor: FieldValue
    status: FieldValue
    status_vendor: FieldValue
    event_1: FieldValue
    event_2: FieldValue
    event_1_vendor: FieldValue
    event_2_vendor: FieldValue
    event_3_vendor: FieldValue
    event_4_vendor: FieldValue


@dataclass
class SunSpecInverterThreePhaseValues(ModelValues):
    did: FieldValue
    length: FieldValue
    ac_current: FieldValue
    ac_current_a: FieldValue
    ac_current_b: FieldValue
    ac_current_c: FieldValue
    ac_current_scale_factor: FieldValue
    ac_voltage_ab: FieldValue
    ac_voltage_bc: FieldValue
    ac_voltage_ca: FieldValue
    ac_voltage_an: FieldValue
    ac_voltage_bn: FieldValue
    ac_voltage_cn: FieldValue
    ac_voltage_scale_factor: FieldValue
    ac_power: FieldValue
    ac_power_scale_factor: FieldValue
    ac_frequency: FieldValue
    ac_frequency_scale_factor: FieldValue
    ac_va: FieldValue
    ac_va_scale_factor: FieldValue
    ac_var: FieldValue
    ac_var_scale_factor: FieldValue
    ac_pf: FieldValue
    ac_pf_scale_factor: FieldValue
    ac_energy_wh: FieldValue
    ac_energy_wh_scale_factor: FieldValue
    dc_current: FieldValue
    dc_current_scale_factor: FieldValue
    dc_voltage: FieldValue
    dc_voltage_scale_factor: FieldValue
    dc_power: FieldValue
    dc_power_scale_factor: FieldValue
    temp_cab: FieldValue
    temp_sink: FieldValue
    temp_trans: FieldValue
    temp_other: FieldValue
    temp_scale_factor: FieldValue
    status: FieldValue
    status_vendor: FieldValue
    event_1: FieldValue
    event_2: FieldValue
    event_1_vendor: FieldValue
    event_2_vendor: FieldValue
    event_3_vendor: FieldValue
    event_4_vendor: FieldValue


@dataclass
class OutBackValues(ModelValues):
    did: FieldValue
    length: FieldValue
    major_firmware_number: FieldValue
    mid_firmware_number: FieldValue
    minor_firmware_number: FieldValue
    encryption_key: FieldValue
    mac_address: FieldValue
    write_password: FieldValue
    enable_dhcp: FieldValue
    tcpip_address: FieldValue
    tcpip_gateway_msw: FieldValue
    tcpip_netmask_msw: FieldValue
    tcpip_dns_1_msw: FieldValue
    tcpip_dns_2_msw: FieldValue
    modbus_port: FieldValue
    smtp_server_name: FieldValue
    smtp_account_name: FieldValue
    smtp_ssl_enable: FieldValue
    smtp_email_password: FieldValue
    smtp_email_user_name: FieldValue
    status_email_interval: FieldValue
    status_email_status_time: FieldValue
    status_email_subject_line: FieldValue
    status_email_to_address_1: FieldValue
    status_email_to_address_2: FieldValue
    alarm_email_enable: FieldValue
    system_name: FieldValue
    alarm_email_to_address_1: FieldValue
    alarm_email_to_address_2: FieldValue
    ftp_password: FieldValue
    telnet_password: FieldValue
    sd_card_data_log_write_interval: FieldValue
    sd_card_data_log_retain_days: FieldValue
    sd_card_data_logging_mode: FieldValue
    time_server_name: FieldValue
    enable_time_server: FieldValue
    set_time_zone: FieldValue
    enable_float_coordination: FieldValue
    enable_fndc_charge_termination: FieldValue
    enable_fndc_grid_tie_control: FieldValue
    voltage_scale_factor: FieldValue
    hour_scale_factor: FieldValue
    ags_mode: FieldValue
    ags_port: FieldValue
    ags_port_type: FieldValue
    ags_generator_type: FieldValue
    ags_dc_gen_absorb_voltage: FieldValue
    ags_dc_gen_absorb_time: FieldValue
    ags_fault_time: FieldValue
    ags_gen_cool_down_time: FieldValue
    ags_gen_warm_up_time: FieldValue
    ags_generator_exercise_mode: FieldValue
    ags_exercise_start_hour: FieldValue
    ags_exercise_start_minute: FieldValue
    ags_exercise_day: FieldValue
    ags_exercise_period: FieldValue
    ags_exercise_interval: FieldValue
    ags_sell_mode: FieldValue
    ags_2_min_start_mode: FieldValue
    ags_2_min_start_voltage: FieldValue
    ags_2_hour_start_mode: FieldValue
    ags_2_hour_start_voltage: FieldValue
    ags_24_hour_start_mode: FieldValue
    ags_24_hour_start_voltage: FieldValue
    ags_load_start_mode: FieldValue
    ags_load_start_kw: FieldValue
    ags_load_start_delay: FieldValue
    ags_load_stop_kw: FieldValue
    ags_load_stop_delay: FieldValue
    ags_soc_start_mode: FieldValue
    ags_soc_start_percentage: FieldValue
    ags_soc_stop_percentage: FieldValue
    ags_enable_full_charge_mode: FieldValue
    ags_full_charge_interval: FieldValue
    ags_must_run_mode: FieldValue
    ags_must_run_weekday_start_hour: FieldValue
    ags_must_run_weekday_start_minute: FieldValue
    ags_must_run_weekday_stop_hour: FieldValue
    ags_must_run_weekday_stop_minute: FieldValue
    ags_must_run_weekend_start_hour: FieldValue
    ags_must_run_weekend_start_minute: FieldValue
    ags_must_run_weekend_stop_hour: FieldValue
    ags_must_run_weekend_stop_minute: FieldValue
    ags_quiet_time_mode: FieldValue
    ags_quiet_time_weekday_start_hour: FieldValue
    ags_quiet_time_weekday_start_minute: FieldValue
    ags_quiet_time_weekday_stop_hour: FieldValue
    ags_quiet_time_weekday_stop_minute: FieldValue
    ags_quiet_time_weekend_start_hour: FieldValue
    ags_quiet_time_weekend_start_minute: FieldValue
    ags_quiet_time_weekend_stop_hour: FieldValue
    ags_quiet_time_weekend_stop_minute: FieldValue
    ags_total_generator_run_time: FieldValue
    hbx_mode: FieldValue
    hbx_grid_connect_voltage: FieldValue
    hbx_grid_connect_delay: FieldValue
    hbx_grid_disconnect_voltage: FieldValue
    hbx_grid_disconnect_delay: FieldValue
    hbx_grid_connect_soc: FieldValue
    hbx_grid_disconnect_soc: FieldValue
    grid_use_interval_1_mode: FieldValue
    grid_use_interval_1_weekday_start_hour: FieldValue
    grid_use_interval_1_weekday_start_minute: FieldValue
    grid_use_interval_1_weekday_stop_hour: FieldValue
    grid_use_interval_1_weekday_stop_minute: FieldValue
    grid_use_interval_1_weekend_start_hour: FieldValue
    grid_use_interval_1_weekend_start_minute: FieldValue
    grid_use_interval_1_weekend_stop_hour: FieldValue
    grid_use_interval_1_weekend_stop_minute: FieldValue
    grid_use_interval_2_mode: FieldValue
    grid_use_interval_2_weekday_start_hour: FieldValue
    grid_use_interval_2_weekday_start_minute: FieldValue
    grid_use_interval_2_weekday_stop_hour: FieldValue
    grid_use_interval_2_weekday_stop_minute: FieldValue
    grid_use_interval_3_mode: FieldValue
    grid_use_interval_3_weekday_start_hour: FieldValue
    grid_use_interval_3_weekday_start_minute: FieldValue
    grid_use_interval_3_weekday_stop_hour: FieldValue
    grid_use_interval_3_weekday_stop_minute: FieldValue
    load_grid_transfer_mode: FieldValue
    load_grid_transfer_threshold: FieldValue
    load_grid_transfer_connect_delay: FieldValue
    load_grid_transfer_disconnect_delay: FieldValue
    load_grid_transfer_connect_battery_voltage: FieldValue
    load_grid_transfer_re_connect_battery_voltage: FieldValue
    global_charger_control_mode: FieldValue
    global_charger_control_output_limit: FieldValue
    radian_ac_coupled_control_mode: FieldValue
    radian_ac_coupled_aux_port: FieldValue
    url_update_lock: FieldValue
    web_reporting_base_url: FieldValue
    web_user_logged_in_status: FieldValue
    hub_type: FieldValue
    hub_major_firmware_number: FieldValue
    hub_mid_firmware_number: FieldValue
    hub_minor_firmware_number: FieldValue
    year: FieldValue
    month: FieldValue
    day: FieldValue
    hour: FieldValue
    minute: FieldValue
    second: FieldValue
    temp_battery: FieldValue
    temp_ambient: FieldValue
    temp_scale_factor: FieldValue
    error: FieldValue
    status: FieldValue
    update_device_firmware_port: FieldValue
    gateway_type: FieldValue
    system_voltage: FieldValue
    measured_system_voltage: FieldValue
    ags_ac_reconnect_delay: FieldValue
    multi_phase_coordination: FieldValue
    sched_1_ac_mode: FieldValue
    sched_1_ac_mode_hour: FieldValue
    sched_1_ac_mode_minute: FieldValue
    sched_2_ac_mode: FieldValue
    sched_2_ac_mode_hour: FieldValue
    sched_2_ac_mode_minute: FieldValue
    sched_3_ac_mode: FieldValue
    sched_3_ac_mode_hour: FieldValue
    sched_3_ac_mode_minute: FieldValue
    auto_reboot: FieldValue
    time_zone_scale_factor: FieldValue
    spare_reg_3: FieldValue
    spare_reg_4: FieldValue


@dataclass
class ChargeControllerValues(ModelValues):
    did: FieldValue
    length: FieldValue
    port_number: FieldValue
    voltage_scale_factor: FieldValue
    current_scale_factor: FieldValue
    power_scale_factor: FieldValue
    ah_scale_factor: FieldValue
    kwh_scale_factor: FieldValue
    battery_voltage: FieldValue
    array_voltage: FieldValue
    battery_current: FieldValue
    array_current: FieldValue
    charger_state: FieldValue
    watts: FieldValue
    todays_min_battery_volts: FieldValue
    todays_max_battery_volts: FieldValue
    voc: FieldValue
    todays_peak_voc: FieldValue
    todays_kwh: FieldValue
    todays_ah: FieldValue
    lifetime_kwh_hours: FieldValue
    lifetime_k_amp_hours: FieldValue
    lifetime_max_watts: FieldValue
    lifetime_max_battery_volts: FieldValue
    lifetime_max_voc: FieldValue
    temp_scale_factor: FieldValue
    temp_output_fets: FieldValue
    temp_enclosure: FieldValue


@dataclass
class ChargeControllerConfigurationValues(ModelValues):
    did: FieldValue
    length: FieldValue
    port_number: FieldValue
    voltage_scale_factor: FieldValue
    current_scale_factor: FieldValue
    hours_scale_factor: FieldValue
    power_scale_factor: FieldValue
    ah_scale_factor: FieldValue
    kwh_scale_factor: FieldValue
    faults: FieldValue
    absorb_volts: FieldValue
    absorb_time_hours: FieldValue
    absorb_end_amps: FieldValue
    rebulk_volts: FieldValue
    float_volts: FieldValue
    bulk_current: FieldValue
    eq_volts: FieldValue
    eq_time_hours: FieldValue
    auto_eq_days: FieldValue
    mppt_mode: FieldValue
    sweep_width: FieldValue
    sweep_max_percentage: FieldValue
    u_pick_pwm_duty_cycle: FieldValue
    grid_tie_mode: FieldValue
    temp_comp_mode: FieldValue
    temp_comp_lower_limit_volts: FieldValue
    temp_comp_upper_limit_volts: FieldValue
    temp_comp_slope: FieldValue
    auto_restart_mode: FieldValue
    wakeup_voc: FieldValue
    snooze_mode_amps: FieldValue
    wakeup_interval: FieldValue
    aux_mode: FieldValue
    aux_control: FieldValue
    aux_state: FieldValue
    aux_polarity: FieldValue
    aux_low_battery_disconnect: FieldValue
    aux_low_battery_reconnect: FieldValue
    aux_low_battery_disconnect_delay: FieldValue
    aux_vent_fan_volts: FieldValue
    aux_pv_limit_volts: FieldValue
    aux_pv_limit_hold_time: FieldValue
    aux_night_light_thres_volts: FieldValue
    night_light_on_hours: FieldValue
    night_light_on_hyst_time: FieldValue
    night_light_off_hyst_time: FieldValue
    aux_error_battery_volts: FieldValue
    aux_divert_hold_time: FieldValue
    aux_divert_delay_time: FieldValue
    aux_divert_relative_volts: FieldValue
    aux_divert_hyst_volts: FieldValue
    major_firmware_number: FieldValue
    mid_firmware_number: FieldValue
    minor_firmware_number: FieldValue
    set_data_log_day_offset: FieldValue
    get_current_data_log_day_offset: FieldValue
    data_log_daily_ah: FieldValue
    data_log_daily_kwh: FieldValue
    data_log_daily_max_output_amps: FieldValue
    data_log_daily_max_output_watts: FieldValue
    data_log_daily_absorb_time: FieldValue
    data_log_daily_float_time: FieldValue
    data_log_daily_min_battery_volts: FieldValue
    data_log_daily_max_battery_volts: FieldValue
    data_log_daily_max_input_volts: FieldValue
    clear_data_log_read: FieldValue
    clear_data_log_write_complement: FieldValue
    stats_maximum_reset_read: FieldValue
    stats_maximum_write_complement: FieldValue
    stats_totals_reset_read: FieldValue
    stats_totals_write_complement: FieldValue
    battery_voltage_calibrate_offset: FieldValue
    serial_number: FieldValue
    model_number: FieldValue


@dataclass
class FXInverterRealTimeValues(ModelValues):
    did: FieldValue
    length: FieldValue
    port_number: FieldValue
    dc_voltage_scale_factor: FieldValue
    ac_current_scale_factor: FieldValue
    ac_voltage_scale_factor: FieldValue
    ac_frequency_scale_factor: FieldValue
    inverter_output_current: FieldValue
    inverter_charge_current: FieldValue
    inverter_buy_current: FieldValue
    inverter_sell_current: FieldValue
    output_ac_voltage: FieldValue
    inverter_operating_mode: FieldValue
    error_flags: FieldValue
    warning_flags: FieldValue
    battery_voltage: FieldValue
    temp_compensated_target_voltage: FieldValue
    aux_output_state: FieldValue
    transformer_temperature: FieldValue
    capacitor_temperature: FieldValue
    fet_temperature: FieldValue
    ac_input_frequency: FieldValue
    ac_input_voltage: FieldValue
    ac_input_state: FieldValue
    minimum_ac_input_voltage: FieldValue
    maximum_ac_input_voltage: FieldValue
    sell_status: FieldValue
    kwh_scale_factor: FieldValue
    buy_kwh: FieldValue
    sell_kwh: FieldValue
    output_kwh: FieldValue
    charger_kwh: FieldValue
    output_kw: FieldValue
    buy_kw: FieldValue
    sell_kw: FieldValue
    charge_kw: FieldValue
    load_kw: FieldValue
    ac_couple_kw: FieldValue


@dataclass
class FXInverterConfigurationValues(ModelValues):
    did: FieldValue
    length: FieldValue
    port_number: FieldValue
    dc_voltage_scale_factor: FieldValue
    ac_current_scale_factor: FieldValue
    ac_voltage_scale_factor: FieldValue
    time_scale_factor: FieldValue
    major_firmware_number: FieldValue
    mid_firmware_number: FieldValue
    minor_firmware_number: FieldValue
    absorb_volts: FieldValue
    absorb_time_hours: FieldValue
    float_volts: FieldValue
    float_time_hours: FieldValue
    re_float_volts: FieldValue
    eq_volts: FieldValue
    eq_time_hours: FieldValue
    search_sensitivity: FieldValue
    search_pulse_length: FieldValue
    search_pulse_spacing: FieldValue
    ac_input_type: FieldValue
    input_support: FieldValue
    grid_ac_input_current_limit: FieldValue
    gen_ac_input_current_limit: FieldValue
    charger_ac_input_current_limit: FieldValue
    charger_operating_mode: FieldValue
    grid_lower_input_voltage_limit: FieldValue
    grid_upper_input_voltage_limit: FieldValue
    grid_transfer_delay: FieldValue
    gen_lower_input_voltage_limit: FieldValue
    gen_upper_input_voltage_limit: FieldValue
    gen_transfer_delay: FieldValue
    gen_connect_delay: FieldValue
    ac_output_voltage: FieldValue
    low_battery_cut_out_voltage: FieldValue
    low_battery_cut_in_voltage: FieldValue
    aux_mode: FieldValue
    aux_control: FieldValue
    aux_load_shed_enable_voltage: FieldValue
    aux_gen_alert_on_voltage: FieldValue
    aux_gen_alert_on_delay: FieldValue
    aux_gen_alert_off_voltage: FieldValue
    aux_gen_alert_off_delay: FieldValue
    aux_vent_fan_enable_voltage: FieldValue
    aux_vent_fan_off_period: FieldValue
    aux_divert_enable_voltage: FieldValue
    aux_divert_off_delay: FieldValue
    stacking_mode: FieldValue
    master_power_save_level: FieldValue
    slave_power_save_level: FieldValue
    sell_volts: FieldValue
    grid_tie_window: FieldValue
    grid_tie_enable: FieldValue
    ac_input_voltage_calibrate_factor: FieldValue
    ac_output_voltage_calibrate_factor: FieldValue
    battery_voltage_calibrate_factor: FieldValue
    serial_number: FieldValue
    model_number: FieldValue


@dataclass
class SplitPhaseRadianInverterRealTimeValues(ModelValues):
    did: FieldValue
    length: FieldValue
    port_number: FieldValue
    dc_voltage_scale_factor: FieldValue
    ac_current_scale_factor: FieldValue
    ac_voltage_scale_factor: FieldValue
    ac_frequency_scale_factor: FieldValue
    l1_inverter_output_current: FieldValue
    l1_inverter_charge_current: FieldValue
    l1_inverter_buy_current: FieldValue
    l1_inverter_sell_current: FieldValue
    l1_grid_input_ac_voltage: FieldValue
    l1_gen_input_ac_voltage: FieldValue
    l1_output_ac_voltage: FieldValue
    l2_inverter_output_current: FieldValue
    l2_inverter_charge_current: FieldValue
    l2_inverter_buy_current: FieldValue
    l2_inverter_sell_current: FieldValue
    l2_grid_input_ac_voltage: FieldValue
    l2_gen_input_ac_voltage: FieldValue
    l2_output_ac_voltage: FieldValue
    inverter_operating_mode: FieldValue
    error_flags: FieldValue
    warning_flags: FieldValue
    battery_voltage: FieldValue
    temp_compensated_target_voltage: FieldValue
    aux_output_state: FieldValue
    aux_relay_output_state: FieldValue
    l_module_transformer_temperature: FieldValue
    l_module_capacitor_temperature: FieldValue
    l_module_fet_temperature: FieldValue
    r_module_transformer_temperature: FieldValue
    r_module_capacitor_temperature: FieldValue
    r_module_fet_temperature: FieldValue
    battery_temperature: FieldValue
    ac_input_selection: FieldValue
    ac_input_frequency: FieldValue
    ac_input_voltage: FieldValue
    ac_input_state: FieldValue
    minimum_ac_input_voltage: FieldValue
    maximum_ac_input_voltage: FieldValue
    sell_status: FieldValue
    kwh_scale_factor: FieldValue
    ac1_l1_buy_kwh: FieldValue
    ac2_l1_buy_kwh: FieldValue
    ac1_l1_sell_kwh: FieldValue
    ac2_l1_sell_kwh: FieldValue
    l1_output_kwh: FieldValue
    ac1_l2_buy_kwh: FieldValue
    ac2_l2_buy_kwh: FieldValue
    ac1_l2_sell_kwh: FieldValue
    ac2_l2_sell_kwh: FieldValue
    l2_output_kwh: FieldValue
    charger_kwh: FieldValue
    output_kw: FieldValue
    buy_kw: FieldValue
    sell_kw: FieldValue
    charge_kw: FieldValue
    load_kw: FieldValue
    ac_couple_kw: FieldValue
    gt_number: FieldValue


@dataclass
class RadianInverterConfigurationValues(ModelValues):
    did: FieldValue
    length: FieldValue
    port_number: FieldValue
    dc_voltage_scale_factor: FieldValue
    ac_current_scale_factor: FieldValue
    ac_voltage_scale_factor: FieldValue
    time_scale_factor: FieldValue
    major_firmware_number: FieldValue
    mid_firmware_number: FieldValue
    minor_firmware_number: FieldValue
    absorb_volts: FieldValue
    absorb_time_hours: FieldValue
    float_volts: FieldValue
    float_time_hours: FieldValue
    re_float_volts: FieldValue
    eq_volts: FieldValue
    eq_time_hours: FieldValue
    search_sensitivity: FieldValue
    search_pulse_length: FieldValue
    search_pulse_spacing: FieldValue
    ac_input_select_priority: FieldValue
    grid_ac_input_current_limit: FieldValue
    gen_ac_input_current_limit: FieldValue
    charger_ac_input_current_limit: FieldValue
    charger_operating_mode: FieldValue
    ac_coupled: FieldValue
    grid_input_mode: FieldValue
    grid_lower_input_voltage_limit: FieldValue
    grid_upper_input_voltage_limit: FieldValue
    grid_transfer_delay: FieldValue
    grid_connect_delay: FieldValue
    gen_input_mode: FieldValue
    gen_lower_input_voltage_limit: FieldValue
    gen_upper_input_voltage_limit: FieldValue
    gen_transfer_delay: FieldValue
    gen_connect_delay: FieldValue
    ac_output_voltage: FieldValue
    low_battery_cut_out_voltage: FieldValue
    low_battery_cut_in_voltage: FieldValue
    aux_mode: FieldValue
    aux_control: FieldValue
    aux_on_battery_voltage: FieldValue
    aux_on_delay_time: FieldValue
    aux_off_battery_voltage: FieldValue
    aux_off_delay_time: FieldValue
    aux_relay_mode: FieldValue
    aux_relay_control: FieldValue
    aux_relay_on_battery_voltage: FieldValue
    aux_relay_on_delay_time: FieldValue
    aux_relay_off_battery_voltage: FieldValue
    aux_relay_off_delay_time: FieldValue
    stacking_mode: FieldValue
    master_power_save_level: FieldValue
    slave_power_save_level: FieldValue
    sell_volts: FieldValue
    grid_tie_window: FieldValue
    grid_tie_enable: FieldValue
    grid_ac_input_voltage_calibrate_factor: FieldValue
    gen_ac_input_voltage_calibrate_factor: FieldValue
    ac_output_voltage_calibrate_factor: FieldValue
    battery_voltage_calibrate_factor: FieldValue
    re_bulk_volts: FieldValue
    mini_grid_lbx_volts: FieldValue
    mini_grid_lbx_delay: FieldValue
    grid_zero_do_d_volts: FieldValue
    grid_zero_do_d_max_offset_ac_amps: FieldValue
    serial_number: FieldValue
    model_number: FieldValue
    module_control: FieldValue
    model_select: FieldValue
    low_battery_cut_out_delay: FieldValue
    high_battery_cut_out_voltage: FieldValue
    high_battery_cut_in_voltage: FieldValue
    high_battery_cut_out_delay: FieldValue
    ee_write_enable: FieldValue


@dataclass
class SinglePhaseRadianInverterRealTimeValues(ModelValues):
    did: FieldValue
    length: FieldValue
    port_number: FieldValue
    dc_voltage_scale_factor: FieldValue
    ac_current_scale_factor: FieldValue
    ac_voltage_scale_factor: FieldValue
    ac_frequency_scale_factor: FieldValue
    inverter_output_current: FieldValue
    inverter_charge_current: FieldValue
    inverter_buy_current: FieldValue
    inverter_sell_current: FieldValue
    grid_input_ac_voltage: FieldValue
    gen_input_ac_voltage: FieldValue
    output_ac_voltage: FieldValue
    inverter_operating_mode: FieldValue
    error_flags: FieldValue
    warning_flags: FieldValue
    battery_voltage: FieldValue
    temp_compensated_target_voltage: FieldValue
    aux_output_state: FieldValue
    aux_relay_output_state: FieldValue
    l_module_transformer_temperature: FieldValue
    l_module_capacitor_temperature: FieldValue
    l_module_fet_temperature: FieldValue
    r_module_transformer_temperature: FieldValue
    r_module_capacitor_temperature: FieldValue
    r_module_fet_temperature: FieldValue
    battery_temperature: FieldValue
    ac_input_selection: FieldValue
    ac_input_frequency: FieldValue
    ac_input_voltage: FieldValue
    ac_input_state: FieldValue
    minimum_ac_input_voltage: FieldValue
    maximum_ac_input_voltage: FieldValue
    sell_status: FieldValue
    kwh_scale_factor: FieldValue
    ac1_buy_kwh: FieldValue
    ac2_buy_kwh: FieldValue
    ac1_sell_kwh: FieldValue
    ac2_sell_kwh: FieldValue
    output_kwh: FieldValue
    charger_kwh: FieldValue
    output_kw: FieldValue
    buy_kw: FieldValue
    sell_kw: FieldValue
    charge_kw: FieldValue
    load_kw: FieldValue
    ac_couple_kw: FieldValue
    gt_number: FieldValue


@dataclass
class FLEXnetDCRealTimeValues(ModelValues):
    did: FieldValue
    length: FieldValue
    port_number: FieldValue
    dc_voltage_scale_factor: FieldValue
    dc_current_scale_factor: FieldValue
    time_scale_factor: FieldValue
    kwh_scale_factor: FieldValue
    kw_scale_factor: FieldValue
    shunt_a_current: FieldValue
    shunt_b_current: FieldValue
    shunt_c_current: FieldValue
    battery_voltage: FieldValue
    battery_current: FieldValue
    battery_temperature: FieldValue
    status_flags: FieldValue
    shunt_a_accumulated_ah: FieldValue
    shunt_a_accumulated_kwh: FieldValue
    shunt_b_accumulated_ah: FieldValue
    shunt_b_accumulated_kwh: FieldValue
    shunt_c_accumulated_ah: FieldValue
    shunt_c_accumulated_kwh: FieldValue
    input_current: FieldValue
    output_current: FieldValue
    input_kw: FieldValue
    output_kw: FieldValue
    net_kw: FieldValue
    days_since_charge_parameters_met: FieldValue
    state_of_charge: FieldValue
    todays_minimum_soc: FieldValue
    todays_maximum_soc: FieldValue
    todays_net_input_ah: FieldValue
    todays_net_input_kwh: FieldValue
    todays_net_output_ah: FieldValue
    todays_net_output_kwh: FieldValue
    todays_net_battery_ah: FieldValue
    todays_net_battery_kwh: FieldValue
    charge_factor_corrected_net_battery_ah: FieldValue
    charge_factor_corrected_net_battery_kwh: FieldValue
    todays_minimum_battery_voltage: FieldValue
    todays_minimum_battery_time: FieldValue
    todays_maximum_battery_voltage: FieldValue
    todays_maximum_battery_time: FieldValue
    cycle_charge_factor: FieldValue
    cycle_kwh_charge_efficiency: FieldValue
    total_days_at_100_percent: FieldValue
    lifetime_k_ah_removed: FieldValue
    shunt_a_historical_returned_to_battery_ah: FieldValue
    shunt_a_historical_returned_to_battery_kwh: FieldValue
    shunt_a_historical_removed_from_battery_ah: FieldValue
    shunt_a_historical_removed_from_battery_kwh: FieldValue
    shunt_a_maximum_charge_rate: FieldValue
    shunt_a_maximum_charge_rate_kw: FieldValue
    shunt_a_maximum_discharge_rate: FieldValue
    shunt_a_maximum_discharge_rate_kw: FieldValue
    shunt_b_historical_returned_to_battery_ah: FieldValue
    shunt_b_historical_returned_to_battery_kwh: FieldValue
    shunt_b_historical_removed_from_battery_ah: FieldValue
    shunt_b_historical_removed_from_battery_kwh: FieldValue
    shunt_b_maximum_charge_rate: FieldValue
    shunt_b_maximum_charge_rate_kw: FieldValue
    shunt_b_maximum_discharge_rate: FieldValue
    shunt_b_maximum_discharge_rate_kw: FieldValue
    shunt_c_historical_returned_to_battery_ah: FieldValue
    shunt_c_historical_returned_to_battery_kwh: FieldValue
    shunt_c_historical_removed_from_battery_ah: FieldValue
    shunt_c_historical_removed_from_battery_kwh: FieldValue
    shunt_c_maximum_charge_rate: FieldValue
    shunt_c_maximum_charge_rate_kw: FieldValue
    shunt_c_maximum_discharge_rate: FieldValue
    shunt_c_maximum_discharge_rate_kw: FieldValue
    shunt_a_reset_maximum_data: FieldValue
    shunt_a_reset_maximum_data_write_complement: FieldValue
    shunt_b_reset_maximum_data: FieldValue
    shunt_b_reset_maximum_data_write_complement: FieldValue
    shunt_c_reset_maximum_data: FieldValue
    shunt_c_reset_maximum_data_write_complement: FieldValue


@dataclass
class FLEXnetDCConfigurationValues(ModelValues):
    did: FieldValue
    length: FieldValue
    port_number: FieldValue
    dc_voltage_scale_factor: FieldValue
    dc_current_scale_factor: FieldValue
    kwh_scale_factor: FieldValue
    major_firmware_number: FieldValue
    mid_firmware_number: FieldValue
    minor_firmware_number: FieldValue
    battery_capacity: FieldValue
    charged_volts: FieldValue
    charged_time: FieldValue
    battery_charged_amps: FieldValue
    charge_factor: FieldValue
    shunt_a_enabled: FieldValue
    shunt_b_enabled: FieldValue
    shunt_c_enabled: FieldValue
    relay_control: FieldValue
    relay_invert_logic: FieldValue
    relay_high_voltage: FieldValue
    relay_low_voltage: FieldValue
    relay_soc_high: FieldValue
    relay_soc_low: FieldValue
    relay_high_enable_delay: FieldValue
    relay_low_enable_delay: FieldValue
    set_data_log_day_offset: FieldValue
    get_current_data_log_day_offset: FieldValue
    datalog_minimum_soc: FieldValue
    datalog_input_ah: FieldValue
    datalog_input_kwh: FieldValue
    datalog_output_ah: FieldValue
    datalog_output_kwh: FieldValue
    datalog_net_ah: FieldValue
    datalog_net_kwh: FieldValue
    clear_data_log_read: FieldValue
    clear_data_log_write_complement: FieldValue
    serial_number: FieldValue
    model_number: FieldValue


@dataclass
class OutBackSystemControlValues(ModelValues):
    did: FieldValue
    length: FieldValue
    dc_voltage_scale_factor: FieldValue
    ac_current_scale_factor: FieldValue
    time_scale_factor: FieldValue
    bulk_charge_enable_disable: FieldValue
    inverter_ac_drop_use: FieldValue
    set_inverter_mode: FieldValue
    grid_tie_mode: FieldValue
    set_inverter_charger_mode: FieldValue
    control_status: FieldValue
    set_sell_voltage: FieldValue
    set_radian_inverter_sell_current_limit: FieldValue
    set_absorb_voltage: FieldValue
    set_absorb_time: FieldValue
    set_float_voltage: FieldValue
    set_float_time: FieldValue
    set_inverter_charger_current_limit: FieldValue
    set_inverter_ac1_current_limit: FieldValue
    set_inverter_ac2_current_limit: FieldValue
    set_ags_op_mode: FieldValue
    ags_operational_state: FieldValue
    ags_operational_state_timer: FieldValue
    gen_last_run_start_time_gmt: FieldValue
    gen_last_start_run_duration: FieldValue


@dataclass
class OPTICSPacketStatisticsValues(ModelValues):
    did: FieldValue
    length: FieldValue
    bt_min: FieldValue
    bt_max: FieldValue
    bt_ave: FieldValue
    bt_attempts: FieldValue
    bt_errors: FieldValue
    bt_timeouts: FieldValue
    bt_packet_timeout: FieldValue
    mp_min: FieldValue
    mp_max: FieldValue
    mp_ave: FieldValue
    mp_attempts: FieldValue
    mp_errors: FieldValue
    mp_timeouts: FieldValue
    mp_packet_timeout: FieldValue
    cu_min: FieldValue
    cu_max: FieldValue
    cu_ave: FieldValue
    cu_attempts: FieldValue
    cu_errors: FieldValue
    cu_timeouts: FieldValue
    cu_packet_timeout: FieldValue
    su_min: FieldValue
    su_max: FieldValue
    su_ave: FieldValue
    su_attempts: FieldValue
    su_errors: FieldValue
    su_timeouts: FieldValue
    su_packet_timeout: FieldValue
    pg_min: FieldValue
    pg_max: FieldValue
    pg_ave: FieldValue
    pg_attempts: FieldValue
    pg_errors: FieldValue
    pg_timeouts: FieldValue
    pg_packet_timeout: FieldValue
    mb_min: FieldValue
    mb_max: FieldValue
    mb_ave: FieldValue
    mb_attempts: FieldValue
    mb_errors: FieldValue
    mb_timeouts: FieldValue
    mb_packet_timeout: FieldValue
    fu_min: FieldValue
    fu_max: FieldValue
    fu_ave: FieldValue
    fu_attempts: FieldValue
    fu_errors: FieldValue
    fu_timeouts: FieldValue
    fu_packet_timeout: FieldValue
    ev_min: FieldValue
    ev_max: FieldValue
    ev_ave: FieldValue
    ev_attempts: FieldValue
    ev_errors: FieldValue
    ev_timeouts: FieldValue
    ev_packet_timeout: FieldValue


MODELS_TO_VALUES = {
    models.SunSpecHeaderModel: SunSpecHeaderValues,
    models.SunSpecEndModel: SunSpecEndValues,
    models.SunSpecCommonModel: SunSpecCommonValues,
    models.SunSpecInverterSinglePhaseModel: SunSpecInverterSinglePhaseValues,
    models.SunSpecInverterSplitPhaseModel: SunSpecInverterSplitPhaseValues,
    models.SunSpecInverterThreePhaseModel: SunSpecInverterThreePhaseValues,
    models.OutBackModel: OutBackValues,
    models.ChargeControllerModel: ChargeControllerValues,
    models.ChargeControllerConfigurationModel: ChargeControllerConfigurationValues,
    models.FXInverterRealTimeModel: FXInverterRealTimeValues,
    models.FXInverterConfigurationModel: FXInverterConfigurationValues,
    models.SplitPhaseRadianInverterRealTimeModel: SplitPhaseRadianInverterRealTimeValues,
    models.RadianInverterConfigurationModel: RadianInverterConfigurationValues,
    models.SinglePhaseRadianInverterRealTimeModel: SinglePhaseRadianInverterRealTimeValues,
    models.FLEXnetDCRealTimeModel: FLEXnetDCRealTimeValues,
    models.FLEXnetDCConfigurationModel: FLEXnetDCConfigurationValues,
    models.OutBackSystemControlModel: OutBackSystemControlValues,
    models.OPTICSPacketStatisticsModel: OPTICSPacketStatisticsValues,
}
