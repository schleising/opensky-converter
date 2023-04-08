# The original IRCA mapping, used if the default mapping file doesn't exist or the user chooses to reset the mapping

from pathlib import Path

ORIGINAL_IRCA_MAPPING = {
    'icao24': 'icao24',
    'registration': 'registration',
    'manufacturericao': 'manufacturericao',
    'manufacturername': 'manufacturername',
    'model': 'model',
    'typecode': 'typecode',
    'serialnumber': 'serialnumber',
    'linenumber': 'linenumber',
    'icaoaircrafttype': 'icaoaircrafttype',
    'operator': 'operator',
    'operatorcallsign': 'operatorcallsign',
    'operatoricao': 'operatoricao',
    'operatoriata': 'operatoriata',
    'owner': 'owner',
    'testreg': 'testreg',
    'registered': 'registered',
    'reguntil': 'reguntil',
    'status': 'status',
    'built': 'built',
    'firstflightdate': 'firstflightdate',
    'seatconfiguration': 'seatconfiguration',
    'engines': 'engines',
    'modes': 'modes',
    'adsb': 'adsb',
    'acars': 'acars',
    'notes': 'notes',
    'categoryDescription': 'categoryDescription',
}

DEFAULT_MAPPING_PATH = Path('defaults/default_mapping.json')