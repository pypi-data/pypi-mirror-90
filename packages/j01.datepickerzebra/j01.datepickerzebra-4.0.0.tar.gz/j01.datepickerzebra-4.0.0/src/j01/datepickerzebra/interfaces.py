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
$Id: interfaces.py 5001 2020-03-26 14:34:16Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

from z3c.form.interfaces import ITextWidget


class IZebraDatePickerWidget(ITextWidget):
    """Zebra DatePicker date widget supporting date and datetime fields."""


class IZebraDateTimePickerWidget(ITextWidget):
    """Zebra DatePicker date and time widget used for datetime fields."""
