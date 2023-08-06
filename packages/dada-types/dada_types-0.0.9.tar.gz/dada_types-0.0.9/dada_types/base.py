import re
import time
import logging
from collections import Counter, defaultdict

from sqlalchemy import TypeDecorator, cast, func
from sqlalchemy.dialects.postgresql import ARRAY

from dada_utils import etc
import dada_serde
import dada_text

from dada_types import hum

# ///////////////////////////////////////////////////////////////
# Core Class For inheritance
# (almost everything important should be serializable to json for queue serialization reasons!)
# //////////////////////////////////////////////////////////////

BASE_LOGGER = logging.getLogger()


class SerializableObject(object):
    """
    TODO: pretty formatting of json
    """

    __abstract__ = True

    _counters = Counter()
    _timers = defaultdict(dict)
    _state = defaultdict()

    @property
    def object_name(self):
        """"""
        return dada_text.camel_to_snake(self.__class__.__name__)

    @property
    def object_title(self):
        """"""
        return dada_text.camel_to_title(self.__class__.__name__)

    @property
    def object_description(self):
        """"""
        return dada_text.rm_whitespace(self.__doc__)

    def to_dict(self):
        """"""
        raise NotImplementedError("A Serializable Object must have a to_dict method")

    def to_json(self):
        """"""
        return dada_serde.obj_to_json(self.to_dict())

    def to_jsongz(self):
        """"""
        return dada_serde.str_to_gz(self.to_json().encode("utf-8"))

    def to_yaml(self):
        """"""
        return dada_serde.obj_to_yaml(self.to_dict())

    # //////////////////
    # Internal Utilities
    # //////////////////

    # counter
    def internal_incr_counter(self, key, by=1):
        """
        Increment the internal counter
        """
        self._counters[key] += by

    # counter
    def internal_decr_counter(self, key, by):
        """
        Increment the internal counter
        """
        self._counters[key] -= by

    @property
    def internal_counters(self):
        """
        Internal counters
        """
        return self._counters

    # Runtime calculation
    def internal_set_timer_start(self, key):
        """"""
        self._timers[key].update({"start": time.time()})

    # Runtime calculation
    def internal_set_timer_end(self, key):
        """"""
        # set end time
        self._timers[key].update({"end": time.time()})
        # set diff
        self._timers[key].update(
            {"diff": self._timers[key]["end"] - self._timers[key]["start"]}
        )
        # set human
        self._timers[key].update(
            {"human": hum.display_seconds(self._timers[key]["diff"])}
        )

    @property
    def internal_timers(self):
        """"""
        return self._timers
