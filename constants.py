"""File containing all the constants used in the application."""

from pathlib import Path

APPLICATION_NAME = 'Aircraft DB Converter'
VERSION = '0.0.1'

X11_SYSTEM = 'x11'
WINDOWS_SYSTEM = 'win32'
MACOS_SYSTEM = 'aqua'

UI_REFRESH_TIME = 100 # The time in milliseconds to wait before refreshing the progress bars

# Default file paths
BASE_PATH = Path(__file__).parent.absolute()
HOME_PATH = Path.home().absolute() / 'AircraftDBConverter'
ORIGINAL_IRCA_INPUT_FILENAME = 'Original IRCA Input.txt.zip'
ORIGINAL_IRCA_INPUT_FILE_PATH = Path(f'{BASE_PATH}/defaults', ORIGINAL_IRCA_INPUT_FILENAME)
ORIGINAL_MAPPING_PATH = Path(f'{BASE_PATH}/defaults/default_mapping.json.zip')

# Default paths
DEFAULTS_PATH = Path(f'{HOME_PATH}/defaults')
DEFAULT_MAPPING_PATH = Path(f'{HOME_PATH}/defaults/default_mapping.json')

# Database path
DATABASE_PATH = Path(f'{HOME_PATH}/database')

# Icon file
ICON_FILE_PATH = Path(f'{BASE_PATH}/resources/icon_512x512.png')

# Docs path
DOCS_PATH = Path(f'{BASE_PATH}/site/index.html')

# Log path
LOG_PATH = Path(f'{HOME_PATH}/aircraft-db-converter-log.txt')

# Dialect settings
SNIFFER_READ_SIZE = 8192
DEFAULT_CURRENT_FILE_DELIMITER = '\t'
DEFAULT_NEW_FILE_DELIMITER = ','
DEFAULT_OUTPUT_FILE_DELIMITER = '\t'
DEFAULT_DELIMITERS = ',\t;'

# Custom events
ENABLE_MENU_ITEMS_EVENT = '<<EnableMenuItems>>'
MAPPING_ACCEPTED_EVENT = '<<MappingAccepted>>'
MAPPING_REJECTED_EVENT = '<<MappingRejected>>'
COMBOBOX_SELECTED_EVENT = '<<ComboboxSelected>>'

# Layout constants for mapping dialog
MAPPING_DIALOG_COLUMNS = 3
MAPPING_DIALOG_ITEMS_PER_COLUMN = 2

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
