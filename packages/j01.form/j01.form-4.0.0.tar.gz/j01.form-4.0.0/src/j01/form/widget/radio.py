###############################################################################
#
# Copyright (c) 2014 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""Radio widget
$Id: radio.py 4806 2018-04-09 13:17:16Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import sys

import zope.i18n
import zope.i18nmessageid
import zope.component
import zope.interface
import zope.schema.interfaces
from zope.pagetemplate.interfaces import IPageTemplate

import z3c.form.interfaces
import z3c.form.widget
import z3c.form.util
import z3c.form.browser.widget

from j01.form import interfaces
from j01.form.layer import IFormLayer
from j01.form.widget.widget import WidgetMixin

_ = zope.i18nmessageid.MessageFactory('p01')

PY3 = sys.version_info[0] >= 3

try:
    unicode
except NameError:
    # Py3: Define unicode.
    unicode = str

def toUnicode(obj):
    if isinstance(obj, bytes):
        return obj.decode('utf-8', 'ignore')
    if PY3:
        return str(obj)
    else:
        return unicode(obj)


class RadioWidget(WidgetMixin, z3c.form.browser.widget.HTMLInputWidget,
    z3c.form.widget.SequenceWidget):
    """RadioWidget using a div wrapper for option tags"""

    zope.interface.implementsOnly(interfaces.IRadioWidget)

    klass = u'radio-control' # no form-control
    css = u'radio'
    noValueMessage = _('No value')
    showNoValueItem = False

    # Internal attributes
    _adapterValueAttributes = \
        z3c.form.widget.SequenceWidget._adapterValueAttributes + \
        ('noValueMessage',)

    def isChecked(self, term):
        return term.token in self.value

    def renderForValue(self, value):
        term = self.terms.getTermByToken(value)
        checked = self.isChecked(term)
        id = '%s-%i' % (self.id, list(self.terms).index(term))
        item = {'id': id, 'name': self.name, 'value': term.token,
                'checked': checked}
        template = zope.component.getMultiAdapter(
            (self.context, self.request, self.form, self.field, self),
            IPageTemplate, name=self.mode + '_single')
        return template(self, item)

    @property
    def items(self):
        items = []
        if not self.required and self.showNoValueItem:
            label = zope.i18n.translate(self.noValueMessage,
                context=self.request, default=self.noValueMessage)
            if not self.value:
                checked = True
            elif self.noValueToken in self.value:
                checked = True
            else:
                checked = False
            items.append({
                'id': self.id + '-novalue',
                'name': self.name,
                'value': self.noValueToken,
                'label': label,
                'checked': checked,
                })
        if self.terms is not None:
            for count, term in enumerate(self.terms):
                checked = self.isChecked(term)
                id = '%s-%i' % (self.id, count)
                if zope.schema.interfaces.ITitledTokenizedTerm.providedBy(term):
                    label = zope.i18n.translate(term.title, context=self.request,
                        default=term.title)
                else:
                    label = toUnicode(term.value)
                items.append({
                    'id': id,
                    'name': self.name,
                    'value': term.token,
                    'label': label,
                    'checked': checked,
                    })
        return items


class RadioInlineWidget(RadioWidget):
    """RadioWidget using a span wrapper for option tags"""

    zope.interface.implementsOnly(interfaces.IRadioInlineWidget)


JAVASCRIPT = """
<script type="text/javascript">
$(document).ready(function(){
    $('input[name^="%s"]').picker();
});
</script>
"""


class RadioPickerWidget(RadioWidget):
    """RadioPickerWidget using a div wrapper for option tags"""

    zope.interface.implementsOnly(interfaces.IRadioPickerWidget)

    klass = u'radio-picker-control' # no form-control
    css = u'radio-picker'

    @property
    def javascript(self):
        return JAVASCRIPT % self.name.replace('.', '\\\.')


class RadioInlinePickerWidget(RadioWidget):
    """RadioInlinePickerWidget using a span wrapper for option tags"""

    zope.interface.implementsOnly(interfaces.IRadioInlinePickerWidget)

    klass = u'radio-picker-control'
    css = u'radio-inline-picker'

    @property
    def javascript(self):
        return JAVASCRIPT % self.name.replace('.', '\\\.')


# get
@zope.component.adapter(zope.schema.interfaces.IField, IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def getRadioWidget(field, request):
    """IFieldWidget factory for RadioWidget."""
    return z3c.form.widget.FieldWidget(field, RadioWidget(request))


@zope.component.adapter(zope.schema.interfaces.IField, IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def getRadioInlineWidget(field, request):
    """IFieldWidget factory for RadioWidget."""
    return z3c.form.widget.FieldWidget(field, RadioInlineWidget(request))


@zope.component.adapter(zope.schema.interfaces.IField, IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def getRadioPickerWidget(field, request):
    """IFieldWidget factory for RadioWidget."""
    return z3c.form.widget.FieldWidget(field, RadioPickerWidget(request))


@zope.component.adapter(zope.schema.interfaces.IField, IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def getRadioInlinePickerWidget(field, request):
    """IFieldWidget factory for RadioWidget."""
    return z3c.form.widget.FieldWidget(field, RadioInlinePickerWidget(request))