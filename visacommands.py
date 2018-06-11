import visa

rm = visa.ResourceManager()

# Global constants
AVAILABLE_INSTRUMENTS = ["34401A", "5520A",]
PREFIX_LIST = {"p": "p", "n": "n", "µ": "u", "m": "m", " ": " ", "k": "k", "M": "M"}
UNITS_LIST_1 = {"V": "V", "A": "A", "Ω": "OHM", "Hz": "Hz", "°C": "CEL", "F": "F"}
UNITS_LIST_2 = {"Hz": "Hz", "A": "A"}


def open_instrument(code):
    """
    Opens the selected instrument
    :param code: string -- GPIB address
    """
    current_instrument = rm.open_resource(code)


def list_resources():
    """
    :return a list of resources using the NI backend
    """
    return rm.list_resources()


def unit_identifiers(units):
    """
    Creates a dict of all available resources
    :param units: rm.list_resources()
    :returns: dict
    """
    identities = {}
    for unit in units:
        identities[unit] = ""
        inst = rm.open_resource(unit)
        if unit[:4] == "GPIB":
            identity = inst.query("*IDN?")
            identities[unit] = identity
    return identities


def query(instrument, command):
    '''
    Queries the instrument
    :param instrument: Current connected instrument
    :param command: GPIB command to be run
    :return: the instruments queried output
    '''
    inst = rm.open_resource(instrument)
    output = inst.query(command)
    return output


def write(instrument, command):
    '''
    Writes only to the instrument
    :param instrument: Current connected instrument
    :param command: GPIB command to be run
    '''
    inst = rm.open_resource(instrument)
    inst.write(command)


def read(instrument, command):
    inst = rm.open_resource(instrument)
    output = inst.read(command)
    return output


