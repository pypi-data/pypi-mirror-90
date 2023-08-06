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

    >>> from pyams_layer.interfaces import IPyAMSLayer

    >>> from pyams_form.interfaces.button import IButtonAction
    >>> from pyams_form.interfaces.widget import IFieldWidget

    >>> from pyams_skin.interfaces.form import IActionButton, ICloseButton, IResetButton, ISubmitButton
    >>> from pyams_skin.interfaces.widget import IActionWidget, ICloseWidget, IResetWidget, ISubmitWidget

    >>> from pyams_skin.widget.button import SubmitFieldWidget, SubmitButtonAction
    >>> call_decorator(config, adapter_config, SubmitFieldWidget,
    ...                required=(ISubmitButton, IPyAMSLayer), provides=IFieldWidget)
    >>> call_decorator(config, adapter_config, SubmitButtonAction,
    ...                required=(IPyAMSLayer, ISubmitButton), provides=IButtonAction)

    >>> from pyams_skin.widget.button import ActionFieldWidget, ActionButtonAction
    >>> call_decorator(config, adapter_config, ActionFieldWidget,
    ...                required=(IActionButton, IPyAMSLayer), provides=IFieldWidget)
    >>> call_decorator(config, adapter_config, ActionButtonAction,
    ...                required=(IPyAMSLayer, IActionButton), provides=IButtonAction)

    >>> from pyams_skin.widget.button import ResetFieldWidget, ResetButtonAction
    >>> call_decorator(config, adapter_config, ResetFieldWidget,
    ...                required=(IResetButton, IPyAMSLayer), provides=IFieldWidget)
    >>> call_decorator(config, adapter_config, ResetButtonAction,
    ...                required=(IPyAMSLayer, IResetButton), provides=IButtonAction)

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
    >>> alsoProvides(request, IPyAMSLayer)

    >>> form = TestForm(None, request)
    >>> form.update()

    >>> 'submit' in form.actions
    True
    >>> form.actions['submit']
    <SubmitButtonAction 'form.buttons.submit' 'Submit'>
    >>> print(form.actions['submit'].render())
    <button
                type="submit"
                id="form-buttons-submit"
                name="form.buttons.submit"
                class="btn btn-primary submit-widget submitbutton-field "
                value="Submit"
                data-loading-test="Submit...">Submit</button>


    >>> 'action' in form.actions
    True
    >>> form.actions['action']
    <ActionButtonAction 'form.buttons.action' 'Action'>
    >>> print(form.actions['action'].render())
    <button
                type="button"
                id="form-buttons-action"
                name="form.buttons.action"
                class="btn btn-secondary submit-widget actionbutton-field "
                value="Action"
                data-loading-test="Action...">Action</button>

    >>> 'reset' in form.actions
    True
    >>> form.actions['reset']
    <ResetButtonAction 'form.buttons.reset' 'Reset'>
    >>> print(form.actions['reset'].render())
    <button
                type="reset"
                id="form-buttons-reset"
                name="form.buttons.reset"
                class="btn btn-light submit-widget resetbutton-field"
                value="Reset">Reset</button>

    >>> 'close' in form.actions
    True
    >>> form.actions['close']
    <CloseButtonAction 'form.buttons.close' 'Close'>
    >>> print(form.actions['close'].render())
    <button
                type="button"
                id="form-buttons-close"
                name="form.buttons.close"
                class="btn btn-light submit-widget closebutton-field"
                value="Close"
                data-dismiss="modal">Close</button>


Custom form fields
------------------

    >>> from zope.schema import Tuple, TextLine
    >>> from pyams_utils.schema import HTTPMethodField, HTMLField

    >>> class IMyContent(Interface):
    ...     list_field = Tuple(title="List field",
    ...                        value_type=TextLine())
    ...     http_method = HTTPMethodField(title="HTTP method")
    ...     html_field = HTMLField(title="HTML field")

    >>> from zope.interface import implementer
    >>> from zope.schema.fieldproperty import FieldProperty

    >>> @implementer(IMyContent)
    ... class MyContent:
    ...     list_field = FieldProperty(IMyContent['list_field'])
    ...     http_method = FieldProperty(IMyContent['http_method'])
    ...     html_field = FieldProperty(IMyContent['html_field'])

    >>> content = MyContent()
    >>> content.list_field = ('value 1', 'value2')
    >>> content.http_method = ('POST', '/api/auth/jwt/token')
    >>> content.html_field = '<p>This is a paragraph</p>'

    >>> from zope.interface import alsoProvides
    >>> from pyams_layer.interfaces import IPyAMSLayer

    >>> request = TestRequest(context=content)
    >>> alsoProvides(request, IPyAMSLayer)

    >>> from pyams_skin.widget.list import OrderedListFieldWidget
    >>> list_widget = OrderedListFieldWidget(IMyContent['list_field'], request)
    >>> list_widget.extract()
    <NO_VALUE>

    >>> request = TestRequest(context=content, params={
    ...     'list_field': 'value2;value1'
    ... })
    >>> alsoProvides(request, IPyAMSLayer)
    >>> list_widget = OrderedListFieldWidget(IMyContent['list_field'], request)
    >>> list_widget.extract()
    ('value2', 'value1')

    >>> from pyams_form.interfaces.form import IContextAware
    >>> from pyams_skin.widget.http import HTTPMethodFieldWidget, HTTPMethodDataConverter

    >>> http_widget = HTTPMethodFieldWidget(IMyContent['http_method'], request)
    >>> http_widget.context = content
    >>> alsoProvides(http_widget, IContextAware)
    >>> http_widget.update()
    >>> http_widget.value
    ('POST', '/api/auth/jwt/token')
    >>> http_widget.display_value
    ('POST', '/api/auth/jwt/token')

    >>> http_widget.extract()
    <NO_VALUE>

    >>> request = TestRequest(context=content, params={
    ...     'http_method-empty-marker': '1',
    ...     'http_method-verb': 'GET',
    ...     'http_method-url': '/api/auth/jwt/another'
    ... })
    >>> alsoProvides(request, IPyAMSLayer)

    >>> http_widget = HTTPMethodFieldWidget(IMyContent['http_method'], request)
    >>> http_widget.context = content
    >>> alsoProvides(http_widget, IContextAware)
    >>> http_widget.extract()
    ('GET', '/api/auth/jwt/another')
    >>> http_widget.http_methods
    ('GET', 'POST', 'PUT', 'PATCH', 'HEAD', 'OPTIONS', 'DELETE')

    >>> from pyams_skin.widget.html import HTMLFieldWidget
    >>> request = TestRequest(context=content)
    >>> alsoProvides(request, IPyAMSLayer)

    >>> html_widget = HTMLFieldWidget(IMyContent['html_field'], request)
    >>> html_widget.context = content
    >>> alsoProvides(html_widget, IContextAware)
    >>> html_widget.update()
    >>> html_widget.value
    '<p>This is a paragraph</p>'
    >>> html_widget.editor_data is None
    True
    >>> pprint.pprint(html_widget.render())
    ('<textarea id="html_field"\n'
     '\t\t  name="html_field"\n'
     '\t\t  class="form-control tinymce textarea-widget required '
     'htmlfield-field">&lt;p&gt;This is a paragraph&lt;/p&gt;</textarea>')

    >>> html_widget.editor_configuration = {'ams-editor-style': 'modern'}
    >>> pprint.pprint(html_widget.render())
    ('<textarea id="html_field"\n'
     '\t\t  name="html_field"\n'
     '\t\t  class="form-control tinymce textarea-widget required htmlfield-field"\n'
     '\t\t  data-ams-options=\'{"ams-editor-style": "modern"}\'>&lt;p&gt;This is a '
     'paragraph&lt;/p&gt;</textarea>')


Tests cleanup:

    >>> tearDown()
