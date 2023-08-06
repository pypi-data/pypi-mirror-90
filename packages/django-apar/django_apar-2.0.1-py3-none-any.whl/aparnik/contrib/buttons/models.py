# -*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext as _

from colorfield.fields import ColorField

from aparnik.contrib.basemodels.models import BaseModel, BaseModelManager
from aparnik.contrib.filefields.models import FileField
from aparnik.contrib.segments.models import BaseSegment, BaseSegmentManager


class ButtonManager(BaseModelManager):
    def get_queryset(self):
        return super(ButtonManager, self).get_queryset()


class Button(BaseModel):

    title = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Title'))
    icon = models.ForeignKey(FileField, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Icon'))
    background_color = ColorField(default='#2672DF', verbose_name=_('Background Color'))
    icon_color = ColorField(default='#2672DF', verbose_name=_('Icon color'))
    title_color = ColorField(default='#2672DF', verbose_name=_('Title color'))
    model_obj = models.ForeignKey(BaseModel, related_name='button_model', on_delete=models.CASCADE, verbose_name=_('Model'))

    objects = ButtonManager()

    def __str__(self):
        return '%s %s' % (self.id, self.title)

    class Meta:
        verbose_name = _('Button')
        verbose_name_plural = _('Buttons')


# Button Segment Model
class ButtonSegmentManager(BaseSegmentManager):

    def get_queryset(self):
        return super(BaseSegmentManager, self).get_queryset()


class ButtonSegment(BaseSegment):

    objects = ButtonSegmentManager()

    def __str__(self):
        return super(ButtonSegment, self).__str__()

    class Meta:
        verbose_name = _('Button Segment')
        verbose_name_plural = _('Button Segments')
