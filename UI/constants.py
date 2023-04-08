# The original IRCA mapping, used if the default mapping file doesn't exist or the user chooses to reset the mapping

from pathlib import Path

UI_REFRESH_TIME = 100 # The time in milliseconds to wait before refreshing the progress bars

NO_MAPPING_STRING = 'Do not Map'

MODE_S_ADDRESS_KEY = 'ModeSCode'

ORIGINAL_IRCA_MAPPING = {
    'RegistrationMark': 'registration',
    'NCAAAircraftSerialNumber': 'serialnumber',
    'NCAARegistrationDt': NO_MAPPING_STRING,
    'OwnerName': 'owner',
    'OwnerAddress1': NO_MAPPING_STRING,
    'OwnerAddress2': NO_MAPPING_STRING,
    'OwnerAddress3': NO_MAPPING_STRING,
    'Country_ICAOCountryName': NO_MAPPING_STRING,
    'OperatorName': NO_MAPPING_STRING,
    'OperatorAddress1': NO_MAPPING_STRING,
    'OperatorAddress2': NO_MAPPING_STRING,
    'OperatorAddress3': NO_MAPPING_STRING,
    'Country_1_ICAOCountryName': NO_MAPPING_STRING,
    'AirportName': NO_MAPPING_STRING,
    'CellCategoryDesc': NO_MAPPING_STRING,
    'CellManufacturer': 'manufacturericao',
    'NCAACellManufacturer': 'manufacturericao',
    'CellMake': 'model',
    'CellMasterModel': 'typecode',
    'CellModel': 'typecode',
    'NCAACellModel': 'typecode',
    'CellMasterSerie': NO_MAPPING_STRING,
    'CellSeries': NO_MAPPING_STRING,
    'CellPopularName': NO_MAPPING_STRING,
    'PaxCount': NO_MAPPING_STRING,
    'NCAAPaxCount': NO_MAPPING_STRING,
    'CellMTOW': NO_MAPPING_STRING,
    'NCAAMTOW': NO_MAPPING_STRING,
    'CellYearFirstConstruction': 'built',
    'NCAAYearOfConstruction': 'built',
    'Length': NO_MAPPING_STRING,
    'CellWidth': NO_MAPPING_STRING,
    'CellHeight': NO_MAPPING_STRING,
    'Ceiling': NO_MAPPING_STRING,
    'MaximumSpeed': NO_MAPPING_STRING,
    'ConstructionMaterial': NO_MAPPING_STRING,
    'AerofoilDesc': NO_MAPPING_STRING,
    'EmpennageDesc': NO_MAPPING_STRING,
    'LandingGearDesc': NO_MAPPING_STRING,
    'Pressurization': NO_MAPPING_STRING,
    'EngineCount': NO_MAPPING_STRING,
    'OACICODE': NO_MAPPING_STRING,
    'ModeSCode': 'icao24',
    'NCAANoiseInformation': NO_MAPPING_STRING,
    'NCAACDNCategory': NO_MAPPING_STRING,
    'NCAACDNExpirationDt': NO_MAPPING_STRING,
    'EngineCategory': NO_MAPPING_STRING,
    'EngineManufacturer': NO_MAPPING_STRING,
    'NCAAEngineManufacturer': NO_MAPPING_STRING,
    'NCAAEngineType': 'engines',
    'EngineModel': 'engines',
    'NCAAEngineModel': 'engines',
    'EngineHorsePower': NO_MAPPING_STRING,
    'EngineUnity': NO_MAPPING_STRING,
    'PropellerCategoryDesc': NO_MAPPING_STRING,
    'PropellerManufacturer': NO_MAPPING_STRING,
    'NCAAPropellerManufacturer': NO_MAPPING_STRING,
    'PropellerModel': NO_MAPPING_STRING,
    'NCAAPropellerModel': NO_MAPPING_STRING,
}

DEFAULT_MAPPING_PATH = Path('defaults/default_mapping.json')
