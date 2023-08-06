# -*- coding: utf-8 -*-
"""
:copyright: (c) 2020 by Greg Dubicki (c) 2019 by better-requests (c) 2012 by Kenneth Reitz.
:license: Apache2, see LICENSE for more details.
"""
import logging

from requests import Session as UpstreamSession
from requests.adapters import HTTPAdapter
from requests.compat import Callable
from urllib3 import Retry

import requests_extra.defaults
from requests_extra.internal.utils import default_headers_with_brotli


def _raise_for_status(res, *args, **kwargs):
    res.raise_for_status()


class Session(UpstreamSession):
    def __init__(self):
        """A Requests session.

        + retries
        + auto raise for status
        """

        super(Session, self).__init__()

        logging.debug("Setting up retries for a new session...")
        retry_strategy = Retry(
            total=requests_extra.defaults.retries_total,
            backoff_factor=requests_extra.defaults.retries_backoff_factor,
            status_forcelist=requests_extra.defaults.retries_status_forcelist,
            allowed_methods=requests_extra.defaults.retries_allowed_methods,
        )
        self.mount("http://", HTTPAdapter(max_retries=retry_strategy))
        self.mount("https://", HTTPAdapter(max_retries=retry_strategy))

        self.headers = default_headers_with_brotli()

    def prepare_request(self, request):
        """A Requests prepared request.

        + auto raise for status
        """

        p = super(Session, self).prepare_request(request)

        # add raise_for_status as a hook
        if requests_extra.defaults.auto_raise_for_status:
            # TODO: consider checking if raise_for_status has been manually added already

            logging.debug("Enabling up raise_for_status() for a request...")
            if p.hooks is None:
                p.hooks = {}

            hooks = [_raise_for_status]

            old_hooks = p.hooks.get("response")
            if old_hooks is None:
                pass
            elif hasattr(old_hooks, "__iter__"):
                hooks.extend(old_hooks)
            elif isinstance(old_hooks, Callable):
                hooks.append(old_hooks)

            p.hooks["response"] = hooks

        return p

    def send(self, request, *args, **kwargs):
        """Send a given PreparedRequest

        + timeout
        :rtype: requests.Response
        """

        # Set default timeout, None -> default, 0 -> no timeout
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = requests_extra.defaults.timeout
        elif timeout == 0:
            kwargs["timeout"] = None

        # noinspection PyArgumentList
        return super(Session, self).send(request, *args, **kwargs)
