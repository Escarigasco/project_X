# Class for interface - it operates the data structure to collect all the objects and create busbars
from busbars import busbar as bb
_FIRST_OF_THE_CLASS = 0


class interface(object):

    def __init__(self, building, board_ID):
        self.building = building
        self.board = self.building.switch_board_list[board_ID]   # good practice to short names

    def get_hydraulic_bays(self):
        return self.board.bays_list

    def get_system_sensors(self):
        bays_list = self.board.bays_list  # ridefinition of variable for clarity
        line_sensors = {}
        connector_sensors_lists = {}
        sensors_list = {}

        for bay in bays_list.keys():  # parsing dictionary keys
            hydraulic_bay = bays_list[bay]
            bay_connectors_list = hydraulic_bay.connectors_list

            for connector in bay_connectors_list.keys():
                bay_connector = bay_connectors_list[connector]
                lines_list = bay_connector.lines_list

                for line in lines_list.keys():
                        connector_line = lines_list[line]
                        line_sensors.update(connector_line.line_sensors)  # add sensors list from each line

        sensors_list = {**connector_sensors_lists, **line_sensors}

        return sensors_list

    def get_system_pumps(self):
        bays_list = self.board.bays_list  # ridefinition of variable for clarity
        line_pumps_list = {}

        for bay in bays_list.keys():  # parsing dictionary keys
            hydraulic_bay = bays_list[bay]
            bay_connectors_list = hydraulic_bay.connectors_list

            for connector in bay_connectors_list.keys():
                bay_connector = bay_connectors_list[connector]
                lines_list = bay_connector.lines_list

                for line in lines_list.keys():
                        connector_line = lines_list[line]
                        line_pumps_list.update(connector_line.pumps)  # add pumps list from each line

        return line_pumps_list

    def get_system_valves(self):
        bays_list = self.board.bays_list  # ridefinition of variable for clarity
        bay_valves_list = {}
        pipes_in_list = {}   # ridefinition of variable for clarity
        pipes_out_list = {}

        for bay in bays_list.keys():  # parsing dictionary keys
            hydraulic_bay = bays_list[bay]
            pipes_in_list = hydraulic_bay.pipes_in_list
            pipes_out_list = hydraulic_bay.pipes_out_list

            for pipe in pipes_in_list.keys():
                pipeline = pipes_in_list[pipe]
                bay_valves_list.update(pipeline.valves_list)
            for pipe in pipes_out_list.keys():
                pipeline = pipes_out_list[pipe]
                bay_valves_list.update(pipeline.valves_list)

        return bay_valves_list

    def get_system_pipes(self):
        bays_list = self.board.bays_list  # ridefinition of variable for clarity
        pipes_in_list = {}   # ridefinition of variable for clarity
        pipes_out_list = {}
        pipes_list = {}

        for bay in bays_list.keys():  # parsing dictionary keys
            hydraulic_bay = bays_list[bay]
            pipes_in_list.update(hydraulic_bay.pipes_in_list)
            pipes_out_list.update(hydraulic_bay.pipes_out_list)

        pipes_list["in"] = pipes_in_list
        pipes_list["out"] = pipes_out_list

        return pipes_list

    def get_system_connectors(self):
        bays_list = self.board.bays_list  # ridefinition of variable for clarity
        connectors_list = {}

        for bay in bays_list.keys():  # parsing dictionary keys
            hydraulic_bay = bays_list[bay]
            connectors_list.update(hydraulic_bay.connectors_list)

        return connectors_list

    def get_system_lines(self):
        bays_list = self.board.bays_list  # ridefinition of variable for clarity
        lines_list = {}
        connectors_list = {}   # ridefinition of variable for clarity

        for bay in bays_list.keys():  # parsing dictionary keys
            hydraulic_bay = bays_list[bay]
            connectors_list = hydraulic_bay.connectors_list

            for connector in connectors_list.keys():
                connector = connectors_list[connector]
                lines_list.update(connector.lines_list)

        return lines_list

    def get_connected_devices(self):
        bays_list = self.board.bays_list  # ridefinition of variable for clarity
        connected_devices_list = {}

        for bay in bays_list.keys():  # parsing dictionary keys
            hydraulic_bay = bays_list[bay]
            bay_connectors_list = hydraulic_bay.connectors_list

            for connector in bay_connectors_list.keys():
                bay_connector = bay_connectors_list[connector]
                connected_devices_list.update(bay_connector.connected_devices_list)

        return connected_devices_list

    def get_all_parents(self):  # return a list of all possible superstructure within a swithcboard
        bays_list = self.board.bays_list
        bay_connectors_list = {}
        connector_lines_list = {}
        pipeline_list = {}

        for bay in bays_list.keys():
            hydraulic_bay = bays_list[bay]
            bay_connectors_list.update(hydraulic_bay.connectors_list)  # computing burden
            connector_for_iteration = hydraulic_bay.connectors_list

            pipeline_list.update(hydraulic_bay.pipes_out_list)
            pipeline_list.update(hydraulic_bay.pipes_in_list)

            for connector in connector_for_iteration.keys():
                bay_connector = connector_for_iteration[connector]
                connector_lines_list.update(bay_connector.lines_list)

        parents_list = {**bays_list, **bay_connectors_list, **connector_lines_list, **pipeline_list}
        return parents_list

    def build_busbars(self, system_pipes):
        busbars_names = set([])
        buffer_for_pipes = []
        busbars_list = {}

        for direction in system_pipes.keys():
            for pipe in system_pipes[direction].keys():
                busbars_names.add(system_pipes[direction][pipe].get_busbar_connection())

        for busbar in busbars_names:
            for direction in system_pipes.keys():
                for pipe in system_pipes[direction].keys():
                    #  print(system_pipes[direction].keys())
                    if (system_pipes[direction][pipe].get_busbar_connection() == busbar):
                        buffer_for_pipes.append(system_pipes[direction][pipe])

            busbars_list[busbar] = bb(busbar, buffer_for_pipes)
            buffer_for_pipes = []
            # you can't really solved the double call of the booster bar pipes as they are actually a couple
            # of objects as the booster can be both a in or out pipe - in reality it will always be a in pipe and only sources will use it
            # this is also proved by the fact that no motorized valve are installed at the sinks in the booster bar

        return busbars_list
