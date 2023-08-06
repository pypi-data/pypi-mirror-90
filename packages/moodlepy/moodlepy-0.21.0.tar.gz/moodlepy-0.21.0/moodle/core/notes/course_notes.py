from typing import List, Optional

from moodle import MoodleWarning, ResponsesFactory
from moodle.attr import dataclass, fields
from . import SiteNote, CourseNote, PersonalNote


@dataclass
class CourseNotes(ResponsesFactory[CourseNote]):
    """Course Notes
    Constructor arguments:
    params: sitenotes (List[SiteNote]): site notes
    params: coursenotes (List[CourseNote]): couse notes
    params: personalnotes (List[PersonalNote]): personal notes
    params: canmanagesystemnotes (Optional[int]): Whether the user can manage notes at system level.
    params: canmanagecoursenotes (Optional[int]): Whether the user can manage notes at the given course.
    params: warnings (List[Warning]): list of warnings
    """
    sitenotes: List[SiteNote] = fields(SiteNote)
    coursenotes: List[CourseNote] = fields(CourseNote)
    personalnotes: List[PersonalNote] = fields(PersonalNote)
    canmanagesystemnotes: Optional[int] = None
    canmanagecoursenotes: Optional[int] = None
    warnings: List[MoodleWarning] = fields(MoodleWarning)

    @property
    def items(self) -> List[CourseNote]:
        return self.coursenotes
