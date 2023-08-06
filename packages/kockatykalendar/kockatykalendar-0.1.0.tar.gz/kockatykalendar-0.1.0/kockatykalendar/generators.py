from typing import Iterable, List

from kockatykalendar.events import Event


class CalendarGenerator:
    def items(self) -> Iterable:
        raise NotImplementedError()

    def event(self, item) -> Event:
        raise NotImplementedError()

    def generate(self) -> List[Event]:
        data = []
        for item in self.items():
            event = self.event(item)
            if not isinstance(event, Event):
                raise TypeError("Expected Event, got %s." % type(event))
            data.append(event)
        return data

    def to_json(self) -> List[dict]:
        data = []
        for item in self.generate():
            data.append(item.to_json())
        return data
