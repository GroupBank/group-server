""" Module containing the tests for the 'decorators' module """

from unittest.mock import MagicMock

import pytest
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from hamcrest import assert_that, is_, instance_of

import common.crypto.ec_secp256k1 as crypto
from rest.decorators import post_parameters, authenticate


class TestPostParameters:
    """ Test cases for the post_parameters() decorator """

    @pytest.mark.parametrize("parameters", [
        {
            'author': '#1',
            'payload': '{"params": "value"}',
            'signature': 'asjkdasjkd',
        },
        {
            'author': '#1',
            'payload': '{"params": "value"}',
            'signature': 'asjkdasjkd',
            'other': 'value',
        },
    ])
    def test_RequestWithAllParameters_CallsTheViewWithNoErrors(self, parameters):
        view = MagicMock()
        request = MagicMock()
        request.POST = parameters

        # Inject the view into the decorator and call the wrapper
        post_parameters(view)(request)

        view.assert_called_once_with(request, '#1', '{"params": "value"}', 'asjkdasjkd')

    @pytest.mark.parametrize("parameters", [
        {
            'payload': '{"params": "value"}',
            'signature': 'asjkdasjkd',
        },
        {
            'author': '#1',
            'signature': 'asjkdasjkd',
        },
        {
            'author': '#1',
            'payload': '{"params": "value"}',
        },
        {},
    ])
    def test_RequestMissingSomeParameters_RespondsWithBadRequestError(self, parameters):
        view = MagicMock()
        request = MagicMock()
        request.POST = parameters

        # Inject the view into the decorator and call the wrapper
        response = post_parameters(view)(request)

        assert_that(response, is_(instance_of(HttpResponseBadRequest)))


class TestAuthenticate:
    """ Test cases for the authenticate() decorator """

    def test_RequestWithValidSignature_CallsTheViewWithSameArguments(self):
        view = MagicMock()
        request = MagicMock()

        key, pubkey = crypto.generate_keys()
        signature = crypto.sign(key, '{"params": "value"}')
        request.POST = {
            'author': pubkey,
            'payload': '{"params": "value"}',
            'signature': signature,
        }

        # Inject the view into the decorator and call the wrapper
        authenticate(view)(request, pubkey, '{"params": "value"}', signature)

        view.assert_called_once_with(request, pubkey, '{"params": "value"}', signature)

    def test_RequestWithInvalidKey_RespondsWithForbiddenError(self):
        view = MagicMock()
        request = MagicMock()
        request.POST = {
            'author': 'invalid key',
            'payload': '{"params": "value"}',
            'signature': 'adkasjd',
        }

        # Inject the view into the decorator and call the wrapper
        response = authenticate(view)(request, 'invalid key', '{"params": "value"}', 'adkasjd')

        assert_that(response, is_(instance_of(HttpResponseForbidden)))

    def test_RequestWithInvalidSignature_RespondsWithForbiddenError(self):
        view = MagicMock()
        request = MagicMock()

        key, pubkey = crypto.generate_keys()
        other_key, _ = crypto.generate_keys()
        signature = crypto.sign(other_key, '{"params": "value"}')
        request.POST = {
            'author': pubkey,
            'payload': '{"params": "value"}',
            'signature': signature,
        }

        # Inject the view into the decorator and call the wrapper
        response = authenticate(view)(request, pubkey, '{"params": "value"}', signature)

        assert_that(response, is_(instance_of(HttpResponseForbidden)))
