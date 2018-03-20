import visa

rm = visa.ResourceManager()

#Global variables
AVAILABLE_INSTRUMENTS = ["3478A", "34401A", "5520A"]


def open_instrument(code):
    """
    Opens the selected instrument
    :param code:
    """
    current_instrument = rm.open_resource(code)


def list_resources():
    """
    returns a list of resources using the NI backend
    :return:
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


def set():
    pass

