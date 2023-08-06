from datetime import date
from typing import List

import requests

from kockatykalendar.events import Event


class Dataset:
    """
    Represents a dataset file in KockatyKalendar data.
    One dataset file holds information about one school year.
    """
    def __init__(self, json):
        self.start_year = json["start_year"]
        self.end_year = json["end_year"]
        self.school_year = json["school_year"]
        self.filename = json["filename"]
        self.url = "https://data.kockatykalendar.sk/%s" % self.filename


def get_available_datasets() -> List[Dataset]:
    """
    Load list of datasets from KockatyKalendar.
    :return: List of available datasets
    """
    res = requests.get("https://data.kockatykalendar.sk/index.json")
    if res.status_code != 200:
        raise ConnectionError("KockatyKalendar.sk API returned wrong status code. 200 != %d." % res.status_code)

    return [Dataset(ds) for ds in res.json()]


def get_current_dataset() -> Dataset:
    """
    Predicts dataset of current school year.
    Should be accurate, however we recommend using get_available_datasets() and choosing
    a dataset from there, as it is based on real dataset index.
    :return: Predicted current school year dataset
    """
    today = date.today()
    current_school_year = today.year if today.month >= 9 else today.year - 1
    school_year = "%d/%d" % (current_school_year, current_school_year + 1),
    filename = "%d_%d.json" % (current_school_year, (current_school_year + 1) % 100),

    return Dataset({
        "start_year": current_school_year,
        "end_year": current_school_year + 1,
        "school_year": school_year,
        "filename": filename
    })


def get_events(dataset) -> List[Event]:
    """
    Get events for given dataset from KockatyKalendar API.
    :param dataset: Dataset instance, filename or URL of the dataset
    :return: List of all events in a dataset
    """
    if isinstance(dataset, Dataset):
        url = dataset.url
    elif isinstance(dataset, str):
        if dataset[0:4] == "http":
            url = dataset
        else:
            url = "https://data.kockatykalendar.sk/%s" % dataset
    else:
        raise TypeError("Dataset should be a str or Dataset object.")

    res = requests.get(url)
    if res.status_code == 404:
        return []
    if res.status_code != 200:
        raise ConnectionError("KockatyKalendar.sk API returned wrong status code. 200 != %d." % res.status_code)

    return [Event.from_json(e) for e in res.json()]
