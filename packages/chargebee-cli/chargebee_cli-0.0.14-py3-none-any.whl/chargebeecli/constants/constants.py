import enum


class Formats(enum.Enum):
    JSON = 'json'
    TABLE = 'table'


class ApiOperation(enum.Enum):
    LIST = 'list'
    FETCH = 'fetch'
    CREATE = 'create'
    DELETE = 'delete'
    UPDATE = 'update'


class Profile(enum.Enum):
    API_KEY = 'api_key'
    ACCOUNT = 'account'
