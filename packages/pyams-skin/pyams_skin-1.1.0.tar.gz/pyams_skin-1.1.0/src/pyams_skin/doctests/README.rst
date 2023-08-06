==================
PyAMS_skin package
==================

Introduction
------------

This package is composed of a set of utility functions, usable into any Pyramid application.

    >>> import pprint

    >>> from pyramid.testing import setUp, tearDown
    >>> config = setUp(hook_zca=True)

    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_form import includeme as include_form
    >>> include_form(config)
    >>> from pyams_skin import includeme as include_skin
    >>> include_skin(config)

    >>> from pyams_utils.testing import call_decorator
    >>> from pyams_utils.adapter import adapter_config


Custom buttons
--------------

    >>> from pyams_layer.interfaces import IFormLayer

    >>> from pyams_form.interfaces.button import IButtonAction
    >>> from pyams_form.interfaces.widget import IFieldWidget

    >>> from pyams_skin.interfaces.form import IActionButton, ICloseButton, IResetButton, ISubmitButton
    >>> from pyams_skin.interfaces.widget import IActionWidget, ICloseWidget, IResetWidget, ISubmitWidget

    >>> from pyams_skin.widget.button import SubmitFieldWidget, SubmitButtonAction
    >>> call_decorator(config, adapter_config, SubmitFieldWidget,
    ...                required=(ISubmitButton, IFormLayer), provides=IFieldWidget)
    >>> call_decorator(config, adapter_config, SubmitButtonAction,
    ...                required=(IFormLayer, ISubmitButton), provides=IButtonAction)

    >>> from pyams_skin.widget.button import ActionFieldWidget, ActionButtonAction
    >>> call_decorator(config, adapter_config, ActionFieldWidget,
    ...                required=(IActionButton, IFormLayer), provides=IFieldWidget)
    >>> call_decorator(config, adapter_config, ActionButtonAction,
    ...                required=(IFormLayer, IActionButton), provides=IButtonAction)

    >>> from pyams_skin.widget.button import ResetFieldWidget, ResetButtonAction
    >>> call_decorator(config, adapter_config, ResetFieldWidget,
    ...                required=(IResetButton, IFormLayer), provides=IFieldWidget)
    >>> call_decorator(config, adapter_config, ResetButtonAction,
    ...                required=(IFormLayer, IResetButton), provides=IButtonAction)

    >>> from pyams_form.testing import TestRequest

    >>> from zope.interface import alsoProvides, Interface
    >>> from pyams_skin.schema.button import SubmitButton, ActionButton, ResetButton, CloseButton

    >>> class ITestButtons(Interface):
    ...     submit = SubmitButton(name='submit', title="Submit")
    ...     action = ActionButton(name='action', title="Action")
    ...     reset = ResetButton(name='reset', title="Reset")
    ...     close = CloseButton(name='close', title="Close")

    >>> from pyams_form.button import Buttons
    >>> from pyams_form.field import Fields
    >>> from pyams_form.form import EditForm

    >>> class TestForm(EditForm):
    ...     buttons = Buttons(ITestButtons)
    ...     fields = Fields(Interface)

    >>> request = TestRequest()
    >>> alsoProvides(request, IFormLayer)
    >>> IFormLayer.providedBy(request)
    True

    >>> form = TestForm(None, request)
    >>> form.update()

    >>> 'submit' in form.actions
    True
    >>> form.actions['submit']
    <SubmitButtonAction 'form.buttons.submit' 'Submit'>
    >>> form.actions['submit'].render()
    '<input type="submit"\n       id="form-buttons-submit"\n       name="form.buttons.submit"\n       class="submit-widget submitbutton-field"\n       value="Submit" />'

    >>> 'action' in form.actions
    True
    >>> form.actions['action']
    <ActionButtonAction 'form.buttons.action' 'Action'>
    >>> form.actions['action'].render()
    '<input type="submit"\n       id="form-buttons-action"\n       name="form.buttons.action"\n       class="submit-widget actionbutton-field"\n       value="Action" />'

    >>> 'reset' in form.actions
    True
    >>> form.actions['reset']
    <ResetButtonAction 'form.buttons.reset' 'Reset'>
    >>> form.actions['reset'].render()
    '<input type="submit"\n       id="form-buttons-reset"\n       name="form.buttons.reset"\n       class="submit-widget resetbutton-field"\n       value="Reset" />'

    >>> 'close' in form.actions
    True
    >>> form.actions['close']
    <CloseButtonAction 'form.buttons.close' 'Close'>
    >>> form.actions['close'].render()
    '<input type="submit"\n       id="form-buttons-close"\n       name="form.buttons.close"\n       class="submit-widget closebutton-field"\n       value="Close" />'


    >>> tearDown()
