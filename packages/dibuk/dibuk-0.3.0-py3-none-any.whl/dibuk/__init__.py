from .error import (  # noqa: F401
    APIConnectionError,
    APIError,
    BookNotFoundError,
    DibukError,
)
from .resource import Book, Catalogue, Category, Order  # noqa: F401

# Configuration variables
api_credentials = None
user_agent = ""
user_agent_is_mobile = False

DIBUK_API_VERSION = "2.1"
DIBUK_API_ENDPOINT = "https://agregator.dibuk.eu/2_1/call.php"
