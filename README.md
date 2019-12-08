# django-enum-ex
一个基于 Django 3.0 Choices 枚举类型的独立扩展包

本库基于 Django 3.0 中自带的 [django.db.models.enum ](https://github.com/django/django/blob/master/django/db/models/enums.py)


特色
---------------

- 支持将枚举字段名自设置为值. 设置值为 `enum.auto()`
- 支持将单一值即设置为值,又设置为 `label`, 通过设置类属性 `__value_as_label__ = True`
- 增加 `Choices.of` 方法,在将原始值转成枚举值时,支持忽略大小定. 支持没有匹配枚举值时,抛出错误.
- 增加 `IntegerChoicesField` 和 `TextChoicesField` 两个Model Field