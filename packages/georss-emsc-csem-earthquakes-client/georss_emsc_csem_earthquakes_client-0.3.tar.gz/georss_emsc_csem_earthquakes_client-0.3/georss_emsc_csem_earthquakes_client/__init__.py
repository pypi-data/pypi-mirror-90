"""
EMSC CSEM Earthquakes Feed.

Fetches GeoRSS feed from EMSC CSEM Earthquakes.
"""
import logging
import datetime

from dateutil.parser import parse
from tzlocal import get_localzone

from typing import Optional

from georss_client import GeoRssFeed, FeedEntry
from georss_client.consts import CUSTOM_ATTRIBUTE
from georss_client.exceptions import GeoRssException
from georss_client.feed_manager import FeedManagerBase

_LOGGER = logging.getLogger(__name__)

"""
Feeds are available here: https://www.emsc-csem.org/service/rss/
Use 'Last 50 earthquakes in euro mediteranean region' feed as default
"""
DEFAULT_URL = 'https://www.emsc-csem.org/service/rss/rss.php?typ=emsc'

XML_TAG_MAGNITUDE = 'https://www.emsc-csem.org:magnitude'
XML_TAG_TIME = 'https://www.emsc-csem.org:time'
XML_TAG_DEPTH = 'https://www.emsc-csem.org:depth'
XML_TAG_LINK = 'link'


class EMSCEarthquakesFeedManager(FeedManagerBase):
    """Feed Manager for EMSC CSEM Earthquakes feed."""

    def __init__(self, generate_callback, update_callback, remove_callback,
                 coordinates, filter_radius=None,
                 filter_minimum_magnitude=None,
                 filter_timespan: datetime.timedelta=None):
        """Initialize the EMSC CSEM Earthquakes Feed Manager."""
        feed = EMSCEarthquakesFeed(
            coordinates,
            filter_radius=filter_radius,
            filter_minimum_magnitude=filter_minimum_magnitude,
            filter_timespan=filter_timespan)
        super().__init__(feed, generate_callback, update_callback,
                         remove_callback)


class EMSCEarthquakesFeed(GeoRssFeed):
    """EMSC CSEM Earthquakes feed."""

    def __init__(self, home_coordinates, url=DEFAULT_URL, filter_radius=None,
                 filter_minimum_magnitude=None, filter_timespan: datetime.timedelta=None):
        """Initialise this service."""
        super().__init__(home_coordinates, url,
                         filter_radius=filter_radius)
        self._filter_minimum_magnitude = filter_minimum_magnitude
        self._filter_timespan = filter_timespan

    def __repr__(self):
        """Return string representation of this feed."""
        return '<{}(home={}, url={}, filter_radius={}, filter_minimum_magnitude={})>'.format(
            self.__class__.__name__, self._home_coordinates, self._url,
            self._filter_radius, self._filter_minimum_magnitude)

    def _new_entry(self, home_coordinates, rss_entry, global_data):
        """Generate a new entry."""
        return EMSCEarthquakesFeedEntry(home_coordinates, rss_entry)

    def _filter_entries(self, entries):
        """Filter the provided entries."""
        entries = super()._filter_entries(entries)
        if self._filter_minimum_magnitude:
            entries = list(filter(lambda entry:
                                  entry.magnitude and entry.magnitude >=
                                  self._filter_minimum_magnitude, entries))
        if self._filter_timespan:
            from_time = datetime.datetime.now(get_localzone()) - self._filter_timespan
            entries = list(filter(lambda entry:
                                  entry.time >= from_time, entries))
        return entries


class EMSCEarthquakesFeedEntry(FeedEntry):
    """EMSC CSEM Earthquakes feed entry."""

    def __init__(self, home_coordinates, rss_entry):
        """Initialise this service."""
        super().__init__(home_coordinates, rss_entry)

    def __repr__(self):
        """Return string representation of this feed."""
        return '<{}(id={}, title={}, link={}, geometry={}, time={}, depth={}, magnitude={})>'.format(
            self.__class__.__name__, self.external_id,
            self.title, self.link, self.geometry, self.time, self.depth, self.magnitude)

    @property
    def link(self) -> Optional[str]:
        """Return a link with detailed description of the earthquake."""
        return self._rss_entry._attribute_with_text([XML_TAG_LINK])

    @property
    def time(self) -> Optional[datetime.datetime]:
        """Return time of the earthquake in local timezone."""
        return parse(self._rss_entry._attribute_with_text([XML_TAG_TIME])).astimezone(get_localzone())
        #return self._rss_entry._attribute_with_text([XML_TAG_TIME])

    @property
    def depth(self) -> Optional[float]:
        """Return depth (in km) of the earthquake."""
        return self._rss_entry._attribute_with_text([XML_TAG_DEPTH])

    @property
    def magnitude(self) -> Optional[float]:
        """Return magnitude of the earthquake.
           Magnitude scale is being reported as prefix and needs to be removed, e.g 'ML ' prefix."""
        mag_str = self._rss_entry._attribute_with_text([XML_TAG_MAGNITUDE])
        if mag_str:
            return float(mag_str.rpartition(' ')[-1])
        return None