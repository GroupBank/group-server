from behave import *
from behave.runner import Context


#
# Givens/Conditions/Initial State
#

@given("the invitee is registered")
def step_impl(context: Context):
    pass


@given("the invited user is not registered")
def step_impl(context: Context):
    pass


@given("the invitee is not registered")
def step_impl(context: Context):
    pass


@given("the invited user is already registered")
def step_impl(context: Context):
    pass


@given("the invite is valid")
def step_impl(context: Context):
    pass


@given("the invite does not follow the JSON format")
def step_impl(context: Context):
    pass


@given('the payload is missing "{attribute}" attribute')
def step_impl(context: Context, attribute: str):
    pass


@given("the invite's ID does not match the ID of the author")
def step_impl(context):
    pass


#
# Whens/Actions
#

@when('invitation is requested without the "{parameter}" parameter')
def step_impl(context: Context, parameter: str):
    pass


@when("invitation is requested")
def step_impl(context: Context):
    pass


#
# Thens/Assertions
#

@then("the server responds with a success code")
def step_impl(context: Context):
    pass


@then("the server responds with a Not Found code")
def step_impl(context: Context):
    pass


@then("the server responds with a Bad Request code")
def step_impl(context: Context):
    pass
