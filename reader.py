import logging

import psycopg
from psycopg.rows import dict_row
from miflora.miflora_poller import MiFloraPoller # type: ignore
from btlewrap.bluepy import BluepyBackend # type: ignore
from rich.logging import RichHandler

LOG_FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO",
    format=LOG_FORMAT,
    datefmt="[%X] ",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)],
)
LOGGER = logging.getLogger(__name__)

METRICS = ["temperature", "moisture", "conductivity", "light", "battery"]


# you can remove this and create a .pgpass file intead, or use 
# environment variables or whatever. 
HOST = "your.db.server.com"
PASSWORD = "secret"


with psycopg.connect(host=HOST, password=PASSWORD) as conn:
    cur = conn.cursor(row_factory=dict_row)
    cur2 = conn.cursor(row_factory=dict_row)

    cur.execute(
        """ select id, mac, name from miflora_sensor_assignments where active """
    )

    sensors_to_visit = cur.fetchall()
    for sensor in sensors_to_visit:
        LOGGER.info("Handling sensor %s", sensor)
        poller = MiFloraPoller(sensor["mac"], BluepyBackend)

        for metric in METRICS:
            LOGGER.info("\tgetting metric %s", metric)
            m_value = poller.parameter_value(metric)
            LOGGER.info("metrics: %s, %s, %s", sensor["name"], metric, m_value)

            cur2.execute(
                """ insert into miflora_readings (sensor_id, metric, metric_value, reading_date) values
                         (%s, %s, %s, now())""",
                (sensor["id"], metric, m_value),
            )
