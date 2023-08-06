[![version](https://badge.fury.io/py/requests-extra.svg)](https://badge.fury.io/py/requests-extra)
![release date](https://img.shields.io/github/release-date/egnyte/requests-extra)
![linter](https://github.com/requests-extra/requests-extra/workflows/Linter%20(Black)/badge.svg)
![tests](https://github.com/requests-extra/requests-extra/workflows/Tests%20(tox%20%26%20pytest)/badge.svg)

# requests-extra

Drop-in replacement for the [Requests](https://github.com/psf/requests) library
that wraps it to provide these ✨**extra**✨ features:

* For resiliency: 🤘
  * Retry by default (3 times in total) with backoff / respecting `Retry-After`,
  * Timeout by default (10 seconds),
  * Exception on 4xx and 5xx responses by default (automatic `raise_for_status()`),

* For performance: ⏩
  * Automatic HTTP keep-alive without explicitly using session,
  * Support for Brotli enabled by default,

## When to use it?

This library is highly opinionated and uses a rather simplistic approach so it may or may not fit your project.
For us it did help in the following use cases:

* improving many small scripts - f.e. used for monitoring,
* modernization of a big but simple and well-tested projects - f.e. old tests,

## How to use?

1. Replace `requests` with `requests-extra` in your dependencies file
2. Replace `requests.` with `requests_extra.` in your code.

That's it!

Example:
```python
# instead of 'from requests import get'
from requests_extra import get

get('https://httpbin.org/headers')
```

For more examples please see the [tests](https://github.com/requests-extra/requests-extra/tests/).

## How to change the defaults?

See [defaults.py](https://github.com/requests-extra/requests-extra/requests_extra/defaults.py).

To change some of them for all of your code do this:
```python
import requests_extra.defaults

requests_extra.defaults.timeout = 1
```

You can also overwrite them for a single request in the usual way:
```python
from requests_extra import get

get('https://httpbin.org', timeout=5)
```

## TODO

More features:

* Single line logging of requests and/or responses, with default secrets redaction,
* HTTP/2 support (by switching to [encode/httpx](https://github.com/encode/httpx) as a backend),
* ~~Rate limiting support, including respecting the appropriate HTTP headers~~ - urllib3 supports it
  since [v. 1.19 released on 2016-11-03](https://github.com/urllib3/urllib3/blob/master/CHANGES.rst#119-2016-11-03)... 😅
* Support for RFC-2782 style DNS SRV entries (for Consul) -
  see [pstiasny/requests-srv](https://github.com/pstiasny/requests-srv),
* Service-to-service authentication on GCP -
  see [adrianchifor/requests-gcp](https://github.com/adrianchifor/requests-gcp),
* Built-in support for caching responses? -
  maybe with [reclosedev/requests-cache](https://github.com/reclosedev/requests-cache)
  or [bionikspoon/cache_requests](https://github.com/bionikspoon/cache_requests)

## Contributing

*ALL* kinds of issues & PRs are very welcome! There are no formal rules of contributing yet, please use common sense. ;)

## Credits

Firstly big thanks to all the authors of the wrapped library, Requests!

Additionally thank you to the authors of reused code:

* The code for timeouts and `raise_for_status()` is copied from
the [better-requests/better-requests](https://github.com/better-requests/better-requests) library.
* The code for LFU cache is copied from the [luxinger/lfu_cache](https://github.com/luxigner/lfu_cache).
* Some concepts from
the [CarlosAMolina/requests_custom](https://github.com/CarlosAMolina/requests_custom) library are used too.

## License

Like the wrapped Requests, and the libraries we reused, this library uses the Apache 2.0 license.
