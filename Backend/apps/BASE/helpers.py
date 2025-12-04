# import datetime, json, random, secrets, string, time, typing, inflect, calendar
import datetime, json, random, secrets, string, time, typing, calendar
from dateutil import tz
from django.conf import settings

# from requests import request


def create_log(data: typing.Any, category: str):
    if settings.DEBUG:
        print("Log: ", data, category)  # noqa


def get_display_name_for_slug(slug: str):
    try:
        return slug.replace("_", " ").title()
    except:  # noqa
        return slug


def convert_utc_to_local_timezone(
    input_datetime: datetime.date | datetime.datetime,
    inbound_request,  # noqa
):
    """
    Given a UTC datetime or date object, this will convert it to the
    user's local timezone based on the request.
    """

    from_zone = tz.gettz(settings.TIME_ZONE)

    # TODO: from `inbound_request`
    to_zone = tz.gettz("Asia/Kolkata")

    input_datetime = input_datetime.replace(tzinfo=from_zone)

    return input_datetime.astimezone(to_zone)
