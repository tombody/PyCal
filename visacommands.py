import visa

available_instruments = ["3478A", "34401A", "5520A"]
rm = visa.ResourceManager()

def open_instrument(code):
    current_instrument = rm.open_resource(code)

def unit_identifier():
    return None


def list_resources():
    return rm.list_resources()


def unit_identifiers(units):
    """
    Creates a dict of all available resources

    kwargs:
    unit -- rm.list_resources()
    """
    identities = {}
    for unit in units:
        identities[unit] = ""
        inst = rm.open_resource(unit)
        if unit[:4]=="GPIB":
            identity = inst.query("*IDN?")
            identities[unit] = identity
    return identities


