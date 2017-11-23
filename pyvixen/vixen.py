"""
pyvixen.vixen
~~~~~~~~~~~~~~~~~~~~
Provides api for Vixen 3.2+
Copyright (c) 2017 John Mihalic <https://github.com/mezz64>
Licensed under the MIT license.

"""

import logging
import asyncio
import aiohttp
import async_timeout

from pyvixen.constants import (
    DEFAULT_TIMEOUT, DEFAULT_HEADERS, ELEMENT_ROOT, GET_ELEMENTS, ELEMENT_ON,
    ELEMENT_OFF, SEARCH_ELEMENTS, ELEMENT_CLEAR, PLAY_ROOT, GET_SEQUENCES,
    SEQUENCE_PLAY, SEQUENCE_STOP, SEQUENCE_PAUSE, SEQUENCE_STATUS)

_LOGGER = logging.getLogger(__name__)

# pylint: disable=invalid-name,no-member
try:
    ensure_future = asyncio.ensure_future
except AttributeError:
    # Python 3.4.3 and earlier has this as async
    ensure_future = asyncio.async


class VixenLights(object):
    """Vixen Lights API object."""
    def __init__(self, ip, port=8888, loop=None):
        """Initialize vixen lights class."""
        self._base_url = 'http://{}:{}'.format(ip, port)

        self._elements = None
        self._selements = None
        self._sequences = None
        self._status = None

        if loop is None:
            _LOGGER.info("Must supply asyncio loop.  Quitting")
            return None
        else:
            self._event_loop = loop

        asyncio.set_event_loop(self._event_loop)

        self._api_session = aiohttp.ClientSession(
            headers=DEFAULT_HEADERS, loop=self._event_loop)

    @property
    def elements(self):
        """Return list of elements."""
        return self._elements

    @property
    def sequences(self):
        """Return list of sequences."""
        return self._sequences

    @property
    def status(self):
        """Return list of sequences."""
        return self._status

    @asyncio.coroutine
    def update_lists(self):
        """Fetch element and sequence lists."""
        yield from self.fetch_elements()
        yield from self.fetch_sequences()

    @asyncio.coroutine
    def stop(self):
        """Stop api session."""
        _LOGGER.debug('Closing vixen lights api session.')
        yield from self._api_session.close()

    @asyncio.coroutine
    def fetch_elements(self):
        """Fetch list of elements."""
        url = self._base_url + ELEMENT_ROOT + GET_ELEMENTS

        elist = yield from self.api_get(url)
        if elist is None:
            _LOGGER.error('Unable to fetch vixen element list.')
        else:
            self._elements = elist
            _LOGGER.debug('Elements: %s', self._elements)

    @asyncio.coroutine
    def search_elements(self, query):
        """search list of elements."""
        url = self._base_url + ELEMENT_ROOT + SEARCH_ELEMENTS
        params = {'q': query}

        selist = yield from self.api_get(url, params)
        if selist is None:
            _LOGGER.error('Unable to search vixen element list.')
        else:
            self._selements = selist
            _LOGGER.debug('Elements: %s', self._selements)

    @asyncio.coroutine
    def turnon_element(self, guid, duration, intensity, color):
        """Turn on element with the specified parameters."""
        url = self._base_url + ELEMENT_ROOT + ELEMENT_ON

        payload = {'id': guid,
                   'duration': duration,
                   'intensity': intensity,
                   'color': color}  # Color Format: '#0000FF'

        on = yield from self.api_post(url, None, payload)
        if on is None:
            _LOGGER.error('Unable to turn on element id (%s).', guid)
        else:
            _LOGGER.debug(on['Message'])

    @asyncio.coroutine
    def turnoff_element(self, guid):
        """Turn off element."""
        url = self._base_url + ELEMENT_ROOT + ELEMENT_OFF

        payload = {'id': guid}

        off = yield from self.api_post(url, None, payload)
        if off is None:
            _LOGGER.error('Unable to turn off element id(%s).', guid)
        else:
            _LOGGER.debug(off['Message'])

    @asyncio.coroutine
    def clearall_elements(self):
        """Clear all active effects initiated from api."""
        url = self._base_url + ELEMENT_ROOT + ELEMENT_CLEAR

        off = yield from self.api_post(url)
        if off is None:
            _LOGGER.error('Unable to clear all elements.')
        else:
            _LOGGER.debug(off['Message'])

    @asyncio.coroutine
    def fetch_sequences(self):
        """Fetch list of sequences from api."""
        url = self._base_url + PLAY_ROOT + GET_SEQUENCES

        slist = yield from self.api_get(url)
        if slist is None:
            _LOGGER.error('Unable to fetch vixen sequence list.')
        else:
            self._sequences = slist
            _LOGGER.debug('Sequences: %s', self._sequences)

    @asyncio.coroutine
    def play_sequence(self, name, filename):
        """Play sequence from sequence list."""
        url = self._base_url + PLAY_ROOT + SEQUENCE_PLAY

        payload = {'Name': name,
                   'FileName': filename}

        play = yield from self.api_post(url, None, payload)
        if play is None:
            _LOGGER.error('Unable to play sequence(%s).', name)
        else:
            _LOGGER.debug(play['Message'])

    @asyncio.coroutine
    def stop_sequence(self, name, filename):
        """Stop sequence from sequence list."""
        url = self._base_url + PLAY_ROOT + SEQUENCE_STOP

        payload = {'Name': name,
                   'FileName': filename}

        stop = yield from self.api_post(url, None, payload)
        if stop is None:
            _LOGGER.error('Unable to stop sequence(%s).', name)
        else:
            _LOGGER.debug(stop['Message'])

    @asyncio.coroutine
    def pause_sequence(self, name, filename):
        """Pause sequence from sequence list."""
        url = self._base_url + PLAY_ROOT + SEQUENCE_PAUSE

        payload = {'Name': name,
                   'FileName': filename}

        pause = yield from self.api_post(url, None, payload)
        if pause is None:
            _LOGGER.error('Unable to pause sequence(%s).', name)
        else:
            _LOGGER.debug(pause['Message'])

    @asyncio.coroutine
    def sequence_status(self):
        """Fetch status of active sequences."""
        url = self._base_url + PLAY_ROOT + SEQUENCE_STATUS

        status = yield from self.api_get(url)
        if status is None:
            _LOGGER.error('Unable to fetch vixen sequence status.')
        else:
            self._status = status
            _LOGGER.debug('Status: %s', self._status)

    @asyncio.coroutine
    def api_post(self, url, params=None, data=None):
        """Make api post request."""
        post = None
        try:
            with async_timeout.timeout(DEFAULT_TIMEOUT, loop=self._event_loop):
                post = yield from self._api_session.post(
                    url, params=params, data=data)
            if post.status != 200:
                _LOGGER.error('Error posting Vixen data: %s', post.status)
                return None

            if 'application/json' in post.headers['content-type']:
                post_result = yield from post.json()
            else:
                _LOGGER.debug('Response was not JSON, returning text.')
                post_result = yield from post.text()

            return post_result

        except (aiohttp.ClientError, asyncio.TimeoutError,
                ConnectionRefusedError) as err:
            _LOGGER.error('Error posting Vixen data. %s', err)
            return None

    @asyncio.coroutine
    def api_get(self, url, params=None):
        """Make api get request."""
        try:
            with async_timeout.timeout(DEFAULT_TIMEOUT, loop=self._event_loop):
                request = yield from self._api_session.get(
                    url, params=params)
            # _LOGGER.debug('Get URL: %s', request.url)
            if request.status != 200:
                _LOGGER.error('Error fetching Vixen data: %s', request.status)
                return None

            if 'application/json' in request.headers['content-type']:
                request_json = yield from request.json()
            else:
                _LOGGER.debug('Response was not JSON, returning text.')
                request_json = yield from request.text()

            return request_json

        except (aiohttp.ClientError, asyncio.TimeoutError,
                ConnectionRefusedError) as err:
            _LOGGER.error('Error fetching Vixen data. %s', err)
            return None
