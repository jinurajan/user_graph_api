

class StatusCode:
    STATUS_BAD_REQUEST = 400
    STATUS_PERMISSION_ERROR = 403
    STATUS_NOT_FOUND = 404
    STATUS_NOT_ALLOWED = 405
    STATUS_CONFLICT_ERROR = 409
    STATUS_INTERNAL_SERVER_ERROR = 500


class CassandraKeySpaces:
    USERDB = "userdb"


class UserAPIConstants:
    DEFAULT_PAGE_LIMIT = 20
    DEFAULT_PAGE_OFFSET = 0