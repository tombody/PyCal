import visa

rm = visa.ResourceManager()


def unit_identifier():
    return None


def list_resources():
    return rm.list_resources()


