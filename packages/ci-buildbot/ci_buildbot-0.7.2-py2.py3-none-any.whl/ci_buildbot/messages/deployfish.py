from .mixins import (
    GitMixin,
    NameVersionMixin,
    CodebuildMixin,
    DeployfishDeployMixin,
    Message
)


class DeployfishDeployStartMessage(DeployfishDeployMixin, CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'deploy_start.tpl'


class DeployfishDeploySuccessMessage(DeployfishDeployMixin, CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'deploy_success.tpl'


class DeployfishDeployFailureMessage(DeployfishDeployMixin, CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'deploy_failed.tpl'
