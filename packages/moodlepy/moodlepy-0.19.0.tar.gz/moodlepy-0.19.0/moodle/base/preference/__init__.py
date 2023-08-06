from dataclasses import dataclass, field
from typing import List
from moodle import MoodleWarning
from .preference_component import PreferenceComponent
from .preference_processor import PreferenceProcessor
from .preference_user import PreferenceUser


@dataclass
class Preference:
    userid: int
    disableall: int
    processors: List[PreferenceProcessor] = field(default_factory=list)
    components: List[PreferenceComponent] = field(default_factory=list)


@dataclass
class NotificationPreference:
    preferences: Preference
    warnings: List[MoodleWarning] = field(default_factory=list)


@dataclass
class MessagePreference:
    preferences: Preference
    blocknoncontacts: int
    entertosend: bool
    warnings: List[MoodleWarning] = field(default_factory=list)


@dataclass
class UserPreference:
    prefereces: List[PreferenceUser] = field(default_factory=list)
    warnings: List[MoodleWarning] = field(default_factory=list)
