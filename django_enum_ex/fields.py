# coding: utf-8
from typing import Type, Union

from django import forms
from django.core.exceptions import ValidationError

from .enums import IntegerChoices, TextChoices

__author__ = "代码会说话"
from django.db import models

__all__ = ["IntegerChoicesField", "TextChoicesField"]


class ChoicesFieldMixin:
  def __init__(self, enum: Union[Type[IntegerChoices], Type[TextChoices]], *args, **kwargs):
    kwargs["choices"] = enum.choices
    self.enum = enum
    super(ChoicesFieldMixin, self).__init__(*args, **kwargs)

  def deconstruct(self):
    """字段解构方法,与 init 相对,用于在数据迁移时,将实例序列化.也即后面用来传递给 __init__ 的参数."""
    name, path, args, kwargs = super().deconstruct()
    kwargs["enum"] = self.enum
    if "choices" in kwargs:
      del kwargs["choices"]
    return name, path, args, kwargs

  def parse_raw_value(self, value):
    enum_item = self.enum.of(value,raise_if_none=False)
    if enum_item is None:
      enum_item = self.enum.db_fallback_item(value)
    if enum_item is None:
      raise ValidationError(f"{value} 不是{self.enum.get_class_label()}有效的枚举值")
    return enum_item

  def from_db_value(self, value, expression, connection):
    """如果此方法存在,会在从数据库加载数据时(包含values的聚合时)调用"""
    if value is None:
      return value
    return self.parse_raw_value(value)

  def to_python(self, value):
    """此方法会在反序列化,及 表单中的 clean() 阶段调用"""
    if value is None:
      return value
    raw_value = super().to_python(value)
    return self.parse_raw_value(raw_value)

  def get_prep_value(self, value):
    """可以在此方法中将 枚举对象转回成 对应枚举值"""
    if value is not None and isinstance(value, self.enum):
      return value.value
    return value

  def formfield(self, **kwargs):

    defaults = {
      "widget": forms.Select,
      "form_class": forms.TypedChoiceField,
      "choices": self.enum.choices,
    }
    if issubclass(self.enum, int):
      defaults["coerce"] = int
    defaults.update(kwargs)
    return super(ChoicesFieldMixin, self).formfield(**defaults)


class IntegerChoicesField(ChoicesFieldMixin, models.IntegerField):
  """限定值要求为 IntegerChoices 的字段类型"""

  description = "整型枚举字段"

  def __init__(self, enum: Type[IntegerChoices], *args, **kwargs):
    super(IntegerChoicesField, self).__init__(enum, *args, **kwargs)


class TextChoicesField(ChoicesFieldMixin, models.CharField):
  """限定值要求为 TextChoices 的字段类型"""

  description = "字符型枚举字段"

  def __init__(self, enum: Type[TextChoices], *args, **kwargs):
    super(TextChoicesField, self).__init__(enum, *args, **kwargs)
