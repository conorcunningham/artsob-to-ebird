import datetime
import pandas as pd
from typing import NamedTuple
from pyproj import Proj


class TimeRecord(NamedTuple):
    start_date: datetime.date
    start_time: datetime.time
    location: str


class Artsob:
    latin: str
    count: int
    start_date: datetime.date
    start_time: datetime.time
    end_date: datetime.date
    end_time: datetime.time
    reporter: str
    observers: list
    comments: str
    location: str
    latitude: str
    longitude: str
    state: str
    duration: int = 60
    wgs_string: str
    id: int

    def __init__(self, row, observer: str = "Conor Cunningham"):
        self.reporter = observer
        self.fields = (
            ("Vitenskapelig navn", "latin"),
            ("Artsnavn", "norwegian"),
            ("Antall", "count"),
            ("Startdato", "start_date"),
            ("Stattidspunkt", "start_time"),
            ("Sluttdato", "end_date"),
            ("Sluttidspunkt", "end_time"),
            ("Rapportør", "reporter"),
            ("Observatører", "observers"),
            ("Privat kommentar", "comments"),
            ("Lokalitetsnavn", "location"),
            ("Kommentar", "comments"),
            ("Fylke", "state"),
            # ("Østkoordinat", "longitude"),
            # ("Nordkoordinat", "latitude"),
            ("Id", "id"),
            ("Originale koordinater", "wgs_string"),
        )
        self.build_object(row)

    def build_object(self, row):
        for pair in self.fields:
            norsk = pair[0]
            english = pair[1]
            if "date" in english:
                value = self.parse_date(row[norsk])
            elif "time" in english:
                value = self.parse_time(row[norsk])
            elif "observers" in english:
                value = self.parse_observers(row[norsk])
            elif "reporter" in english:
                value = self.reporter
            elif "location" in english:
                value = self.parse_location(row[norsk])
            else:
                value = self.parse_csv_cell(row[norsk])

            setattr(self, english, value)

            if "wgs_string" in english:
                cleaned_cell = self.parse_csv_cell(row[norsk])
                self.longitude, self.latitude = self.parse_coordinates(cleaned_cell)

    @staticmethod
    def parse_location(value):
        if "," in value:
            location = value.split(",")
            return location[0].strip()
        elif "(" in value:
            location = value.split("(")
            return location[0].strip()
        else:
            return value.strip()

    @staticmethod
    def parse_observers(value):
        if not pd.isna(value):
            clean_value = value.replace(" ", "").strip()
            return len(clean_value.split(","))
        return 1

    @staticmethod
    def parse_csv_cell(value):
        if pd.isna(value):
            return None
        if isinstance(value, str):
            return value.strip()
        if value == "":
            return None
        return value

    @staticmethod
    def parse_date(text):
        datestamp = text.split()[0]
        if "/" in datestamp:
            digits = [int(d) for d in datestamp.split("/")]
        else:
            digits = [int(d) for d in datestamp.split("-")]
        return datetime.date(digits[0], digits[1], digits[2])  # .strftime("%m/%d/%y")

    @staticmethod
    def parse_time(text):
        if isinstance(text, pd.Timestamp):
            text = str(text)
        if not pd.isna(text):
            time_parts = [int(part) for part in text.split(":")]
            return datetime.time(hour=time_parts[0], minute=time_parts[1])  # .strftime("%H:%M")

    def parse_coordinates(self, text: str):
        text = self.parse_csv_cell(text)
        if text is None or text == "" or pd.isna(text):
            return None, None
        if text.startswith("32V"):
            return None, None

        replace = ("N", ",", "Ø")
        coord_text = text
        for char in replace:
            coord_text = coord_text.replace(char, "")
        parts = coord_text.split()
        x = int(parts[0])
        y = int(parts[1])

        # convert wgs to decimal
        myProj = Proj("+proj=utm +zone=33, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
        longitude, latitude = myProj(x, y, inverse=True)
        longitude = round(longitude, 7)
        latitude = round(latitude, 7)
        return longitude, latitude


class ArtsobRecords:
    """
    This is a class to store all of the artsob records for a user.
    """

    records: set[Artsob]
    date_lookup = {"placeholder": {}}
    location_lookup = {"placeholder": {}}

    def __init__(self, records):
        self.records = set(records)
        self.existing_records = set()
        self.generate_time_records()

    def generate_time_records(self):
        for record in self.records:
            if record.id in self.existing_records:
                self.records.remove(record)
                print(f"Duplicate in artsob: {record.id}")
                continue

            duration = self.calculate_duration(record)
            if duration != 0:
                record.duration = duration
            else:
                record.duration = 60

            start_date = record.start_date.strftime("%m/%d/%y")
            time_record = TimeRecord(record.start_date, record.start_time, record.location)
            location_time = self.location_lookup.get(time_record.location, None)

            if location_time is None and time_record.start_time is not None:
                self.location_lookup[record.location] = {}
                self.location_lookup[record.location][start_date] = time_record.start_time.strftime(
                    "%H:%M"
                )
            elif time_record.start_time is not None:
                self.location_lookup[record.location][start_date] = time_record.start_time.strftime(
                    "%H:%M"
                )

        # mark method as have being run
        setattr(self, "time_records", True)
        self.update_times()

    def update_times(self):
        assert hasattr(
            self, "time_records"
        ), "You must call generate_time_records() before calling update_times()"
        for record in self.records:
            if record.start_time is None or record.start_time == "":
                self.assign_start_time(record)

            # convert dates to correct string format
            record.start_date = record.start_date.strftime("%m/%d/%Y")
            record.end_date = record.end_date.strftime("%m/%d/%Y")
            if isinstance(record.start_time, datetime.time):
                record.start_time = record.start_time.strftime("%H:%M")

    def assign_start_time(self, record: Artsob):
        try:
            location_time = self.location_lookup.get(record.location, None)
            if location_time is not None and location_time != "":
                record.start_time = location_time[record.start_date.strftime("%m/%d/%Y")]
            else:
                record.start_time = "08:00"
        except KeyError:
            record.start_time = "08:00"

    @staticmethod
    def calculate_duration(record: Artsob):
        if record.start_time is not None and record.end_time is not None:
            start_date = datetime.datetime.combine(record.start_date, record.start_time)
            finish_date = datetime.datetime.combine(record.end_date, record.end_time)
            time_delta = finish_date - start_date
            total_seconds = time_delta.total_seconds()
            return int(round(total_seconds / 60, 0))
        return 60
