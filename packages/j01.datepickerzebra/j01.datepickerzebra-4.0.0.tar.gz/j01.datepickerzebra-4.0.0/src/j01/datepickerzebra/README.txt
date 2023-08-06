======================
ZebraDatePicker Widget
======================

This package provides two datepicker based widgets. One can be used for
IDatetime fields and the other for IDate fields.


ZebraDatePickerWidget
---------------------

As for all widgets, the ZebraDatePickerWidget must provide the new ``IWidget``
interface:

  >>> import os
  >>> import zope.schema
  >>> from zope.interface.verify import verifyClass
  >>> from z3c.form.interfaces import IWidget
  >>> from z3c.form.interfaces import INPUT_MODE
  >>> from z3c.form.converter import FieldWidgetDataConverter
  >>> import j01.datepickerzebra
  >>> from j01.datepickerzebra import interfaces
  >>> from j01.datepickerzebra.converter import ZebraDatePickerConverter
  >>> from j01.datepickerzebra.widget import ZebraDatePickerWidget

  >>> verifyClass(IWidget, ZebraDatePickerWidget)
  True

The widget can be instantiated NOT only using the request like other widgets,
we need an additional schema field because our widget uses a converter for
find the right date formatter pattern.Let's setup a schema field now:

  >>> date = zope.schema.Date(
  ...     title=u"date",
  ...     description=u"date")

  >>> from z3c.form.testing import TestRequest
  >>> request = TestRequest()

  >>> widget = ZebraDatePickerWidget(request)
  >>> widget.field = date

Before rendering the widget, one has to set the name and id of the widget:

  >>> widget.id = 'widget.id'
  >>> widget.name = 'widget.date'

We also need to register the template for the widget:

  >>> import zope.component
  >>> from zope.pagetemplate.interfaces import IPageTemplate
  >>> from z3c.form.widget import WidgetTemplateFactory

  >>> def getPath(filename):
  ...     return os.path.join(os.path.dirname(j01.datepickerzebra.__file__),
  ...     filename)

  >>> zope.component.provideAdapter(
  ...     WidgetTemplateFactory(getPath('input.pt'), 'text/html'),
  ...     (None, None, None, None, interfaces.IZebraDatePickerWidget),
  ...     IPageTemplate, name=INPUT_MODE)

And we need our ZebraDatePickerConverter date converter:

  >>> zope.component.provideAdapter(FieldWidgetDataConverter)
  >>> zope.component.provideAdapter(ZebraDatePickerConverter)

If we render the widget we get a simple input element. The given input element
id called ``j01ZebraDatePickerWidget`` will display a nice date picker if you click
on it and load the selected date into the given input element with the id
``j01ZebraDatePickerWidget``:

  >>> widget.update()
  >>> print(widget.render())
  <input type="text" id="widget.id" name="widget.date" class="j01ZebraDatePickerWidget" value="" />
  <script>
  $(document).ready(function() {
      $("#widget\\.id").Zebra_DatePicker({
      direction: [false, false],
      format: "m.d.Y",
      months: ["January","February","March","April","May","June","July","August","September","October","November","December"],
      days: ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
      lang_clear_date: "Clear date",
      show_select_today: "Today",
      readonly_element: false});
  });
  </script>
  <BLANKLINE>

A value will get rendered as simple text input:

  >>> widget.value = '24.02.1969'
  >>> print(widget.render())
  <input type="text" id="widget.id" name="widget.date" class="j01ZebraDatePickerWidget" value="24.02.1969" />
  <script>
  $(document).ready(function() {
      $("#widget\\.id").Zebra_DatePicker({
      direction: [false, false],
      format: "m.d.Y",
      months: ["January","February","March","April","May","June","July","August","September","October","November","December"],
      days: ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
      lang_clear_date: "Clear date",
      show_select_today: "Today",
      readonly_element: false});
  });
  </script>
  <BLANKLINE>

Let's now make sure that we can extract user entered data from a widget:

  >>> widget.request = TestRequest(form={'widget.date': '24.02.1969'})
  >>> widget.update()
  >>> widget.extract()
  u'24.02.1969'


If nothing is found in the request, the default is returned:

  >>> widget.request = TestRequest()
  >>> widget.update()
  >>> widget.extract()
  <NO_VALUE>


options
-------

the zebra datepicker widget provides different options. This are:

  >>> widget.alwaysVisibleExpression = True
  >>> widget.container = '#container'
  >>> widget.currentDate = True
  >>> widget.customClasses =  ['* * * 0,6']
  >>> widget.daysAbbr = True
  >>> widget.defaultPosition = 'below'
  >>> widget.disableTimePicker = True
  >>> widget.disabledDates = ['* * * 0,6']
  >>> widget.enabledDates = True
  >>> widget.enabledHours = True
  >>> widget.enabledMinutes = True
  >>> widget.enabledSeconds = True
  >>> widget.fastNavigation = False
  >>> widget.firstDayOfWeek = 1
  >>> widget.headerCaptions = {
  ...     'days': 'F, Y',
  ...     'months': 'Y',
  ...     'years': 'Y1 - Y2'
  ...     }
  >>> widget.iconMargin = True
  >>> widget.iconPosition = 'right'
  >>> widget.inside = False
  >>> widget.monthsAbbr = True
  >>> widget.navigation = ['&#9664;', '&#9654;', '&#9650;', '&#9660;']
  >>> widget.offset = [4, -4]
  >>> widget.openIconOnly = True
  >>> widget.openOnFocus = True
  >>> widget.pair = True
  >>> widget.readonlyElement = False
  >>> widget.rtl = True
  >>> widget.selectOtherMonths = True
  >>> widget.showClearDate = 1
  >>> widget.showIcon = False
  >>> widget.showOtherMonths = False
  >>> widget.showWeekNumber = True
  >>> widget.startDate = '29.02.2020'
  >>> widget.strict = True
  >>> widget.view = 'months'
  >>> widget.weekendDays = [0,1]
  >>> widget.zeroPad = True
  >>> widget.onChange = 'function onChange(view, elements) {}'
  >>> widget.onClear = 'function onClear(view, elements) {}'
  >>> widget.onOpen = 'function onOpen(view, elements) {}'
  >>> widget.onClose = 'function onClose(view, elements) {}'
  >>> widget.onSelect = 'function onSelect(view, elements) {}'
  >>> print(widget.render())
  <input type="text" id="widget.id" name="widget.date" class="j01ZebraDatePickerWidget" value="24.02.1969" />
  <script>
  $(document).ready(function() {
      $("#widget\\.id").Zebra_DatePicker({
      onOpen: "function onOpen(view, elements) {}",
      months_abbr: true,
      months: ["January","February","March","April","May","June","July","August","September","October","November","December"],
      enabled_hours: true,
      rtl: true,
      enabled_minutes: true,
      fast_navigation: false,
      open_icon_only: true,
      container: "$("#container")",
      show_clear_date: 1,
      icon_margin: true,
      strict: true,
      current_date: true,
      header_captions: {
          months: "Y",
          days: "F, Y",
          years: "Y1 - Y2"
      },
      weekend_days: [0, 1],
      enabled_seconds: true,
      onChange: "function onChange(view, elements) {}",
      days_abbr: true,
      start_date: "29.02.2020",
      disable_time_picker: true,
      direction: [false, false],
      format: "m.d.Y",
      select_other_months: true,
      onClose: "function onClose(view, elements) {}",
      zero_pad: true,
      lang_clear_date: "Clear date",
      onSelect: "function onSelect(view, elements) {}",
      open_on_focus: true,
      always_visible: true,
      offset: [4, -4],
      pair: True,
      disabled_dates: ['* * * 0,6'],
      enabled_dates: true,
      readonly_element: false,
      show_icon: false,
      inside: false,
      default_position: "below",
      days: ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
      custom_classes: ['* * * 0,6'],
      show_week_number: true,
      show_select_today: "Today",
      view: "months",
      navigation: ["&#9664;","&#9654;","&#9650;","&#9660;"],
      onClear: "function onClear(view, elements) {}",
      show_other_months: false});
  });
  </script>
  <BLANKLINE>

  >>> widget.request = TestRequest(form={'widget.date': '24.02.1969'})
  >>> widget.update()
  >>> widget.extract()
  u'24.02.1969'
