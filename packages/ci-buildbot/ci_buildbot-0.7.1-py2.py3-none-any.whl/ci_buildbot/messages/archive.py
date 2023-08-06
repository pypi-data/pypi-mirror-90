
from .mixins import (
    CodebuildMixin,
    NameVersionMixin,
    GitMixin,
    GitChangelogMixin,
    Message
)


class ArchiveCodeMessage(GitChangelogMixin, CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'archive.tpl'
