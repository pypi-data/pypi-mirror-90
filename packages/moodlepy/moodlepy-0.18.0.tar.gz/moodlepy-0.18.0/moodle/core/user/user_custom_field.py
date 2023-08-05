from dataclasses import dataclass, field
from typing import Optional

from moodle.base.general import GeneralTypeValue


@dataclass
class UserCustomField(GeneralTypeValue):
    """User custom fields (also known as user profil fields)

    Args:
        type (str): The name of the custom field
        value (str): The value of the custom field
        name (Optional[str]): The name of the custom field
        shortname (Optional[str]): The shortname of the custom field - to be able to build the field class in the code
    """
    name: Optional[str] = field(default=None)
    shortname: Optional[str] = field(default=None)
