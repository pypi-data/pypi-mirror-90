from moodle import BaseMoodle
from moodle.utils.decorator import lazy
from . import (
    BaseAssign,
    BaseFolder,
    BaseForum,
    BaseLesson,
    BaseResource,
    BaseUrl,
)


class Mod(BaseMoodle):
    @property  # type: ignore
    @lazy
    def assign(self) -> BaseAssign:
        return BaseAssign(self.moodle)

    @property  # type: ignore
    @lazy
    def folder(self) -> BaseFolder:
        return BaseFolder(self.moodle)

    @property  # type: ignore
    @lazy
    def forum(self) -> BaseForum:
        return BaseForum(self.moodle)

    @property  # type: ignore
    @lazy
    def lesson(self) -> BaseLesson:
        return BaseLesson(self.moodle)

    @property  # type: ignore
    @lazy
    def resource(self) -> BaseResource:
        return BaseResource(self.moodle)

    @property  # type: ignore
    @lazy
    def url(self) -> BaseUrl:
        return BaseUrl(self.moodle)
