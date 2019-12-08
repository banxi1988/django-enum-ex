import enum
from typing import Any, Union

from django.utils.functional import Promise

__all__ = ['Choices', 'IntegerChoices', 'TextChoices']

"""
本模块主要来自:
https://github.com/django/django/blob/master/django/db/models/enums.py
"""


class ChoicesMeta(enum.EnumMeta):
  """用于创建 Choices 枚举的元类"""

  def __new__(metacls, classname, bases, classdict):
    labels = []
    value_as_label = classdict.pop('__value_as_label__', False)
    for key in classdict._member_names:
      args = classdict[key]
      if (
          isinstance(args, (list, tuple)) and
          len(args) > 1 and
          isinstance(args[-1], (Promise, str))
      ):
        if len(args) == 2 and isinstance(args[0],enum.auto):
          value = key
          label = args[1]
        else:
          *value, label = args
          value = tuple(value)
      else:
        value = args
        if value_as_label:
          label = value
        else:
          label = key.replace('_', ' ').title()
      labels.append(label)
      # Use dict.__setitem__() to suppress defenses against double
      # assignment in enum's classdict.
      dict.__setitem__(classdict, key, value)
    cls = super().__new__(metacls, classname, bases, classdict)
    cls._value2label_map_ = dict(zip(cls._value2member_map_, labels))
    # Add a label property to instances of enum which uses the enum member
    # that is passed in as "self" as the value to use when looking up the
    # label in the choices.
    cls.label = property(lambda self: cls._value2label_map_.get(self.value))
    return enum.unique(cls)

  def __contains__(cls, member):
    if not isinstance(member, enum.Enum):
      # Allow non-enums to match against member values.
      return member in {x.value for x in cls}
    return super().__contains__(member)

  @property
  def names(cls):
    empty = ['__empty__'] if hasattr(cls, '__empty__') else []
    return empty + [member.name for member in cls]

  @property
  def choices(cls):
    empty = [(None, cls.__empty__)] if hasattr(cls, '__empty__') else []
    return empty + [(member.value, member.label) for member in cls]

  @property
  def labels(cls):
    return [label for _, label in cls.choices]

  @property
  def values(cls):
    return [value for value, _ in cls.choices]





class Choices(enum.Enum, metaclass=ChoicesMeta):
  """Class for creating enumerated choices."""

  def __str__(self):
    """
    Use value when cast to str, so that Choices set as model instance
    attributes are rendered as expected in templates and similar contexts.
    """
    return str(self.value)

  @classmethod
  def of(cls,value:Any,raise_if_none:bool=False):
    """
    提供一个比 Choices 构造函数更宽容的函数.对于字符串可以忽略大小写
    :param value: 枚举原始值,或者枚举本身
    :return: 枚举对于,如果找不到对应枚举,可以返回 None
    """
    if value is not  None:
      if isinstance(value,cls):
        return value
      if issubclass(cls, str) and isinstance(value,str):
        lower = value.lower()
        for enum_item in cls:
          if enum_item.value.lower() == lower:
            return enum_item
      else:
        for enum_item in cls:
          if enum_item.value == value:
            return enum_item
    if raise_if_none:
      raise ValueError(f"{value} 不是 '{cls.get_class_label()}' 的有效值")

  @classmethod
  def get_class_label(cls):
    # EnumMeta 提供了默认的 __doc__ 'An enumeration.'
    doc = cls.__doc__
    lines = doc.splitlines()
    return lines[0].strip()

  @classmethod
  def db_fallback_item(cls,value:Any):
    """可以为从数据库读取回来的异常值提供一个 fallback,方便兼容老的数据"""
    pass



class IntegerChoices(int, Choices):
  """Class for creating enumerated integer choices."""

  @classmethod
  def of(cls,value:Union['IntegerChoices',int],raise_if_none:bool=False):
    return super().of(value,raise_if_none)

class TextChoices(str, Choices):
  """Class for creating enumerated string choices."""

  @classmethod
  def of(cls,value:Union['TextChoices',str],raise_if_none:bool=False):
    return super().of(value,raise_if_none)

  def _generate_next_value_(name, start, count, last_values):
    return name
