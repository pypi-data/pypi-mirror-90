###############################################################################
#
# Copyright (c) 2014 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""Interfaces

$Id: interfaces.py 5036 2020-06-16 11:23:18Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import zope.schema
import zope.interface
import zope.i18nmessageid

import z3c.form.interfaces

import j01.dialog.interfaces
import j01.jsonrpc.interfaces


###############################################################################
#
# form

class IForm(zope.interface.Interface):
    """Simple form"""

    refreshWidgets = zope.schema.Bool(
        title=u'Refresh widgets',
        description=(u'A flag, when set, causes form widgets to be updated '
                     u'again after action execution.'),
        default=False,
        required=True)

    refreshActions = zope.schema.Bool(
        title=u'Refresh actions',
        description=(u'A flag, when set, causes form actions to be updated '
                     u'again after action execution.'),
        default=False,
        required=True)

    def setUpWidgetValidation(name):
        """Support for single widget ssetup used by j01.validate"""


class IDisplayForm(IForm, z3c.form.interfaces.IDisplayForm):
    """Display Form"""


class IAddForm(IForm, z3c.form.interfaces.IAddForm):
    """Add form."""


class IEditForm(IForm, z3c.form.interfaces.IEditForm):
    """Edit form."""


###############################################################################
#
# jsonrpc form

class IJSONRPCForm(IForm, j01.jsonrpc.interfaces.IJSONRPCForm):
    """JSON-RPC base form mixin class."""


class IJSONRPCAddForm(IJSONRPCForm, j01.jsonrpc.interfaces.IJSONRPCAddForm):
    """JSON-RPC based add form."""


class IJSONRPCEditForm(IJSONRPCForm, j01.jsonrpc.interfaces.IJSONRPCEditForm):
    """JSON-RPC based edit form."""


###############################################################################
#
# dialog form

class IDialogForm(IForm, j01.dialog.interfaces.IDialogPage):
    """Dialog form."""


class IDialogAddForm(IDialogForm, j01.dialog.interfaces.IDialogAddForm):
    """Dialog add form."""


class IDialogEditForm(IDialogForm, j01.dialog.interfaces.IDialogEditForm):
    """Dialog edit form."""


class IDialogDeleteForm(IDialogForm, j01.dialog.interfaces.IDialogDeleteForm):
    """Dialog delete form."""


class IDialogConfirmForm(IDialogForm, j01.dialog.interfaces.IDialogConfirmForm):
    """Dialog confirm form."""


###############################################################################
#
# widgets

class IWidget(z3c.form.interfaces.IWidget):
    """Enhanced widget supporting addons and description text"""

    description = zope.schema.TextLine(
        title=u'Description',
        description=u'Description',
        default=None,
        required=False)

    addOnBefore = zope.schema.TextLine(
        title=u'Addon before widget',
        description=u'Addon before widget',
        default=None,
        required=False)

    addOnAfter = zope.schema.TextLine(
        title=u'Addon after widget',
        description=u'Addon after widget',
        default=None,
        required=False)

    addOnWrapper = zope.schema.TextLine(
        title=u'Addon widget wrapper',
        description=u'Addon widget wrapper',
        default=None,
        required=False)

    # layout element rendering conditions
    showLabel = zope.schema.Bool(
        title=u'Show widget label',
        description=u'Show widget label',
        default=True,
        required=False)

    showDescription = zope.schema.Bool(
        title=u'Show widget description',
        description=u'Show widget description',
        default=True,
        required=False)

    showRequired = zope.schema.Bool(
        title=u'Show widget required',
        description=u'Show widget required',
        default=True,
        required=False)

    showError = zope.schema.Bool(
        title=u'Show widget error',
        description=u'Show widget error',
        default=True,
        required=False)


# html5 text
class ITextWidget(IWidget):
    """Text widget with placeholder and hint support"""

    pattern = zope.schema.ASCIILine(
        title=u'Validation pattern',
        description=u'Validation pattern',
        default=None,
        required=False)

    placeholder = zope.schema.TextLine(
        title=u'Placeholder',
        description=u'Placeholder',
        default=None,
        required=False)


class IEMailWidget(ITextWidget):
    """EMail input type widget"""


class IDateWidget(ITextWidget):
    """Date input type widget"""


class IDatetimeWidget(ITextWidget):
    """Datetime input type widget"""


class IDatetimeLocalWidget(ITextWidget):
    """Datetime local input type widget"""


class ITimeWidget(ITextWidget):
    """Time input type widget"""


class IWeekWidget(ITextWidget):
    """Week input type widget"""


class IMonthWidget(ITextWidget):
    """Month input type widget"""


class IColorWidget(ITextWidget):
    """Color input type widget"""


class ISearchWidget(ITextWidget):
    """Search input type widget"""


class IURLWidget(ITextWidget):
    """Search input type widget"""


class INumberWidget(ITextWidget):
    """Number input type widget"""


class ITelWidget(ITextWidget):
    """Tel input type widget"""


# checkbox
class ICheckBoxWidget(IWidget, z3c.form.interfaces.ICheckBoxWidget):
    """CheckBoxWidget using a div wrapper for option tags"""


class ICheckBoxInlineWidget(ICheckBoxWidget):
    """CheckBoxWidget using a span wrapper for option tags"""


class ISingleCheckBoxWidget(ICheckBoxWidget,
    z3c.form.interfaces.ISingleCheckBoxWidget):
    """Single checkbox using a div wrapper for option tags"""


class ISingleCheckBoxInlineWidget(ISingleCheckBoxWidget):
    """SingleCheckBoxWidget using a span wrapper for option tags"""


class ICheckBoxPickerWidget(ICheckBoxWidget):
    """Checkbox picker using a div wrapper for option tags"""


class ICheckBoxInlinePickerWidget(ICheckBoxWidget):
    """Checkbox picker using a span wrapper for option tags"""


class ISingleCheckBoxPickerWidget(ISingleCheckBoxWidget):
    """Single checkbox using a div wrapper for option tags"""


class ISingleCheckBoxInlinePickerWidget(ISingleCheckBoxPickerWidget):
    """SingleCheckBoxWidget using a span wrapper for option tags"""


# file
class IFileWidget(IWidget, z3c.form.interfaces.IFileWidget):
    """File widget."""


# multi
class IMultiWidget(IWidget, z3c.form.interfaces.IMultiWidget):
    """None Term based sequence widget base.

    The multi widget is used for ITuple, IList or IDict if no other widget is defined.

    Some IList or ITuple are using another specialized widget if they can
    choose from a collection. e.g. a IList of IChoice. The base class of such
    widget is the ISequenceWidget.

    This widget can handle none collection based sequences and offers add or
    remove values to or from the sequence. Each sequence value get rendered by
    it's own relevant widget. e.g. IList of ITextLine or ITuple of IInt
    """


# password
class IPasswordWidget(ITextWidget, z3c.form.interfaces.IPasswordWidget):
    """Password widget with placeholder and hint support"""


class IPasswordConfirmationWidget(ITextWidget,
    z3c.form.interfaces.IPasswordWidget):
    """Password including confirmation field widget."""


# radio
class IRadioWidget(IWidget, z3c.form.interfaces.IRadioWidget):
    """Radio widget."""

    showNoValueItem = zope.schema.Bool(
        title=u'Show None as value in selection',
        description=u'Show None as value in selection',
        default=False,
        required=True)

class IRadioInlineWidget(IRadioWidget):
    """Radio inline widget."""

class IRadioPickerWidget(IRadioWidget):
    """Radio picker widget."""

class IRadioInlinePickerWidget(IRadioWidget):
    """Radio inline picker widget."""


# select
class ISelectWidget(IWidget, z3c.form.interfaces.ISelectWidget):
    """Select widget with ITerms option."""


class IMultiSelectWidget(ISelectWidget):
    """Multi select widget"""


class ISelectDropDownWidget(ISelectWidget):
    """MultiSelectDropDownWidget"""


class IMultiSelectDropDownWidget(ISelectDropDownWidget, IMultiSelectWidget):
    """MultiSelectDropDownWidget"""


class IGroupSelectWidget(ISelectWidget):
    """Select widget with optgroup support"""


class IDDSlickSelectWidget(ISelectWidget):
    """DDSlick select widget"""


# text lines
class ITextLinesWidget(IWidget, z3c.form.interfaces.ITextLinesWidget):
    """Text lines widget."""


# textarea
class ITextAreaWidget(IWidget, z3c.form.interfaces.ITextAreaWidget):
    """Text widget."""


# dictionary
class IDictKeyValueWidget(IWidget, z3c.form.interfaces.ITextAreaWidget):
    """Dict with key:value values as textarea widget."""


# proxy dictionary (<proto>:<host:port>)
class IProxyWidget(IDictKeyValueWidget):
    """Dict with <key>:<host:port> values as textarea widget.

    The key:value get split on first ':' as separator. Any following ':' will
    get joined as value.
    """


###############################################################################
#
# only availabe if j01.datepicker is available

try:
    import j01.datepicker.interfaces
    class IDatePickerWidget(IWidget,
        j01.datepicker.interfaces.IDatePickerWidget):
        """DatePicker date widget."""
except ImportError:
    pass


###############################################################################
#
# only availabe if j01.datetimepicker is available

try:
    import j01.datetimepicker.interfaces
    class IDateTimePickerWidget(IWidget,
        j01.datetimepicker.interfaces.IDateTimePickerWidget):
        """DatePicker date widget."""
except ImportError:
    pass


###############################################################################
#
# only availabe if j01.datepickerzebra is available

try:
    import j01.datepickerzebra.interfaces
    class IZebraDatePickerWidget(IWidget,
        j01.datepickerzebra.interfaces.IZebraDatePickerWidget):
        """DatePicker date widget."""
except ImportError:
    pass

try:
    import j01.datepickerzebra.interfaces
    class IZebraDateTimePickerWidget(IWidget,
        j01.datepickerzebra.interfaces.IZebraDateTimePickerWidget):
        """DatePicker date widget."""
except ImportError:
    pass


###############################################################################
#
# only availabe if j01.rater is available

try:
    import j01.rater.interfaces

    class IRatingWidget(IWidget,
        j01.rater.interfaces.IRatingWidget):
        """IRatingWidget widget"""

    class IFiveStarRatingWidget(IRatingWidget,
        j01.rater.interfaces.IFiveStarRatingWidget):
        """IFiveStarRatingWidget widget"""

    class IFiveHalfStarRatingWidget(IRatingWidget,
        j01.rater.interfaces.IFiveHalfStarRatingWidget):
        """IFiveHalfStarRatingWidget widget"""

    class IFiveHalfStarFullRatingWidget(IRatingWidget,
        j01.rater.interfaces.IFiveHalfStarFullRatingWidget):
        """IFiveHalfStarFullRatingWidget widget"""

except ImportError:
    pass


###############################################################################
#
# only availabe if j01.select2 is available

try:
    import j01.select2.interfaces
    # select
    class ISelect2Widget(IWidget, j01.select2.interfaces.ISelect2Widget):
        """Select widget for IList of IChoice fields

        All values must be a part of the choice vocabulary/source. No extra
        input is allowed. The widget will render the result as select input
        like design.
        """

    # single select
    class ISingleSelect2Widget(IWidget,
        j01.select2.interfaces.ISingleSelect2Widget):
        """Select widget for IChoice fields

        The value must be a part of the choice vocabulary/source. No extra
        input is allowed. The widget will render the result with tokens.
        """


    # tagging
    class ITagListSelect2Widget(IWidget,
        j01.select2.interfaces.ITagListSelect2Widget):
        """Select2 widget for IList of ITextLine"""


    # single tag
    class ISingleTagSelect2Widget(IWidget,
        j01.select2.interfaces.ISingleTagSelect2Widget):
        """Select2 widget for ITextLine"""


    # livelist
    class ILiveListSelect2Widget(IWidget,
        j01.select2.interfaces.ILiveListSelect2Widget):
        """Select2 widget for IList of IChoice offering live autosuggest"""


    class ILiveTagSelect2Widget(IWidget,
        j01.select2.interfaces.ILiveTagSelect2Widget):
        """Select2 widget for IChoice offering live autosuggest"""
except ImportError:
    pass


###############################################################################
#
# only availabe if j01.selectordered is available

try:
    import j01.selectordered.interfaces
    # select ordered
    class IOrderedSelectWidget(IWidget,
        j01.selectordered.interfaces.IOrderedSelectWidget):
        """Select ordered widget"""
except ImportError:
    pass


###############################################################################
#
# only availabe if m01.gmap is available

try:
    import m01.gmap.interfaces
    class IGMapWidget(IWidget, m01.gmap.interfaces.IGMapWidget):
        """GMap widget"""

    class IGeoPointGMapWidget(IWidget, m01.gmap.interfaces.IGeoPointGMapWidget):
        """GeoPoint GMap widget"""
except ImportError:
    pass
