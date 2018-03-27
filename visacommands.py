import visa

rm = visa.ResourceManager()

#Global variables
AVAILABLE_INSTRUMENTS = ["34401A", "5520A", "3478A"]
PREFIX_LIST = ["p", "n", "µ", " ", "m", "k", "M", "G"]
UNITS_LIST = ["V", "A", "Ω", "Hz", "°C", "F", "dBm", "W", "sec"]


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


def query(unit, command):
    inst = rm.open_resource(unit)
    output = inst.query(command)
    return output

