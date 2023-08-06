import dibuk
import hmac
import requests
import user_agents

from .version import VERSION
from base64 import b64decode
from datetime import datetime
from decimal import Decimal
from hashlib import md5, sha1
from time import mktime
from urllib.parse import urlencode


class Auth:
    def __init__(self):
        try:
            assert isinstance(dibuk.api_credentials, tuple)
            assert len(dibuk.api_credentials) == 2
        except AssertionError:
            raise dibuk.error.APIError(
                "Invalid credentials to Dibuk service provided (expected "
                "two-part tuple with `client_id` and `shared_secret`)."
            )

    def sign(self, data):
        encoded_data = []

        for key, value in data:
            encoded_data.append((key, str(value).encode("utf-8")))

        return hmac.new(
            b64decode(dibuk.api_credentials[1]),
            urlencode(encoded_data).encode("utf-8"),
            sha1,
        ).hexdigest()


class Requestor:
    OK = "OK"
    ERROR = "ERR"

    def request(self, method, data=[]):
        auth = Auth()

        fields = [
            ("a", method),
            ("v", dibuk.DIBUK_API_VERSION),
            ("did", dibuk.api_credentials[0]),
        ]

        fields.extend(data)
        fields.append(("ch", auth.sign(fields)))

        headers = {
            "User-Agent": "dibuk-python/" + VERSION,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            response = requests.post(
                url=dibuk.DIBUK_API_ENDPOINT,
                headers=headers,
                data=fields,
                timeout=80,
            )
        except Exception as e:
            self._handle_request_error(e)

        data = response.json()

        try:
            status = data["status"]
        except (KeyError, TypeError):
            raise dibuk.error.APIError(
                "Invalid response object from API: %s" % (response.text),
                response.text,
            )

        if status == self.ERROR:
            if data["eNum"] == 2007:
                if method == "export":
                    return status, []
                else:
                    raise dibuk.error.BookNotFoundError(
                        "Book not found", response.text
                    )

            raise dibuk.error.APIError("%s" % (data["eNum"]), response.text)

        if method not in ["available", "preview"]:
            try:
                data = data["id"] if method == "buy" else data["data"]
            except KeyError:
                raise dibuk.error.APIError(
                    "Invalid response object from API: %s" % data,
                    response.text,
                )

        return status, data

    def _handle_request_error(self, e):
        if isinstance(e, requests.exceptions.RequestException):
            err = "%s: %s" % (type(e).__name__, str(e))
        else:
            err = "A %s was raised" % (type(e).__name__,)

            if str(e):
                err += " with error message %s" % (str(e),)
            else:
                err += " with no error message"

        msg = "Network error: %s" % (err,)

        raise dibuk.error.APIConnectionError(msg)


class Book:
    INACTIVE = "inactive"
    ACTIVE = "active"

    def __init__(self, data={}):
        if data.get("status", "u") == "n":
            self.status = self.INACTIVE
        else:
            self.status = self.ACTIVE

        self.id = int(data.get("id"))
        self.language = data.get("lang")

        self.title = data.get("title")
        self.subtitle = data.get("subtitle")
        self.original_title = data.get("original_name", None)
        self.description = data.get("description", "")
        self.image_url = data.get("image", None)
        self.category_id = (
            int(data.get("cat_id")) if data.get("cat_id") else None
        )

        self.license_from = (
            datetime.fromtimestamp(int(data.get("license_from")))
            if data.get("license_from")
            else None
        )
        self.license_to = (
            datetime.fromtimestamp(int(data.get("license_to")))
            if data.get("license_to")
            else None
        )

        self.tags = list(
            filter(None, [tag.strip() for tag in data.get("tags").split(",")])
        )

        self.authors = list(
            filter(
                None,
                [
                    author.strip()
                    for author in data.get("author", "").split(",")
                ],
            )
        )

        self.print_edition = {
            "isbn": data.get("isbn"),
            "page_count": data.get("pages_cnt", None),
            "price": {
                "amount": Decimal(data.get("print_price")),
                "currency": data.get("currency"),
            },
        }

        try:
            self.print_edition["published_on"] = datetime.strptime(
                data.get("publish_date"), "%Y-%m-%d"
            )
        except ValueError:
            self.print_edition["published_on"] = None

        try:
            self.published_on = datetime.strptime(
                data.get("publish_date"), "%Y-%m-%d"
            )
        except ValueError:
            self.published_on = None

        try:
            self.epublished_on = datetime.strptime(
                data.get("epublish_date"), "%Y-%m-%d"
            )
        except ValueError:
            self.epublished_on = self.published_on

        self.price = {
            "amount": Decimal(data.get("price")),
            "currency": data.get("currency"),
        }

        self.publisher = {
            "id": int(data.get("publisher_id")),
            "name": data.get("publisher"),
        }

        self.samples = {}
        self.formats = []

        for file_format in [
            "acs_epub",
            "acs_pdf",
            "epub",
            "mobi",
            "pdf",
            "social_epub",
            "social_mobi",
            "social_pdf",
        ]:
            if file_format in data and data[file_format] == "1":
                self.formats.append(file_format)

                file_format_general = file_format.split("_")[-1]

                if (
                    "previews" in data
                    and file_format_general in data["previews"]
                ):
                    self.samples[file_format_general] = data["previews"][
                        file_format_general
                    ]

    @classmethod
    def get(self, book_id):
        client = Requestor()
        status, book = client.request("detail", [("book_id", book_id)])
        book = book[0]

        if book["status"] != "n":
            status, preview_data = client.request(
                "preview", [("book_id", book_id)]
            )
            if status == "OK":
                book["previews"] = preview_data.get("data", {})

        return Book(book)

    @classmethod
    def available(self, book_id, user_id):
        client = Requestor()
        status, response = client.request(
            "available", [("book_id", book_id), ("user_id", user_id)]
        )

        return True if status == "HAVEYET" else False


class Order:
    @classmethod
    def create(cls, books, user_id, metadata):
        if not isinstance(books, list):
            books = [books]

        client = Requestor()
        orders = {}

        for book in books:
            if not isinstance(book, tuple):
                continue

            status, data = client.request(
                "buy",
                [
                    ("book_id", book[0]),
                    ("user_id", user_id),
                    ("user_email", metadata.get("user_email", "")),
                    ("user_order", metadata.get("order_id", 0)),
                    ("seller_price", book[1]),
                    ("payment_channel", metadata.get("payment_channel", "")),
                    ("user_name", ""),
                    ("user_surname", ""),
                ],
            )

            if status in ["HAVEYET", "UNAVAIL"]:
                orders[book[0]] = {
                    "status": False,
                    "error": (data["eNum"], data["eMsg"]),
                }

            if status == "OK":
                orders[book[0]] = {"status": True, "order_id": int(data)}

        return orders

    @classmethod
    def get(cls, books, user_id, user_name="", user_surname="", user_email=""):
        def file_format(format_id):
            format_id = int(format_id)
            if format_id == 1:
                format = ("acs_epub", "application/epub+zip")
            elif format_id == 2:
                format = ("acs_pdf", "application/pdf")
            elif format_id == 3:
                format = ("epub", "application/epub+zip")
            elif format_id == 4:
                format = ("pdf", "application/pdf")
            elif format_id == 5:
                format = ("mobi", "application/x-mobipocket-ebook")
            elif format_id == 6:
                format = ("social_epub", "application/epub+zip")
            elif format_id == 7:
                format = ("social_pdf", "application/pdf")
            elif format_id == 8:
                format = ("social_mobi", "application/x-mobipocket-ebook")

            if format:
                return {"format": format[0], "mime_type": format[1]}

            return {}

        if not isinstance(books, list):
            books = [books]

        client = Requestor()
        download_links = {}

        if dibuk.user_agent:
            user_agent = md5(dibuk.user_agent.encode("utf-8")).hexdigest()
        else:
            user_agent = ""

        if dibuk.user_agent_is_mobile:
            user_agent_is_mobile = dibuk.user_agent_is_mobile
        else:
            user_agent_is_mobile = user_agents.parse(
                dibuk.user_agent
            ).is_mobile

        for book_id in books:
            status, data = client.request(
                "downloadLinks",
                [
                    ("book_id", book_id),
                    ("user_id", user_id),
                    ("for_mobile", 1 if user_agent_is_mobile is True else 0),
                    ("det", user_agent),
                    ("user_name", user_name),
                    ("user_surname", user_surname),
                    ("user_email", user_email),
                ],
            )

            download_links[book_id] = []

            for format_id, download_link in data.items():
                link = file_format(format_id)
                link["url"] = download_link

                download_links[book_id].append(link)

        return download_links


class Catalogue:
    @classmethod
    def all(cls, timestamp=None, include_previews=False):
        data = [("export", "catalog")]

        if isinstance(timestamp, datetime):
            data.append(("ts", int(mktime(timestamp.timetuple()))))
        elif isinstance(timestamp, int):
            data.append(("ts", timestamp))

        client = Requestor()
        status, response = client.request("export", data)

        books = {}

        for book in response:
            book_id = int(book["id"])

            if include_previews is True and book["status"] != "n":
                status, preview_data = client.request(
                    "preview", [("book_id", book_id)]
                )

                if status == "OK":
                    book["previews"] = preview_data.get("data", {})

            books[book_id] = Book(book)

        return books


class Category:
    def __init__(self, data):
        if not isinstance(data, dict):
            return

        self.id = data.get("id")
        self.parent_id = data.get("parent_id")
        self.name = data.get("name")

    @classmethod
    def all(cls):
        client = Requestor()
        status, data = client.request("export", [("export", "categories")])

        categories = {}

        for category in data:
            categories[int(category["id"])] = Category(category)

        return categories
