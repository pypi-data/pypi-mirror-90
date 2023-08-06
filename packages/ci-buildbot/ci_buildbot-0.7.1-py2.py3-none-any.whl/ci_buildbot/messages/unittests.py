from .mixins import (
    NameVersionMixin,
    GitMixin,
    CodebuildMixin,
    Message
)


class UnittestsStartMessage(CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'unittests_start.tpl'


class UnittestsSuccessMessage(CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'unittests_success.tpl'


class UnittestsFailureMessage(CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'unittests_failed.tpl'
