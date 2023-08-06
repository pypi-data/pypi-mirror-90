##############################################################################
#
# Copyright (c) 2020 Projekt01 GmbH and Contributors.
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
$Id: datepickerzebra.py 5036 2020-06-16 11:23:18Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import zope.interface

import z3c.form.widget

import j01.datepickerzebra.widget

from j01.form import interfaces
from j01.form.widget.widget import WidgetMixin


################################################################################
#
# date picker widget

class ZebraDatePickerWidget(WidgetMixin,
    j01.datepickerzebra.widget.ZebraDatePickerWidget):
    """DatePicker widget implementation."""

    zope.interface.implementsOnly(interfaces.IZebraDatePickerWidget)

    klass = u'j01-datepicker-zebra-control form-control'
    css = u'j01-datepicker-zebra'


def getZebraDatePickerWidget(field, request):
    """IFieldWidget factory for ItemsWidget."""
    return z3c.form.widget.FieldWidget(field, ZebraDatePickerWidget(request))


def getStartZebraDatePickerWidget(field, request):
    """IFieldWidget factory for ItemsWidget."""
    # this widget uses the default timeAppendix settings '00:00:00'
    # and prevents selecting previous dates
    widget = ZebraDatePickerWidget(request)
    widget.skipPastDates = True
    return z3c.form.widget.FieldWidget(field, widget)


def getEndZebraDatePickerWidget(field, request):
    """IFieldWidget factory for ItemsWidget."""
    # this widget uses the default timeAppendix settings '23:59:59'
    # and prevents selecting previous dates
    widget = ZebraDatePickerWidget(request)
    widget.timeAppendix = '23:59:59'
    widget.skipPastDates = True
    return z3c.form.widget.FieldWidget(field, widget)


################################################################################
#
# date time picker widget

class ZebraDateTimePickerWidget(WidgetMixin,
    j01.datepickerzebra.widget.ZebraDateTimePickerWidget):
    """DateTimePicker widget implementation."""

    zope.interface.implementsOnly(interfaces.IZebraDateTimePickerWidget)

    klass = u'j01-datepicker-zebra-control form-control'
    css = u'j01-datepicker-zebra'


def getZebraDateTimePickerWidget(field, request):
    """IFieldWidget factory for ItemsWidget."""
    return z3c.form.widget.FieldWidget(field, ZebraDateTimePickerWidget(request))
