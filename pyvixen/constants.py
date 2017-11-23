"""
pyvixen.constants
~~~~~~~~~~~~~~~~~~~~
Constants list
Copyright (c) 2017 John Mihalic <https://github.com/mezz64>
Licensed under the MIT license.
"""

MAJOR_VERSION = 0
MINOR_VERSION = 0
SUB_MINOR_VERSION = 1
__version__ = '{}.{}.{}'.format(
    MAJOR_VERSION, MINOR_VERSION, SUB_MINOR_VERSION)

# Endpoint URLS
ELEMENT_ROOT = '/api/element/'
GET_ELEMENTS = 'getElements'
SEARCH_ELEMENTS = 'searchElements'
ELEMENT_ON = 'on'
ELEMENT_OFF = 'off'
ELEMENT_GROUPON = 'groupon'
ELEMENT_CLEAR = 'clearall'

PLAY_ROOT = '/api/play/'
GET_SEQUENCES = 'getSequences'
SEQUENCE_PLAY = 'playSequence'
SEQUENCE_STOP = 'stopSequence'
SEQUENCE_PAUSE = 'pauseSequence'
SEQUENCE_STATUS = 'status'

DEFAULT_TIMEOUT = 10

DEFAULT_HEADERS = {
    'content-type': "application/x-www-form-urlencoded",
    }
