from .db_utils import *
from .scheduler import *

connection = get_connection()
scheduler = start_task(connection)

