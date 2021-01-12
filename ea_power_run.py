#!/usr/bin/env python3

from ea_psu_controller import PsuEA
import configparser
import time
import os

os.chdir("C:\\Users\\gw00192300\\PycharmProjects\\pythonProject")

# Read config from file
config = configparser.ConfigParser()
config.read("EA_POWER_CONFIG.ini")

cycle_count = config.getint("DEVICE", "power_cycle_count")
power_v_config_count = config.getint("DEVICE", "power_v_count")

# psu = PsuEA(comport='COM10')
psu = PsuEA(comport=str(config.get("DEVICE", "port")))
psu.remote_on()
psu.output_on()
psu.set_ovp(19)
psu.set_ocp(10)

if cycle_count != 0:
    while cycle_count != 0:
        cycle_count -= 1
        for count in range(0, power_v_config_count):
            name = "POWER_v_" + str(count)
            psu.set_voltage(config.getfloat(name, "v_value"))
            time.sleep(config.getint(name, "time_in_sec"))
else:
    while True:
        for count in range(0, power_v_config_count):
            name = "POWER_v_" + str(count)
            psu.set_voltage(config.getfloat(name, "v_value"))
            time.sleep(config.getint(name, "time_in_sec"))

print("TEST DONE!!!!!")
psu.close(False, False, output_num=0)
