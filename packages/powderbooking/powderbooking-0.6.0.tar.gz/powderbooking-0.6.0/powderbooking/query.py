#  Copyright (c) 2021. Michael Kemna.

from enum import Enum

from sqlalchemy import text


class Query(Enum):
    """
    This Enum is used to create a framework to store the queries that are used by the
    application.
    Of course, you can also create your own Query Enum in your own module.

    source to execute raw sql with sqlalchemy:
    https://chartio.com/resources/tutorials/how-to-execute-raw-sql-in-sqlalchemy/
    """

    select_forecast_scrape_today = text(
        """
        SELECT r.id, lat, lng
        FROM resort as r
        LEFT JOIN (SELECT id, resort_id
                   FROM forecast
                   WHERE date = current_date
                   and timepoint = 0
                   ) as f on r.id = f.resort_id
        WHERE f.id is NULL
        AND r.id >= 0
    """
    )

    select_weather_scrape_3h = text(
        """
        SELECT r.id, lat, lng
        FROM resort as r
        LEFT JOIN (SELECT id, resort_id 
                   FROM weather 
                   WHERE date_request > current_timestamp - 3 * interval '1 hour'
                   ) as w on r.id = w.resort_id
        WHERE w.id is NULL
        AND r.id >= 0
    """
    )

    select_weather_resort_1d = text(
        """
        SELECT *
        FROM weather
        WHERE weather.resort_id = :resort_id 
            AND NOW() - dt < INTERVAL '1 day'
        ORDER BY dt DESC
        LIMIT 1
    """
    )

    select_forecast_resort_1d = text(
        """
        SELECT *
        FROM forecast
        WHERE resort_id = :resort_id
            AND NOW() - date_request < INTERVAL '1 day'
        ORDER BY timepoint
    """
    )

    select_forecast_week_resort_1d = text(
        """
        SELECT *
        FROM forecast_week
        WHERE resort_id = :resort_id
            AND NOW() - date_request < INTERVAL '1 day'
    """
    )
