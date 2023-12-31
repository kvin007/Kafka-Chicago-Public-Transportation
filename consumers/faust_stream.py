"""Defines trends calculations for stations"""
import logging

import faust

logger = logging.getLogger(__name__)


# Faust will ingest records from Kafka in this format
class Station(faust.Record):
    stop_id: int
    direction_id: str
    stop_name: str
    station_name: str
    station_descriptive_name: str
    station_id: int
    order: int
    red: bool
    blue: bool
    green: bool


# Faust will produce records to Kafka in this format
class TransformedStation(faust.Record):
    station_id: int
    station_name: str
    order: int
    line: str


app = faust.App(
    "stations-stream", broker="kafka://localhost:9092", store="memory://"
)
# app = faust.App(
#     "stations-stream", broker="kafka://kafka0:9092", store="memory://"
# )

topic = app.topic("connect_stations", value_type=Station)
out_topic = app.topic("org.chicago.cta.stations.table.v1", partitions=1)

table = app.Table(
    "transformed_stations",
    default=TransformedStation,
    partitions=1,
    changelog_topic=out_topic,
)


def determine_line(station):
    if station.red:
        return "red"
    elif station.blue:
        return "blue"
    elif station.green:
        return "green"
    else:
        return "unknown"


@app.agent(topic)
async def transform_stations(stations):
    async for station in stations:
        line = determine_line(station)
        table[station.station_id] = TransformedStation(
            station_id=station.station_id,
            station_name=station.station_name,
            order=station.order,
            line=line,
        )


if __name__ == "__main__":
    app.main()
