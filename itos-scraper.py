import csv, requests, sys

BASE_URL = "http://gistmaps.itos.uga.edu/arcgis/rest/services/"
""" Base API URL for iTOS services """

def get_itos_services ():
    """ Get the list of iTOS services.
    Each item will consist of the service name (starting with "COD_EXTERNAL/") and type.
    """
    result = requests.get(BASE_URL + "COD_External/?f=json")
    return result.json().get("services")

def get_itos_labels (name):
    """ Extract labels from an iTOS service name.
    This is a kludge. iTOS should have this info fielded in the JSON.
    """
    stub = name[13:]
    if "_" in stub:
        labels = stub.split("_")
        return labels[0], labels[1]
    else:
        return stub, ""

def get_itos_service_layers (name, type):
    """ Get the list of layers for an iTOS service.
    """
    result = requests.get(BASE_URL +  "{}/{}/layers?f=json".format(name, type))
    return result.json().get("layers")

#
# Scrape iTOS to extract basic info about the layers available and write to stdout.
#

output = csv.writer(sys.stdout)

output.writerow([
    "Country code",
    "Service type",
    "Service label",
    "Layer id",
    "Layer name",
    "Min lat",
    "Max lat",
    "Min lon",
    "Max lon",
])

output.writerow([
    "#country +code",
    "#service +type",
    "#service +label",
    "#meta +id",
    "#geo +admin_type",
    "#geo +lat +max",
    "#geo +lat +min",
    "#geo +lon +max",
    "#geo +lon +min",
])

for service in get_itos_services():
    country_code, service_label = get_itos_labels(service["name"])
    country_code = service["name"][13:16] # hack: strange they don't seem to provide this as a separate field
    for layer in get_itos_service_layers(service["name"], service["type"]):
        output.writerow([
            country_code,
            service["type"],
            service_label,
            layer["id"],
            layer["name"],
            layer["extent"]["ymin"],
            layer["extent"]["ymax"],
            layer["extent"]["xmin"],
            layer["extent"]["xmax"],
        ])
