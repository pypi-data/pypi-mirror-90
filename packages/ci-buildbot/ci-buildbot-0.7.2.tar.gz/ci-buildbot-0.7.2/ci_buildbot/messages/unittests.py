from .mixins import (
    CodebuildMixin,
    GitMixin,
    Message,
    NameVersionMixin,
    UnittestReportGroupMixin,
)


class UnittestsStartMessage(CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'unittests_start.tpl'


class UnittestsSuccessMessage(UnittestReportGroupMixin, CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'unittests_success.tpl'


class UnittestsFailureMessage(UnittestReportGroupMixin, CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'unittests_failed.tpl'
