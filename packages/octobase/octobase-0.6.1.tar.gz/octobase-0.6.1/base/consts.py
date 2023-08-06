#!/opt/local/bin/python
# Copyright 2018, Octoboxy LLC.  All Rights Reserved.

import base
import datetime
#import pytz


### Timezones

TIME_UTC                = None          # XYZZY: pytz.utc
TIME_ZONE               = None          # Filled in during Boot(), after settings are processed.


### DateTimes

# We add/subtract one day from date min/max so they can be localized without overflowing
DATE_MIN                = datetime.date.min + datetime.timedelta(days=1)
DATE_MAX                = datetime.date.max - datetime.timedelta(days=1)
DATETIME_MIN            = datetime.datetime.min.replace(tzinfo=TIME_UTC) + datetime.timedelta(days=1)
DATETIME_MAX            = datetime.datetime.max.replace(tzinfo=TIME_UTC) - datetime.timedelta(days=1)


### Field sizes

MAX_LENGTH_KEY          =  32
MAX_LENGTH_SLUG         =  base.utils.strings.MAX_LENGTH_SLUG   #  64
MAX_LENGTH_TITLE        =  96
MAX_LENGTH_FILEPATH     = 255
MAX_LENGTH_IDENTIFIER   = 255
MAX_LENGTH_RECAPTCHA    = 740



### Quotes

# All the standard unicode quote marks
base.Enum.Define(('QUOTE', 'Quotes'), (
    ('Quotation Mark',                '"'),
    ('Apostrophe',                    "'"),
    ('Grave Accent',                  '`'),
    ('Acute Accent',                  '´'),
    ('Left Single Quotation Mark',    '‘'),
    ('Right Single Quotation Mark',   '’'),
    ('Left Double Quotation Mark',    '“'),
    ('Right Double Quotation Mark',   '”'),
))
