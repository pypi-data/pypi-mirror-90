##############################################################################
#
# Copyright (c) 2011 Projekt01 GmbH and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
$Id: converter.py 5005 2020-04-15 13:45:48Z rodrigo.ristow $
"""
__docformat__ = "reStructuredText"

import zope.i18n.format
import zope.component
import zope.schema.interfaces

import z3c.form.converter

from j01.datepickerzebra import interfaces


class ZebraDatePickerConverterBase(z3c.form.converter.BaseDataConverter):
    """A special data converter for IDatePickerWidget."""

    def __init__(self, field, widget):
        super(ZebraDatePickerConverterBase, self).__init__(field, widget)
        assert self.type == self.widget.formatterType
        self.formatter = self.widget.formatter

    def toWidgetValue(self, value):
        """See interfaces.IDataConverter"""
        if value is self.field.missing_value:
            return u''
        # format based on the widgets settings
        return self.widget.doFormat(value)


class ZebraDatePickerConverter(ZebraDatePickerConverterBase):
    """A special data converter for IDatePickerWidget."""

    zope.component.adapts(zope.schema.interfaces.IDate,
        interfaces.IZebraDatePickerWidget)

    type = 'date'

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        if value == u'':
            return self.field.missing_value
        try:
            # parse based on the widgets settings
            return self.widget.doParse(value)
        except zope.i18n.format.DateTimeParseError, err:
            raise z3c.form.converter.FormatterValidationError(err.args[0],
                value)


class ZebraDatePickerForDatetimeConverter(ZebraDatePickerConverterBase):
    """DatePicker date for datetime converter using no time in widget."""

    zope.component.adapts(zope.schema.interfaces.IDatetime,
        interfaces.IZebraDatePickerWidget)

    type = 'dateTime'

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        if value == u'':
            return self.field.missing_value
        try:
            # first append time string and enhance date pattern with time
            value = '%s %s' % (value, self.widget.timeAppendix)
            pattern = '%s H:M:S' % self.widget.dateFormatPattern
            # parse based on the widgets settings
            dt = self.widget.doParse(value, pattern=pattern)
            return dt.replace(tzinfo=self.widget.tzinfo)
        except zope.i18n.format.DateTimeParseError, err:
            try:
                self.formatter.format(value, self.widget.dateFormatPattern)
            except zope.i18n.format.DateTimeParseError, err:
                raise z3c.form.converter.FormatterValidationError(err.args[0],
                    value)


class ZebraDateTimePickerForDatetimeConverter(ZebraDatePickerConverterBase):
    """DatePicker date for datetime converter using no time in widget."""

    zope.component.adapts(zope.schema.interfaces.IDatetime,
        interfaces.IZebraDateTimePickerWidget)

    type = 'dateTime'

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        if value == u'':
            return self.field.missing_value
        try:
            # parse based on the widgets settings
            dt = self.widget.doParse(value)
            try:
                return dt.replace(tzinfo=self.widget.tzinfo)
            except TypeError:
                # TODO: Dirty fix when dt is a date and not a datetime.
                #  Saving a channel - TypeError: 'tzinfo' is an invalid keyword argument for this function
                from datetime import datetime
                return datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=self.widget.tzinfo)
        except zope.i18n.format.DateTimeParseError, err:
            try:
                self.widget.doFormat(value)
            except zope.i18n.format.DateTimeParseError, err:
                raise z3c.form.converter.FormatterValidationError(err.args[0],
                    value)
