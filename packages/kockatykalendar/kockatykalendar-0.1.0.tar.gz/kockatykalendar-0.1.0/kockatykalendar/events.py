import enum
import re
from datetime import date, datetime

hex_color_re = re.compile(r"^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$")


class EventScience(enum.Enum):
    MAT = "mat"
    FYZ = "fyz"
    INF = "inf"
    OTHER = "other"


class EventType(enum.Enum):
    SUTAZ = "sutaz"
    SEMINAR = "seminar"
    SUSTREDENIE = "sustredenie"
    VIKENDOVKA = "vikendovka"
    TABOR = "tabor"
    OLYMPIADA = "olympiada"
    PREDNASKY = "prednasky"
    OTHER = "other"


class EventContestant:
    class SchoolType(enum.Enum):
        ZAKLADNA = "zs"
        STREDNA = "ss"

    def __init__(self, type=None, year=None, raw=None):
        self.type = type
        self.year = year
        if raw:
            self.type = self.SchoolType(raw[0:2])
            self.year = int(raw[2])

    def validate(self):
        if not self.type:
            return
        if not self.year:
            raise ValueError("School year is required when school type is present.")
        if not isinstance(self.year, int):
            raise TypeError("School year should be an int, got %s." % type(self.year))
        if not isinstance(self.type, self.SchoolType):
            raise TypeError("Expected EventContestant.SchoolType, got %s." % type(self.type))

        if self.type == self.SchoolType.ZAKLADNA and (self.year < 1 or self.year > 9):
            raise ValueError("School year %d is invalid for this school type. Allowed 1-9." % self.year)
        if self.type == self.SchoolType.STREDNA and (self.year < 1 or self.year > 4):
            raise ValueError("School year %d is invalid for this school type. Allowed 1-4." % self.year)

    @property
    def raw(self):
        self.validate()
        if self.type:
            return "%s%d" % (self.type.value, self.year)

    def __eq__(self, other):
        if not isinstance(other, EventContestant):
            return False
        return self.type == other.type and self.year == other.year


class Event:
    class Dates:
        def __init__(self, start=None, end=None, text=None):
            self.start = start
            self.end = end
            self.text = text

        def validate(self):
            if not self.start:
                raise ValueError("Event start date is required.")
            if not isinstance(self.start, date):
                raise TypeError("Event start date must be instance of date or datetime.")
            if self.end and not isinstance(self.end, date):
                raise TypeError("Event end date must be instance of date or datetime.")

        def to_json(self) -> dict:
            self.validate()
            return {
                "start": self.start.strftime("%Y-%m-%d"),
                "end": self.end.strftime("%Y-%m-%d") if self.end else None,
                "text": self.text
            }

        @staticmethod
        def from_json(json: dict):
            d = Event.Dates()
            d.start = datetime.strptime(json["start"], "%Y-%m-%d").date()
            d.end = datetime.strptime(json["end"], "%Y-%m-%d").date() if "end" in json and json["end"] else None
            d.text = json["text"] if "text" in json else None
            return d

    class Contestants:
        def __init__(self, min=None, max=None):
            if not min:
                self.min = EventContestant()
            elif isinstance(min, str):
                self.min = EventContestant(raw=min)
            else:
                self.min = min
            if not max:
                self.max = EventContestant()
            elif isinstance(max, str):
                self.max = EventContestant(raw=max)
            else:
                self.max = max

        def validate(self):
            if not isinstance(self.min, EventContestant):
                raise TypeError("Expected EventContestant, got %s.", type(self.min))
            if not isinstance(self.max, EventContestant):
                raise TypeError("Expected EventContestant, got %s.", type(self.max))

        def to_json(self) -> dict:
            return {
                "min": self.min.raw,
                "max": self.max.raw
            }

        @staticmethod
        def from_json(json: dict):
            return Event.Contestants(json["min"], json["max"])

    def __init__(self, name="", sciences=[], type=None, oragnizers=[], places=[], volatile=False,
                 cancelled=False, info=None, color=None, link=None, date=None, contestants=None):
        # required
        self.name = name
        self.sciences = sciences
        self.type = type
        self.organizers = oragnizers
        self.places = places
        if date:
            self.date = date
        else:
            self.date = self.Dates()
        if contestants:
            self.contestants = contestants
        else:
            self.contestants = self.Contestants()

        # optional
        self.info = info
        self.color = color
        self.link = link
        self.volatile = volatile
        self.cancelled = cancelled

    def validate(self):
        if not self.name:
            raise ValueError("Event name is required.")
        if not isinstance(self.name, str):
            raise TypeError("Event name should be string.")

        # Sciences validation
        if not isinstance(self.sciences, list):
            raise TypeError("Event sciences should be a list, got %s." % type(self.sciences))
        if len(self.sciences) == 0:
            raise ValueError("Event must have at least 1 science.")
        for science in self.sciences:
            if not isinstance(science, EventScience):
                raise TypeError("Event science is not instance of EventScience: '%s'" % science)

        # Type validation
        if not self.type:
            raise ValueError("Event type is required.")
        if not isinstance(self.type, EventType):
            raise TypeError("Event type is not instance of EventType: '%s'" % self.type)

        # Places validation
        if not isinstance(self.places, list):
            raise TypeError("Event places should be a list.")
        if len(self.places) == 0:
            raise ValueError("Event must have at least 1 place.")
        for place in self.places:
            if not isinstance(place, str):
                raise TypeError("Place should be string: '%s'" % place)

        # Organizer validation
        if not isinstance(self.organizers, list):
            raise TypeError("Organizers should be a list of organizers, got %s." % type(self.organizers))
        if len(self.organizers) == 0:
            raise ValueError("Event must have at least 1 organizer.")
        for organizer in self.organizers:
            if not isinstance(organizer, str):
                raise TypeError("Oragnizer should be string: '%s'" % organizer)

        if not isinstance(self.date, self.Dates):
            raise TypeError("Event dates should be instance of Event.Dates.")
        self.date.validate()
        if not isinstance(self.contestants, self.Contestants):
            raise TypeError("Event dates should be instance of Event.Contestants.")
        self.contestants.validate()

        if self.info:
            if not isinstance(self.info, str):
                raise TypeError("Event info should be string.")
            if len(self.info) > 255:
                raise ValueError("Event info is too long. %d > 255" % len(self.info))
        if self.color:
            if not isinstance(self.color, str):
                raise TypeError("Event color should be string.")
            if self.color not in ["red", "orange", "yellow", "green", "blue", "purple"] and not hex_color_re.match(
                    self.color):
                raise ValueError("Event color is not valid.")
        if self.link:
            if not isinstance(self.link, str):
                raise TypeError("Event link should be string.")
            if self.link[0:4] != "http":
                raise ValueError("Event link should be a HTTP(s) URL.")
        if not isinstance(self.volatile, bool):
            raise TypeError("Volatile should be a bool, got %s." % type(self.volatile))
        if not isinstance(self.cancelled, bool):
            raise TypeError("Cancelled should be a bool, got %s." % type(self.cancelled))

    def to_json(self) -> dict:
        self.validate()
        return {
            "name": self.name.strip(),
            "sciences": [s.value for s in self.sciences],
            "type": self.type.value,
            "date": self.date.to_json(),
            "organizers": [o.strip() for o in self.organizers],
            "link": self.link.strip() if self.link else None,
            "places": self.places,
            "contestants": self.contestants.to_json(),
            "info": self.info,
            "color": self.color,
            "volatile": self.volatile,
            "cancelled": self.cancelled
        }

    @staticmethod
    def from_json(json: dict):
        e = Event()
        e.name = json["name"]
        e.sciences = [EventScience(s) for s in json["sciences"]]
        e.type = EventType(json["type"])
        e.date = Event.Dates.from_json(json["date"])
        e.organizers = json["organizers"]
        e.places = json["places"]
        e.contestants = Event.Contestants.from_json(json["contestants"])

        e.link = json["link"] if "link" in json else None
        e.info = json["info"] if "info" in json else None
        e.color = json["color"] if "color" in json else None
        e.volatile = json["volatile"] if "volatile" in json else False
        e.cancelled = json["cancelled"] if "cancelled" in json else False

        return e
