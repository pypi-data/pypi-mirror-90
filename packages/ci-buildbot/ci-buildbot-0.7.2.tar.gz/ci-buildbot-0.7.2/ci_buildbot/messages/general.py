from typing import Dict

from .mixins import (
    AnnotationMixin,
    GitMixin,
    NameVersionMixin,
    CodebuildMixin,
    Message
)


class GeneralMixin(AnnotationMixin):

    def __init__(self, *args, **kwargs):
        self.label = None
        if 'label' in kwargs:
            self.label = kwargs['label']
            del kwargs['label']
        super().__init__()

    def annotate(self, values: Dict[str, str]):
        super().annotate(values)
        values['label'] = self.label


class GeneralStartMessage(GeneralMixin, CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'general_start.tpl'


class GeneralSuccessMessage(GeneralMixin, CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'general_success.tpl'


class GeneralFailureMessage(GeneralMixin, CodebuildMixin, GitMixin, NameVersionMixin, Message):
    template = 'general_failed.tpl'
