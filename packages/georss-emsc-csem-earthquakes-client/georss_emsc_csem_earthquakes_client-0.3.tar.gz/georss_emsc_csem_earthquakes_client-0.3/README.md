# python-georss-emsc-csem-earthquakes-client

This library provides convenient access to the [EMSC CSEM](https://www.emsc-csem.org/).

## Installation
`pip install georss_emsc_csem_earthquakes_client`

## Usage
See below for an example of how this library can be used. After instantiating 
the feed class and supplying the required parameters, you can call `update` to 
retrieve the feed data. The return value will be a tuple of a status code and 
the actual data in the form of a list of specific feed entries.

**Status Codes**
* _UPDATE_OK_: Update went fine and data was retrieved. The library may still return empty data, for example because no entries fulfilled the filter criteria.
* _UPDATE_OK_NO_DATA_: Update went fine but no data was retrieved, for example because the server indicated that there was not update since the last request.
* _UPDATE_ERROR_: Something went wrong during the update

**Supported Filters**

| Filter            |                            | Description |
|-------------------|----------------------------|-------------|
| Radius            | `filter_radius`            | Radius in kilometers around the home coordinates in which events from the feed are included. |
| Minimum Magnitude | `filter_minimum_magnitude` | Minimum magnitude as float value. Only events with a magnitude equal or above this value are included. |
| Time span | `filter_timespan` | Maximum age of reported event. |

**Example**
```python
from datetime import timedelta
from georss_emsc_csem_earthquakes_client import EMSCEarthquakesFeed
# Home Coordinates: Latitude: 46.1, Longitude: 14.1
# Filter radius: 500 km
# Filter minimum magnitude: 2.0
# Filter time span: 3 days
feed = EMSCEarthquakesFeed((46.1, 14.1), 
                            filter_radius=500,
                            filter_minimum_magnitude=2.0,
                            filter_timespan=timedelta(days=3))
status, entries = feed.update()
```

## Feed Manager

The Feed Manager helps managing feed updates over time, by notifying the 
consumer of the feed about new feed entries, updates and removed entries 
compared to the last feed update.

* If the current feed update is the first one, then all feed entries will be 
  reported as new. The feed manager will keep track of all feed entries' 
  external IDs that it has successfully processed.
* If the current feed update is not the first one, then the feed manager will 
  produce three sets:
  * Feed entries that were not in the previous feed update but are in the 
    current feed update will be reported as new.
  * Feed entries that were in the previous feed update and are still in the 
    current feed update will be reported as to be updated.
  * Feed entries that were in the previous feed update but are not in the 
    current feed update will be reported to be removed.
* If the current update fails, then all feed entries processed in the previous
  feed update will be reported to be removed.

After a successful update from the feed, the feed manager will provide two
different dates:

* `last_update` will be the timestamp of the last successful update from the
  feed. This date may be useful if the consumer of this library wants to
  treat intermittent errors from feed updates differently.
* `last_timestamp` will be the latest timestamp extracted from the feed data. 
  This requires that the underlying feed data actually contains a suitable 
  date. This date may be useful if the consumer of this library wants to 
  process feed entries differently if they haven't actually been updated.
