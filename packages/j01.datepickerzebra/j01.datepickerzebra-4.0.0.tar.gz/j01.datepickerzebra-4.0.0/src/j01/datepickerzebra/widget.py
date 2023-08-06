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
$Id: widget.py 5034 2020-06-16 11:22:36Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import datetime

import zope.interface
import zope.component
import zope.i18n
import zope.i18nmessageid

import z3c.form.interfaces
import z3c.form.widget
import z3c.form.browser.widget

from j01.datepickerzebra import UTC
from j01.datepickerzebra import interfaces


_ = zope.i18nmessageid.MessageFactory('p01')


# i18n
DAYS = [
    _('Sunday'),
    _('Monday'),
    _('Tuesday'),
    _('Wednesday'),
    _('Thursday'),
    _('Friday'),
    _('Saturday'),
    ]

MONTHS = [
    _('January'),
    _('February'),
    _('March'),
    _('April'),
    _('May'),
    _('June'),
    _('July'),
    _('August'),
    _('September'),
    _('October'),
    _('November'),
    _('December'),
    ]


# javascript
J01_ZEBRA_DATEPICKER_JAVASCRIPT = """<script>
$(document).ready(function() {
    $("%(expression)s").Zebra_DatePicker({%(settings)s});
});
</script>
"""


def j01DatePickerJavaScript(j01DatePickerExpression, data):
    """DatePicker JavaScript generator

    SEE: https://github.com/stefangabos/Zebra_Datepicker#properties

    $(document).ready(function() {
        // assuming the controls you want to attach the plugin to
        // have the "datepicker" class set
        $('input.datepicker').Zebra_DatePicker();
    });

    """
    # settings
    lines = []
    append = lines.append
    for key, value in data.items():
        # complex values
        if key == 'direction':
            # single direction marker
            if value is True:
                append("\n    direction: true")
            elif value is False:
                append("\n    direction: false")
            elif isinstance(value, int):
                append("\n    direction: %s" % value)
            # start end date range
            elif isinstance(value, list):
                start, end = value
                if start == False:
                    sd = 'false'
                elif isisntance(start, int):
                    sd = int(start)
                else:
                    # formatted string
                    sd = start
                if end == False:
                    ed = 'false'
                elif isisntance(end, int):
                    ed = int(end)
                else:
                    # formatted string
                    ed = end
                append("\n    direction: [%s, %s]" % (sd, ed))
        elif key == 'pair':
            # pair with other widget, that's a JQuery lookup call
            append("\n    pair: %s" % value)
        elif key in ['days', 'months']:
            # prevent unicode marker e.g. u'Januar'
            l = ["\"%s\"" % v for v in value]
            append("\n    %s: [%s]" % (key, ','.join(l)))
        elif key in ['header_captions']:
            l = ["        %s: \"%s\"" % (k,v) for k,v in value.items()]
            if l:
                append("\n    %s: {\n%s\n    }" % (key, ',\n'.join(l)))
        elif key in ['custom_classes',
                     'disabled_dates',
                     'enabled_dates',
                     'enabled_seconds',
                     'enabled_minutes',
                     'enabled_hours',
                     'weekend_days']:
            if value is False:
                append("\n    %s: false" % key)
            elif value is True:
                append("\n    %s: true" % key)
            elif isinstance(value, list):
                append("\n    %s: %s" % (key, value))
        elif key in ['navigation']:
            l = ["\"%s\"" % v for v in value]
            if l:
                append("\n    %s: [%s]" % (key, ','.join(l)))
        # generic values
        elif value is True:
            append("\n    %s: true" % key)
        elif value is False:
            append("\n    %s: false" % key)
        elif value is None:
            append("\n    %s: null" % key)
        elif isinstance(value, int):
            append("\n    %s: %s" % (key, value))
        elif isinstance(value, (str, unicode)):
            append("\n    %s: \"%s\"" % (key, value))
        else:
            append("\n    %s: %s" % (key, value))
    settings = ','.join(lines)
    return J01_ZEBRA_DATEPICKER_JAVASCRIPT % ({
        'expression': j01DatePickerExpression,
        'settings': settings,
        })


# date widget
class ZebraDatePickerWidgetBase(z3c.form.browser.widget.HTMLTextInputWidget,
    z3c.form.widget.Widget):
    """Date picker widget widget"""

    klass = u'j01ZebraDatePickerWidget'
    css = u'j01-datepicker-zebra'

    _label = None
    value = u''

    formatterType = 'dateTime'
    formatterLength = 'medium'
    formatter = None


    # deault date or datetime formatter pattern
    defaultDateFormatPattern = u'MM.dd.yyyy'

    # default date picker formatter pattern
    defaultDatePickerFormatPattern = u'm.d.Y'

    # i18n
    dateLocales = {
        # NOTE: we exclude seconds display and selection
        'dd.MM.yyyy': _(u'dd.mm.yyyy'),
        'dd.MM.yyyy HH': _(u'dd.mm.yyyy HH'),
        'dd.MM.yyyy HH:mm': _(u'dd.mm.yyyy HH:MM'),
        'dd.MM.yyyy HH:mm:ss': _(u'dd.mm.yyyy HH:MM:SS'),
        'dd/MM/yyyy': _(u'dd/mm/yyyy'),
        'dd/MM/yyyy HH': _(u'dd/mm/yyyy HH'),
        'dd/MM/yyyy HH:mm': _(u'dd/mm/yyyy HH:MM'),
        'dd/MM/yyyy HH:mm:ss': _(u'dd/mm/yyyy HH:MM:SS'),
        'dd-MM-yyyy': _(u'dd-mm-yyyy'),
        'dd-MM-yyyy HH': _(u'dd-mm-yyyy HH'),
        'dd-MM-yyyy HH:mm': _(u'dd-mm-yyyy HH:MM'),
        'dd-MM-yyyy HH:mm:ss': _(u'dd-mm-yyyy HH:MM:SS'),
        'MM.dd.yyyy': _(u'mm.dd.yyyy'),
        'MM.dd.yyyyHH': _(u'mm.dd.yyyy HH'),
        'MM.dd.yyyyHH:mm': _(u'mm.dd.yyyy HH:MM'),
        'MM.dd.yyyyHH:mm:ss': _(u'mm.dd.yyyy HH:MM:SS'),
        'MM/dd/yyyy': _(u'mm/dd/yyyy'),
        'MM/dd/yyyy HH': _(u'mm/dd/yyyy HH'),
        'MM/dd/yyyy HH:mm': _(u'mm/dd/yyyy HH:MM'),
        'MM/dd/yyyy HH:mm:ss': _(u'mm/dd/yyyy HH:MM:SS'),
        'MM-dd-yyyy': _(u'mm-dd-yyyy'),
        'MM-dd-yyyy HH': _(u'mm-dd-yyyy HH'),
        'MM-dd-yyyy HH:mm': _(u'mm-dd-yyyy HH:MM'),
        'MM-dd-yyyy HH:mm:ss': _(u'mm-dd-yyyy HH:MM:SS'),
    }

    appendLabelDatePattern = True

    # timeAppendix is only used in datetime convert for correct the appended
    # time. see: DatePickerForDatetimeConverter for more info
    # We can use startDate = '00:00:00' and endDate = '23:59:59'
    # this will make sure we have almost a full day stored between startDate
    # and endDate but at the same time we can show the same date value
    timeAppendix = '00:00:00'

    skipPastDates = False
    skipFutureDates = False
    skipDates = False

    # skip selection and control formatter pattern
    skipHours = False
    skipMinutes = False
    skipSeconds = True

    # https://github.com/stefangabos/Zebra_Datepicker#properties
    # zebra datepicker settings
    alwaysVisibleExpression = False

    # 'body' or jQuery expression will get wrapped with $('')
    container = None
    currentDate = False

    # custom_classes. {'myclass':  ['* * * 0,6']}
    customClasses = False
    daysAbbr = False

    # default_position: possible values are "above" and "below"
    defaultPosition = 'above'

    disableTimePicker = False

    # disabled_dates: ['* * * 0,6']
    disabledDates = False
    enabledDates = False
    enabledHours = False
    enabledMinutes = False
    enabledSeconds = False
    fastNavigation = True
    firstDayOfWeek = 1

    # header_captions: {
    #    days: 'F, Y',
    #    months: 'Y',
    #    years: 'Y1 - Y2'
    #    }
    headerCaptions = None

    iconMargin = False
    iconPosition = 'right'
    inside = True
    monthsAbbr = False

    # navigation: ['&#9664;', '&#9654;', '&#9650;', '&#9660;']
    navigation = None

    # offset: [5, -5]
    offset = None
    openIconOnly = False
    openOnFocus = False
    pair = False
    readonlyElement = False
    rtl = False
    selectOtherMonths = False
    showClearDate = 0
    showIcon = True
    showOtherMonths = True

    showWeekNumber = False
    startDate = False
    strict = False
    view = 'days'

    # weekend_days: [0, 6]
    weekendDays = None
    zeroPad = False
    onChange = None
    onClear = None
    onOpen = None
    onClose = None
    onSelect = None

    def translate(self, msg):
        return zope.i18n.translate(msg, context=self.request)

    @property
    def pattern(self):
        return self.formatter.getPattern()

    def doFormat(self, d):
        return self.formatter.format(d, self.dateFormatPattern)

    def doParse(self, s, pattern=None):
        if pattern is None:
            pattern = self.dateFormatPattern
        return self.formatter.parse(s, pattern=pattern)

    @property
    def showSelectToday(self):
        return self.translate(_(u"Today"))

    @property
    def langClearDate(self):
        return self.translate(_(u"Clear date"))

    def getLabel(self):
        if self.appendLabelDatePattern:
            # translate and append date pattern to label
            label = self.translate(self._label)
            i18n = self.dateLocales.get(self.dateFormatPattern)
            pattern = self.translate(i18n)
            return '%s (%s)' % (label, pattern)
        else:
            # return plain label
            return self._label

    @apply
    def label():
        def fget(self):
            return self.getLabel()
        def fset(self, value):
            # set plain field title as value
            self._label = value
        return property(fget, fset)

    @property
    def tzinfo(self):
        return UTC

    @property
    def dateFormatPattern(self):
        """Returns the python format for parse the date string input value"""
        if self.pattern in self.dateLocales:
            pattern = self.pattern
            if self.skipHours:
                # remove hours
                pattern = pattern.replace(':HH', '')
            if self.skipMinutes:
                # remove mminutes
                pattern = pattern.replace(':mm', '')
            if self.skipSeconds:
                # remove seconds
                pattern = pattern.replace(':ss', '')
        else:
            pattern = self.defaultDateFormatPattern
        return pattern

    @property
    def datePickerFormatPattern(self):
        """Return the zebra datepicker format based on the given pattern"""
        if self.pattern in self.dateLocales:
            pattern = self.pattern.replace('yyyy', 'Y')
            pattern = pattern.replace('MM', 'm')
            pattern = pattern.replace('dd', 'd')
            if self.skipHours:
                pattern = pattern.replace(' HH', '')
            else:
                pattern = pattern.replace('HH', 'H')
            if self.skipMinutes:
                # remove mminutes
                pattern = pattern.replace(':mm', '')
            else:
                pattern = pattern.replace('mm', 'i')
            if self.skipSeconds:
                # remove seconds
                pattern = pattern.replace(':ss', '')
            else:
                pattern = pattern.replace(':ss', '')
        else:
            pattern = self.defaultDatePickerFormatPattern
        return pattern

    # dates
    @property
    def days(self):
        return [self.translate(d) for d in DAYS]

    @property
    def months(self):
        return [self.translate(d) for d in MONTHS]

    @property
    def today(self):
        return zope.i18n.translate(_(u"today"), context=self.request)

    @property
    def clear(self):
        return zope.i18n.translate(_(u"remove"), context=self.request)

    @property
    def language(self):
        # the language is not really important, it's just used as a namespace
        # for our translated date strings
        lang = self.request.locale.id.language
        return lang and lang or 'en'

    @property
    def sDate(self):
        """Start date"""
        if self.skipPastDates:
            today = datetime.date.today()
            return self.doFormat(today)
        else:
            return False

    @property
    def eDate(self):
        """End date"""
        if self.skipFutureDates:
            today = datetime.date.today()
            return self.doFormat(today)
        else:
            return False

    @property
    def direction(self):
        if self.skipDates:
            return 0
        else:
            return [self.sDate, self.eDate]

    @property
    def containerExpression(self):
        if self.container is not None:
            return '$("%s")' % self.container

    @property
    def j01DatePickerExpression(self):
        return '#%s' % self.id.replace('.', '\\\.')

    @property
    def javascript(self):
        data = {
            'format': self.datePickerFormatPattern,
            'show_select_today': self.showSelectToday,
            'lang_clear_date': self.langClearDate,
		    }
        if self.containerExpression is not None:
            data['container'] = self.containerExpression
        if self.alwaysVisibleExpression is not False:
            data['always_visible'] = self.alwaysVisibleExpression
        if self.currentDate is not False:
            data['current_date'] = self.currentDate
        if self.customClasses is not False:
            data['custom_classes'] = self.customClasses
        if self.days:
            data['days'] = self.days
        if self.daysAbbr is not False:
            data['days_abbr'] = self.daysAbbr
        if self.defaultPosition != 'above':
            data['default_position'] = self.defaultPosition
        if self.direction != 0:
            data['direction'] = self.direction
        if self.disableTimePicker is not False:
            data['disable_time_picker'] = self.disableTimePicker
        if self.disabledDates is not False:
            data['disabled_dates'] = self.disabledDates
        if self.enabledDates is not False:
            data['enabled_dates'] = self.enabledDates
        if self.enabledHours is not False:
            data['enabled_hours'] = self.enabledHours
        if self.enabledMinutes is not False:
            data['enabled_minutes'] = self.enabledMinutes
        if self.enabledSeconds is not False:
            data['enabled_seconds'] = self.enabledSeconds
        if self.fastNavigation is not True:
            data['fast_navigation'] = self.fastNavigation
        if self.firstDayOfWeek != 1:
            data['first_day_of_week'] = self.firstDayOfWeek
        if self.headerCaptions:
            data['header_captions'] = self.headerCaptions
        if self.iconMargin is not False:
            data['icon_margin'] = self.iconMargin
        if self.iconPosition != 'right':
            data['icon_position'] = self.iconPosition
        if self.inside is not True:
            data['inside'] = self.inside
        if self.months:
            data['months'] = self.months
        if self.monthsAbbr is not False:
            data['months_abbr'] = self.monthsAbbr
        if self.navigation is not None:
            data['navigation'] = self.navigation
        if self.offset is not None:
            data['offset'] = self.offset
        if self.openIconOnly is not False:
            data['open_icon_only'] = self.openIconOnly
        if self.openOnFocus is not False:
            data['open_on_focus'] = self.openOnFocus
        if self.pair is not False:
            data['pair'] = self.pair
        if self.readonlyElement is not True:
            data['readonly_element'] = self.readonlyElement
        if self.rtl is not False:
            data['rtl'] = self.rtl
        if self.selectOtherMonths is not False:
            data['select_other_months'] = self.selectOtherMonths
        if self.showClearDate != 0:
            data['show_clear_date'] = self.showClearDate
        if self.showIcon is not True:
            data['show_icon'] = self.showIcon
        if self.showOtherMonths is not True:
            data['show_other_months'] = self.showOtherMonths
        if self.showWeekNumber is not False:
            data['show_week_number'] = self.showWeekNumber
        if self.startDate is not False:
            data['start_date'] = self.startDate
        if self.strict is not False:
            data['strict'] = self.strict
        if self.view != 'days':
            data['view'] = self.view
        if self.weekendDays is not None:
            data['weekend_days'] = self.weekendDays
        if self.zeroPad is not False:
            data['zero_pad'] = self.zeroPad
        if self.onChange is not None:
            data['onChange'] = self.onChange
        if self.onClear is not None:
            data['onClear'] = self.onClear
        if self.onOpen is not None:
            data['onOpen'] = self.onOpen
        if self.onClose is not None:
            data['onClose'] = self.onClose
        if self.onSelect is not None:
            data['onSelect'] = self.onSelect

        return j01DatePickerJavaScript(self.j01DatePickerExpression, data)

    def update(self):
        """Will setup the script attribute."""
        # setup formatter pattern given from request via converter
        self.formatter = self.request.locale.dates.getFormatter(
            self.formatterType, self.formatterLength)
        # update widget and converter which uses our own formatter pattern
        super(ZebraDatePickerWidgetBase, self).update()


################################################################################
#
# date picker widget

class ZebraDatePickerWidget(ZebraDatePickerWidgetBase):
    """Zebra DatePicker date widget supporting date and datetime fields."""

    zope.interface.implementsOnly(interfaces.IZebraDatePickerWidget)


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

class ZebraDateTimePickerWidget(ZebraDatePickerWidgetBase):
    """Zebra DatePicker date and time widget used for datetime fields."""

    zope.interface.implementsOnly(interfaces.IZebraDateTimePickerWidget)


def getZebraDateTimePickerWidget(field, request):
    """IFieldWidget factory for ItemsWidget."""
    return z3c.form.widget.FieldWidget(field, ZebraDateTimePickerWidget(request))
