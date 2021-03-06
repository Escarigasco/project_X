# Pipeline Class that generates the embedded valves

from bay_valve import bay_valve


class pipeline(object):
    'Class for Pipeline definition and properties'

    def __init__(self, parent_ID, ID, pipe, busbar, type, direction, connected_dev):
        self.parent_ID = parent_ID
        self.ID = ID
        self.pipe = pipe
        self.direction = direction
        self.valves_list = {}
        self.busbar = busbar
        self.type = type

        valves = self.pipe.find_all("valve")     # find valves

        for valve in valves:
            self.valves_list[valve["id"]] = bay_valve(self.ID, valve["id"], valve["connection"], valve["flow"], self.direction, connected_dev)  # creates valves

    def get_parent(self):
        return self.parent_ID

    def get_type(self):
        return self.type

    def get_name(self):
        return self.ID

    def get_busbar_connection(self):
        return self.busbar

    def __repr__(self):
        return "<Pipe, id: {0}>".format(self.ID)

    def __str__(self):
        return "<Pipe, id: {0}>".format(self.ID)
