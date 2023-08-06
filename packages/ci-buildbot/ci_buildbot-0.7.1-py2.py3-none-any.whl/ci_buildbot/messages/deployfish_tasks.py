from .mixins import (
    GitMixin,
    NameVersionMixin,
    CodebuildMixin,
    DeployfishTasksDeployMixin,
    Message
)


class DeployfishTasksDeployStartMessage(DeployfishTasksDeployMixin, CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'deploy_tasks_start.tpl'


class DeployfishTasksDeploySuccessMessage(DeployfishTasksDeployMixin, CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'deploy_tasks_success.tpl'


class DeployfishTasksDeployFailureMessage(DeployfishTasksDeployMixin, CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'deploy_tasks_failed.tpl'
