import logging
from urllib.parse import urlparse

from requests_extra import sessions
from requests_extra.internal.cache import LFUCache

logger = logging.getLogger(__name__)

lfu = LFUCache(10)


def get_cached_session(url):
    logger.debug("Getting a session for url: '%s'", url)

    cache_key = get_cache_key(url)
    logger.debug("Cache key is: '%s'", cache_key)

    maybe_session = lfu.get(cache_key)
    if maybe_session != -1:
        logger.debug("Got session from cache!")

        # we need to clear the cookie jar of this session before reusing it
        # to simulate non-sessioned requests

        maybe_session.cookies.clear()

        return maybe_session
    else:
        logger.debug("No such session in cache - creating new one...")
        new_session = get_new_session()
        lfu.set(cache_key, new_session)
        return new_session


def get_cache_key(url):
    # we want to prevent reconnecting so sessions are kept in cache per scheme, host and port,
    # f.e. "http://httpbin.org:80" or "https://www.google.com:443"

    parsed_url = urlparse(url, scheme="http")

    # netloc 'httpbin.org:80' and 'httpbin.org' are de facto the same for 'http' scheme
    # simlarly for port 443 with 'https'
    # (but NOT in the mixed cases: 'http://httpbin.org:443' != 'http://httpbin.org')
    # TODO: consider normalizing the netloc to take this into account

    protocol_host_and_port = parsed_url.scheme + "://" + parsed_url.netloc

    return protocol_host_and_port


def get_new_session():
    session = sessions.Session()
    return session
