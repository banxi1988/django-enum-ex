import pytest
from django.core.exceptions import ValidationError

from django_enum_ex import IntegerChoices, TextChoices ,IntegerChoicesField,TextChoicesField


class DemoType(IntegerChoices):
  NORMAL = 1, "正常"
  MEDIUM = 2, "中等"


class DemoStatus(TextChoices):
  NORMAL = "normal", "正常"
  GOOD = "good", "好"


def test_enum_field():
  type = IntegerChoicesField(DemoType, verbose_name="类型", default=DemoType.NORMAL)
  status = TextChoicesField(DemoStatus, verbose_name="状态", default=DemoStatus.NORMAL)

  assert type.get_prep_value(DemoType.NORMAL) == 1
  assert type.get_prep_value(1) == 1

  assert type.from_db_value(1, None, None) == DemoType.NORMAL
  assert type.from_db_value(None, None, None) is None
  assert type.to_python("1") == DemoType.NORMAL
  assert type.to_python(1) == DemoType.NORMAL
  assert type.to_python(None) is None
  with pytest.raises(ValidationError):
    type.to_python('bad_enum_value')

  assert status.from_db_value("good", None, None) == DemoStatus.GOOD
  assert status.from_db_value(None, None, None) is None
  assert status.to_python("good") == DemoStatus.GOOD
  assert status.to_python(None) is None
  with pytest.raises(ValidationError):
    status.to_python("bad_enum_value")
  assert status.get_prep_value("good") == "good"
  assert status.get_prep_value(DemoStatus.GOOD) == "good"

  status.deconstruct()
  type.deconstruct()

  status.formfield()
  type.formfield()