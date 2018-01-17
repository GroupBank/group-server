import os

import django
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.shortcuts import resolve_url
from django.test.runner import DiscoverRunner

os.environ["DJANGO_SETTINGS_MODULE"] = "group_server.settings"
django.setup()


def before_all(context):
    context.test_runner = DiscoverRunner()
    context.test_runner.setup_test_environment()
    context.old_db_config = context.test_runner.setup_databases()


def before_scenario(context, _):
    context.test = BehaviorDrivenTestCase()
    context.test.setUpClass()
    context.test()  # this starts a transaction

    context.base_url = context.test.live_server_url

    def get_url(to=None, *args, **kwargs):
        return context.base_url + (
            resolve_url(to, *args, **kwargs) if to else '')

    context.get_url = get_url


class BehaviorDrivenTestCase(StaticLiveServerTestCase):
    """
    Test case attached to the context during behave execution

    This test case prevents the regular tests from running.
    """

    def runTest(*args, **kwargs):
        pass


def after_scenario(context, _):
    context.test.tearDownClass()
    del context.test


def after_all(context):
    context.test_runner.teardown_databases(context.old_db_config)
    context.test_runner.teardown_test_environment()
