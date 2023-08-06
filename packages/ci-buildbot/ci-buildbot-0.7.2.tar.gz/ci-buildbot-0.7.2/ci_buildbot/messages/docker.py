from .mixins import (
    NameVersionMixin,
    GitMixin,
    CodebuildMixin,
    DockerMixin,
    DockerImageNameMixin,
    Message
)


class DockerStartMessage(DockerImageNameMixin, CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'docker_start.tpl'


class DockerSuccessMessage(DockerImageNameMixin, DockerMixin, CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'docker_success.tpl'


class DockerFailureMessage(DockerImageNameMixin, CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'docker_failed.tpl'
