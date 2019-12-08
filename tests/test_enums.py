import datetime
import decimal
import ipaddress
import re
import uuid
from enum import auto

import pytest

from django_enum_ex import IntegerChoices,TextChoices,Choices
from django.test import SimpleTestCase
from django.utils.functional import Promise
from django.utils.translation import gettext_lazy as _


class Suit(IntegerChoices):
  DIAMOND = 1, _('Diamond')
  SPADE = 2, _('Spade')
  HEART = 3, _('Heart')
  CLUB = 4, _('Club')


class YearInSchool(TextChoices):
  FRESHMAN = 'FR', _('Freshman')
  SOPHOMORE = 'SO', _('Sophomore')
  JUNIOR = 'JR', _('Junior')
  SENIOR = 'SR', _('Senior')
  GRADUATE = 'GR', _('Graduate')


class Vehicle(IntegerChoices):
  CAR = 1, 'Carriage'
  TRUCK = 2
  JET_SKI = 3

  __empty__ = _('(Unknown)')


class Gender(TextChoices):
  MALE = 'M'
  FEMALE = 'F'
  NOT_SPECIFIED = 'X'

  __empty__ = '(Undeclared)'



def test_integerchoices():
  assert Suit.choices == [(1, 'Diamond'), (2, 'Spade'), (3, 'Heart'), (4, 'Club')]
  assert Suit.labels == ['Diamond', 'Spade', 'Heart', 'Club']
  assert Suit.values == [1, 2, 3, 4]
  assert Suit.names == ['DIAMOND', 'SPADE', 'HEART', 'CLUB']

  assert repr(Suit.DIAMOND) == '<Suit.DIAMOND: 1>'
  assert Suit.DIAMOND.label == 'Diamond'
  assert Suit.DIAMOND.value == 1
  assert Suit['DIAMOND'] == Suit.DIAMOND
  assert Suit(1) == Suit.DIAMOND

  assert isinstance(Suit, type(Choices))
  assert isinstance(Suit.DIAMOND, Suit)
  assert isinstance(Suit.DIAMOND.label, Promise)
  assert isinstance(Suit.DIAMOND.value, int)
  assert isinstance(Suit.DIAMOND, int)

def test_integerchoices_auto_label():
  assert Vehicle.CAR.label == 'Carriage'
  assert Vehicle.TRUCK.label == 'Truck'
  assert Vehicle.JET_SKI.label == 'Jet Ski'

def test_integerchoices_empty_label():
  assert Vehicle.choices[0] == (None, '(Unknown)')
  assert Vehicle.labels[0] == '(Unknown)'
  assert Vehicle.values[0] == None
  assert Vehicle.names[0] == '__empty__'

def test_integerchoices_functional_api():
  Place = IntegerChoices('Place', 'FIRST SECOND THIRD')
  assert Place.labels == ['First', 'Second', 'Third']
  assert Place.values == [1, 2, 3]
  assert Place.names == ['FIRST', 'SECOND', 'THIRD']

def test_integerchoices_containment():
  assert Suit.DIAMOND in Suit
  assert 1 in Suit
  assert 0 not in Suit

def test_textchoices():
  assert YearInSchool.choices == [
    ('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior'), ('GR', 'Graduate'),
  ]
  assert YearInSchool.labels == ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate']
  assert YearInSchool.values == ['FR', 'SO', 'JR', 'SR', 'GR']
  assert YearInSchool.names == ['FRESHMAN', 'SOPHOMORE', 'JUNIOR', 'SENIOR', 'GRADUATE']

  assert repr(YearInSchool.FRESHMAN) == "<YearInSchool.FRESHMAN: 'FR'>"
  assert YearInSchool.FRESHMAN.label == 'Freshman'
  assert YearInSchool.FRESHMAN.value == 'FR'
  assert YearInSchool['FRESHMAN'] == YearInSchool.FRESHMAN
  assert YearInSchool('FR') == YearInSchool.FRESHMAN

  assert isinstance(YearInSchool, type(Choices))
  assert isinstance(YearInSchool.FRESHMAN, YearInSchool)
  assert isinstance(YearInSchool.FRESHMAN.label, Promise)
  assert isinstance(YearInSchool.FRESHMAN.value, str)

def test_textchoices_auto_label():
  assert Gender.MALE.label ==  'Male'
  assert Gender.FEMALE.label == 'Female'
  assert Gender.NOT_SPECIFIED.label == 'Not Specified'

def test_textchoices_empty_label():
  assert Gender.choices[0] == (None, '(Undeclared)')
  assert Gender.labels[0] == '(Undeclared)'
  assert Gender.values[0] == None
  assert Gender.names[0] == '__empty__'

def test_textchoices_functional_api():
  Medal = TextChoices('Medal', 'GOLD SILVER BRONZE')
  assert Medal.labels == ['Gold', 'Silver', 'Bronze']
  assert Medal.values == ['GOLD', 'SILVER', 'BRONZE']
  assert Medal.names == ['GOLD', 'SILVER', 'BRONZE']

def test_textchoices_containment():
  assert YearInSchool.FRESHMAN in  YearInSchool
  assert 'FR' in  YearInSchool
  assert 'XX' not in YearInSchool

def test_textchoices_blank_value():
  class BlankStr(TextChoices):
    EMPTY = '', '(Empty)'
    ONE = 'ONE', 'One'

  assert BlankStr.labels == ['(Empty)', 'One']
  assert BlankStr.values == ['', 'ONE']
  assert BlankStr.names == ['EMPTY', 'ONE']

class Status(TextChoices):
  """上下线状态

  用于上下线的枚举
  """
  ONLINE = auto(), '上线'
  OFFLINE = auto(), '下线'

def test_textchoices_auto_value():
  assert Status.choices == [('ONLINE', '上线'), ('OFFLINE','下线')]
  assert Status.labels == ['上线','下线']
  assert Status.ONLINE.value == 'ONLINE'
  assert Status.OFFLINE.value == 'OFFLINE'
  assert Status.ONLINE.label == '上线'
  assert Status.OFFLINE.label == '下线'
  assert Status.names == ['ONLINE','OFFLINE']

def test_choices_of():
  assert Vehicle(1) == Vehicle.CAR
  assert Vehicle.of(1) == Vehicle.CAR
  assert YearInSchool.of('FR') == YearInSchool.FRESHMAN
  assert YearInSchool.of('fr') == YearInSchool.FRESHMAN
  assert YearInSchool.of(YearInSchool.JUNIOR) == YearInSchool.JUNIOR
  with pytest.raises(ValueError,match=re.escape("'fr' is not a valid YearInSchool")):
    YearInSchool('fr')

def test_choices_eq():
  assert 1 == Vehicle.CAR
  assert 'FR' == YearInSchool.FRESHMAN
  assert 'OFFLINE' == Status.OFFLINE
  assert 'ONLINE' == Status.ONLINE

def test_choices_get_class_label():
  assert Status.get_class_label() == "上下线状态"
  assert Gender.get_class_label() == 'An enumeration.'

def test_choices_of_raise():
  with pytest.raises(ValueError, match=re.escape("None 不是 '上下线状态' 的有效值")):
    Status.of(None, raise_if_none=True)
  with pytest.raises(ValueError, match=re.escape("off 不是 '上下线状态' 的有效值")):
    Status.of('off', raise_if_none=True)
  with pytest.raises(ValueError, match=re.escape("1 不是 '上下线状态' 的有效值")):
    Status.of(1, raise_if_none=True)

def test_choices_value_as_label():
  class Action(TextChoices):
    __value_as_label__ = True
    ADD = "增加"
    EDIT = "修改"

  assert Action.labels == ['增加','修改']
  assert Action.values == ['增加','修改']
  assert Action.ADD == '增加'
  assert Action.EDIT == '修改'




class TestCase(SimpleTestCase):
  def test_invalid_definition(self):
    msg = "'str' object cannot be interpreted as an integer"
    with self.assertRaisesMessage(TypeError, msg):
      class InvalidArgumentEnum(IntegerChoices):
        # A string is not permitted as the second argument to int().
        ONE = 1, 'X', 'Invalid'

    msg = "duplicate values found in <enum 'Fruit'>: PINEAPPLE -> APPLE"
    with self.assertRaisesMessage(ValueError, msg):
      class Fruit(IntegerChoices):
        APPLE = 1, 'Apple'
        PINEAPPLE = 1, 'Pineapple'

  def test_str(self):
    for test in [Gender, Suit, YearInSchool, Vehicle]:
      for member in test:
        with self.subTest(member=member):
          assert str(test[member.name]) == str(member.value)


class Separator(bytes, Choices):
  FS = b'\x1c', 'File Separator'
  GS = b'\x1d', 'Group Separator'
  RS = b'\x1e', 'Record Separator'
  US = b'\x1f', 'Unit Separator'


class Constants(float, Choices):
  PI = 3.141592653589793, 'π'
  TAU = 6.283185307179586, 'τ'


class Set(frozenset, Choices):
  A = {1, 2}
  B = {2, 3}
  UNION = A | B
  DIFFERENCE = A - B
  INTERSECTION = A & B


class MoonLandings(datetime.date, Choices):
  APOLLO_11 = 1969, 7, 20, 'Apollo 11 (Eagle)'
  APOLLO_12 = 1969, 11, 19, 'Apollo 12 (Intrepid)'
  APOLLO_14 = 1971, 2, 5, 'Apollo 14 (Antares)'
  APOLLO_15 = 1971, 7, 30, 'Apollo 15 (Falcon)'
  APOLLO_16 = 1972, 4, 21, 'Apollo 16 (Orion)'
  APOLLO_17 = 1972, 12, 11, 'Apollo 17 (Challenger)'


class DateAndTime(datetime.datetime, Choices):
  A = 2010, 10, 10, 10, 10, 10
  B = 2011, 11, 11, 11, 11, 11
  C = 2012, 12, 12, 12, 12, 12


class MealTimes(datetime.time, Choices):
  BREAKFAST = 7, 0
  LUNCH = 13, 0
  DINNER = 18, 30


class Frequency(datetime.timedelta, Choices):
  WEEK = 0, 0, 0, 0, 0, 0, 1, 'Week'
  DAY = 1, 'Day'
  HOUR = 0, 0, 0, 0, 0, 1, 'Hour'
  MINUTE = 0, 0, 0, 0, 1, 'Hour'
  SECOND = 0, 1, 'Second'


class Number(decimal.Decimal, Choices):
  E = 2.718281828459045, 'e'
  PI = '3.141592653589793', 'π'
  TAU = decimal.Decimal('6.283185307179586'), 'τ'


class IPv4Address(ipaddress.IPv4Address, Choices):
  LOCALHOST = '127.0.0.1', 'Localhost'
  GATEWAY = '192.168.0.1', 'Gateway'
  BROADCAST = '192.168.0.255', 'Broadcast'


class IPv6Address(ipaddress.IPv6Address, Choices):
  LOCALHOST = '::1', 'Localhost'
  UNSPECIFIED = '::', 'Unspecified'


class IPv4Network(ipaddress.IPv4Network, Choices):
  LOOPBACK = '127.0.0.0/8', 'Loopback'
  LINK_LOCAL = '169.254.0.0/16', 'Link-Local'
  PRIVATE_USE_A = '10.0.0.0/8', 'Private-Use (Class A)'


class IPv6Network(ipaddress.IPv6Network, Choices):
  LOOPBACK = '::1/128', 'Loopback'
  UNSPECIFIED = '::/128', 'Unspecified'
  UNIQUE_LOCAL = 'fc00::/7', 'Unique-Local'
  LINK_LOCAL_UNICAST = 'fe80::/10', 'Link-Local Unicast'


class CustomChoicesTests(SimpleTestCase):
  def test_labels_valid(self):
    enums = (
      Separator, Constants, Set, MoonLandings, DateAndTime, MealTimes,
      Frequency, Number, IPv4Address, IPv6Address, IPv4Network,
      IPv6Network,
    )
    for choice_enum in enums:
      with self.subTest(choice_enum.__name__):
        assert None not in  choice_enum.labels

  def test_bool_unsupported(self):
    msg = "type 'bool' is not an acceptable base type"
    with self.assertRaisesMessage(TypeError, msg):
      class Boolean(bool, Choices):
        pass

  def test_timezone_unsupported(self):
    msg = "type 'datetime.timezone' is not an acceptable base type"
    with self.assertRaisesMessage(TypeError, msg):
      class Timezone(datetime.timezone, Choices):
        pass

  def test_uuid_unsupported(self):
    msg = 'UUID objects are immutable'
    with self.assertRaisesMessage(TypeError, msg):
      class Identifier(uuid.UUID, Choices):
        A = '972ce4eb-a95f-4a56-9339-68c208a76f18'
