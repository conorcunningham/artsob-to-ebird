from .artsob import Artsob
from .utils import get_logger

logger = get_logger(__name__)


class Ebird:
    headings = (
        "Common Name",
        "Genus",
        "Species",
        "Number",
        "Comments",
        "Location Name",
        "Latitude",
        "Longitude",
        "Date",
        "Start Time",
        "State/Province",
        "Country Code",
        "Protocol",
        "Number of Observers",
        "Duration",
        "All observations reported?",
        "Effort Distance Miles",
        "Effort area acres",
        "Submission Comments",
    )


class EBirdRecord:
    valid: bool = False

    def __init__(self, species, artsob: Artsob):

        # these fields are statically set
        # self.headings will dynamically add this dict
        self.fields = {
            "Country Code": "NO",
            "Protocol": "stationary",
            "All observations reported?": "Yes",
            "Submission Comments": "Imported from Artsob (Norway)",
            "Effort area acres": None,
            "Effort Distance Miles": None,
            "Genus": None,
            "Species": None,
            "Latitude": None,
            "Longitude": None,
            "State/Province": "NO",
        }

        # these are the value which we will get
        # from the artsob record
        self.headings = {
            "count": "Number",
            "comments": "Comments",
            "location": "Location Name",
            "latitude": "Latitude",
            "longitude": "Longitude",
            "start_date": "Date",
            "start_time": "Start Time",
            # "state": "State/Province",
            "observers": "Number of Observers",
            "duration": "Duration",
            # "norwegian": "Common Name"
        }

        self.species = species
        self.artsob = artsob
        self.valid = True

        self.find_bird_name()
        for artsob, ebird in self.headings.items():
            self.fields[ebird] = getattr(self.artsob, artsob, None)

    # find and assign common, species and genus names
    def find_bird_name(self):
        common_name = self.species.get(self.artsob.latin, None)
        if common_name is None:
            logger.error(f"No species found in lookup table for {self.artsob.latin}")
            self.valid = False
        else:
            self.fields["Common Name"] = common_name["comName"]
            self.valid = True
