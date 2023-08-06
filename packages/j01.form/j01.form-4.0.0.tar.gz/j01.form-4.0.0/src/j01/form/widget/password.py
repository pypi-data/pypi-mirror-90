###############################################################################
#
# Copyright (c) 2014 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""Password widget
$Id: password.py 4932 2018-10-05 15:00:06Z roger.ineichen $
"""
__docformat__ = 'restructuredtext'

# use html.escape for python3
import cgi

import zope.interface
import zope.component
import zope.i18n
import zope.i18nmessageid
import zope.schema
import zope.schema.interfaces

import z3c.form.interfaces
import z3c.form.converter
import z3c.form.validator
import z3c.form.widget

import j01.form.exceptions
from j01.form import interfaces
from j01.form.layer import IFormLayer
from j01.form.widget.text import TextWidget

_ = zope.i18nmessageid.MessageFactory('p01')


class PasswordWidget(TextWidget):
    """Input type password widget implementation."""

    zope.interface.implementsOnly(interfaces.IPasswordWidget)

    _type = 'password'
    klass = u'password-control form-control'
    css = u'password'


LABEL_PASSWORD_CONFIRMATION = """
<div class="labelPasswordConfirmation">
  <label for="%s">
    <span>%s</span>
  </label>
</div>
"""

class PasswordConfirmationWidget(TextWidget):
    """Input type password widget implementation."""
    zope.interface.implementsOnly(interfaces.IPasswordConfirmationWidget)

    _type = 'password'
    klass = u'password-confirmation-control form-control'
    css = u'password-confirmation'

    @property
    def labelPasswordConfirmation(self):
        label = zope.i18n.translate(_(u'Password confirmation'),
            context=self.request)
        for_ = '%s-confirm' % self.id
        # escaped label because we use structure vew/labelPasswordConfirmation
        return LABEL_PASSWORD_CONFIRMATION % (for_, cgi.escape(label))


class PasswordRequiredValue(object):
    """Knows if input is required or not."""

    zope.interface.implements(z3c.form.interfaces.IValue)
    zope.component.adapts(zope.interface.Interface, zope.interface.Interface,
        zope.interface.Interface, zope.schema.interfaces.IPassword,
        interfaces.IPasswordConfirmationWidget)

    def __init__(self, context, request, form, field, widget):
        self.context = context
        self.request = request
        self.form = form
        self.field = field
        self.widget = widget

    def get(self):
        """Returns the value for the required field."""
        if self.field.required == True and \
            self.widget.value != self.field.missing_value:
            # change the required flag at the field
            self.field.required = False
        return self.field.required


class PasswordConfirmationValidator(z3c.form.validator.SimpleFieldValidator):
    """Simple Field Validator"""
    zope.interface.implements(z3c.form.interfaces.IValidator)
    zope.component.adapts(
        zope.interface.Interface,
        zope.interface.Interface,
        zope.interface.Interface,
        zope.schema.interfaces.IPassword,
        interfaces.IPasswordConfirmationWidget)

    def validate(self, value):
        """See interfaces.IValidator"""
        # we get a value if the password is equal to the confirmation value or
        # if password and confirmation is empty, we get the existing value
        # stored in the field

        # don't validate emtpy value if the widget was set to required = False
        # by the PasswordRequiredValue adapter
        requestValue = self.request.get(self.widget.name, 1)
        confirmValue = self.request.get(self.widget.name + '.confirm', 2)
        if confirmValue == u'' and requestValue == u'' and \
            self.field.required == False:
            return

        # compare both field values with each others
        if requestValue != confirmValue:
            raise j01.form.exceptions.PasswordComparsionError

        # default validation if we not allready get done
        field = self.field
        if self.context is not None:
            field = field.bind(self.context)
        return field.validate(value)


# password confirmation converter
class PasswordConfirmationDataConverter(z3c.form.converter.FieldDataConverter):
    """A data converter using the field's ``fromUnicode()`` method."""
    zope.component.adapts(zope.schema.interfaces.IFromUnicode,
        interfaces.IPasswordConfirmationWidget)

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        # check for empty form input
        confirm = self.widget.request.get(self.widget.name + '.confirm', None)
        if value == u'' and confirm == u'' and self.field.required == False:
            # if there is an empty value, we return the field value if widget
            # was set to required = False by the PasswordRequiredValue adapter
            return self.field.query(self.widget.context)
        return self.field.fromUnicode(value)


# get
@zope.component.adapter(zope.schema.interfaces.IPassword, IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def getPasswordWidget(field, request):
    """IFieldWidget factory for IPasswordWidget."""
    return z3c.form.widget.FieldWidget(field, PasswordWidget(request))


@zope.component.adapter(zope.schema.interfaces.IPassword, IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def getPasswordConfirmationWidget(field, request):
    """IFieldWidget factory for PasswordConfirmationWidget."""
    return z3c.form.widget.FieldWidget(field, PasswordConfirmationWidget(request))
