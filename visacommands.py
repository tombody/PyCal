import visa

rm = visa.ResourceManager()

def open_instrument(code):
    current_instrument = rm.open_resource(code)

def unit_identifier():
    return None


def list_resources():
    return rm.list_resources()


