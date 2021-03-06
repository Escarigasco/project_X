import syslab
import syslab.core.datatypes.CompositeMeasurement as CM
import syslab.core.datatypes.HeatCirculationPumpMode as PM
import time
import sys

_BUILDING_NAME = "716-h1"
_MULTIPLIER = 1000000
_TURN_ME_ON = 1.0
_TURN_ME_OFF = 0.0
_VALVES = 'Valves_active'
_VALVES_TO_SHUT = 'Valves_to_shut'
_PUMP = "Pump"
_SOURCE = 1
_VALIDITY = 1
_ZERO = 0


class physical_logic(object):

    def __init__(self):
        self.valves_status = {
            "Bay_2L-Busbar_2R": 0.0, "Bay_2L-Busbar_1R": 0.0, "Bay_2H-Busbar_B": 0.0, "Bay_2H-Busbar_2F": 0.0, "Bay_2H-Busbar_1F": 0.0, "Bay_2L-Busbar_B": 0.0,
            "Bay_3L-Busbar_2R": 0.0, "Bay_3L-Busbar_1R": 0.0, "Bay_3H-Busbar_B": 0.0, "Bay_3H-Busbar_2F": 0.0, "Bay_3H-Busbar_1F": 0.0, "Bay_3L-Busbar_B": 0.0,
            "Bay_4L-Busbar_2R": 0.0, "Bay_4L-Busbar_1R": 0.0, "Bay_4H-Busbar_B": 0.0, "Bay_4H-Busbar_2F": 0.0, "Bay_4H-Busbar_1F": 0.0, "Bay_4L-Busbar_B": 0.0,
            "Bay_5L-Busbar_1R": 0.0, "Bay_5L-Busbar_2R": 0.0, "Bay_5H-Busbar_B": 0.0, "Bay_5H-Busbar_1F": 0.0, "Bay_5H-Busbar_2F": 0.0, "Bay_5L-Busbar_B": 0.0,
            "Bay_6L-Busbar_1R": 0.0, "Bay_6L-Busbar_2R": 0.0, "Bay_6H-Busbar_B": 0.0, "Bay_6H-Busbar_1F": 0.0, "Bay_6H-Busbar_2F": 0.0, "Bay_6L-Busbar_B": 0.0,
            "Bay_7H-Busbar_1F": 0.0, "Bay_7H-Busbar_2F": 0.0, "Bay_7L-Busbar_1R": 0.0, "Bay_7L-Busbar_2R": 0.0,
            "Bay_8H-Busbar_1F": 0.0, "Bay_8H-Busbar_2F": 0.0, "Bay_8L-Busbar_1R": 0.0, "Bay_8L-Busbar_2R": 0.0}
        self.pumps_status = {
            "Pump_Bay4": 0.0,
            "Pump_Bay5": 0.0,
            "Pump_Bay6": 0.0,
            "Pump_Bay7": 0.0,
            "Pump_Bay8": 0.0}

        self.interface = syslab.HeatSwitchBoard(_BUILDING_NAME)

    def initialization(self, inputs):
        print("Initialization of the equipment")
        valves_status_checker = {}
        complete = False
        CompositMess_Shut = CM(_TURN_ME_OFF, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        circulator_mode = 4
        circulator_mode = PM(circulator_mode, time.time() * _MULTIPLIER)
        opening_threshold = 0.05
        for pump in inputs[_PUMP]:
                    #self.interface.setPumpControlMode(pumps, circulator_mode)
                    print("mode set in pump ", pump)
                    #self.interface.setPumpSetpoint(circulator, CompositMess_Shut)
                    print("setpoint at 0 for pump ", pump)
        while not complete:
            for valve in inputs[_VALVES_TO_SHUT]:
                self.valves_status[valve] = 0.0
                print("setpoint at 0 for valve", valve)
                #self.interface.setValvePosition(valve, CompositMess_Shut)
            #time.sleep(10)
            for valve in inputs[_VALVES_TO_SHUT]:
                valves_status_checker[valve] = 0.0  #self.interface.getValvePosition(valve)
                if ((sum(opening for opening in valves_status_checker.values()) <= opening_threshold)):
                    complete = True
        return [complete, self.valves_status]

    def get_pumps_status(self, pumps_for_physical_layer):
        print("I am reading pumps")
        pumps_for_logical_layer = {}
        for pump in pumps_for_physical_layer.keys():
            head = self.interface.getPumpHead(pump)
            pumps_for_logical_layer[pump] = head.value
        return pumps_for_logical_layer

    def get_pumps_simulated_status(self, pumps_for_physical_layer):
        print("I am reading simulated pumps")
        pumps_for_logical_layer = {}
        for pump in pumps_for_physical_layer.keys():
            pumps_for_logical_layer[pump] = self.pumps_status[pump]
        return pumps_for_logical_layer

    def get_valves_status(self, valves_for_physical_layer):
        #print("I am reading circuit")
        valves_for_logical_layer = {}
        for valve in valves_for_physical_layer.keys():
            opening = self.interface.getValvePosition(valve)
            valves_for_logical_layer[valve] = opening.value
        return valves_for_logical_layer

    def get_valves_simulated_status(self, valves_for_physical_layer, queue=None):
        #print("I am reading simulated circuit")
        valves_for_logical_layer = {}
        for valve in valves_for_physical_layer.keys():
            valves_for_logical_layer[valve] = self.valves_status[valve]
        return valves_for_logical_layer

    def set_hydraulic_circuit(self, inputs):
        valves = inputs[_VALVES]
        valves_to_shut = inputs[_VALVES_TO_SHUT]
        valves_status = {}
        valves_to_shut_status = {}
        opening_threshold = len(valves) * 0.95
        closing_threshold = len(valves_to_shut) * 0.1
        CompositMess_Shut = CM(_TURN_ME_OFF, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        CompositMess_Open = CM(_TURN_ME_ON, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        complete = False
        for valve in valves_to_shut:
            time.sleep(0.1)
            self.interface.setValvePosition(valve, CompositMess_Shut)
            print("I have set to 0 valve ", valve)
        for valve in valves:
            time.sleep(0.1)
            self.interface.setValvePosition(valve, CompositMess_Open)
            print("I have set to 1 valve ", valve)
        time.sleep(5)
        while not complete:
            time.sleep(1)
            for valve in valves:
                valves_status[valve] = self.interface.getValvePosition(valve).value
                if not isinstance(valves_status[valve], float):
                    valves_status[valve] = 0
                print("valves status")
                print(valves_status)
                time.sleep(0.1)
            for valve in valves_to_shut:
                valves_to_shut_status[valve] = self.interface.getValvePosition(valve).value
                if not isinstance(valves_to_shut_status[valve], float):
                    valves_to_shut_status[valve] = 0
                print("valves to shut status")
                print(valves_to_shut_status)
                time.sleep(0.1)
            if ((sum(opening for opening in valves_status.values()) > opening_threshold) &
               (sum(opening for opening in valves_to_shut_status.values()) < closing_threshold)):
                complete = True
        return complete

    def set_hydraulic_simulated_circuit(self, inputs):
        print("I am setting simulated circuit")
        #time.sleep(1)
        valves = inputs[_VALVES]
        valves_to_shut = inputs[_VALVES_TO_SHUT]
        valves_status = {}
        valves_to_shut_status = {}
        opening_threshold = len(valves) * 0.9
        closing_threshold = len(valves_status) * 0.1
        complete = False
        for valve in valves:
            valves_status[valve] = 1.0
            self.valves_status[valve] = 1.0
        for valve in valves_to_shut:
            valves_to_shut_status[valve] = 1.0
            self.valves_status[valve] = 0.0
        # print(sum(opening for opening in valves_status.values()))
        if ((sum(opening for opening in valves_status.values()) >= opening_threshold)
           & (sum(opening for opening in valves_to_shut_status.values()) <= closing_threshold)):
                complete = True
        print(self.valves_status)
        return [complete, self.valves_status]

    def shut_pumps(self, pumps):
        pumps = pumps[_PUMP]
        for pump in pumps:
            #self.interface.stopPump(pump)
            print("Pump ", pump, " was stopped")
        return ("All the pumps not in use have been stopped")

    def update_valves(self, valves):
        self.valves_status = valves
