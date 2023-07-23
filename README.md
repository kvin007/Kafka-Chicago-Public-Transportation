# Public Transit Status with Apache Kafka - Solution

In this project, a streaming pipeline was built around Apache Kafka and its ecosystem to display the real-time status of train lines for the Chicago Transit Authority (CTA) on a monitoring website.

## Prerequisites

To complete this project, the following prerequisites were required:

* Docker
* Python 3.7
* Access to a computer with a minimum of 16GB+ RAM and a 4-core CPU to execute the simulation

## Description

The project involved multiple steps to build the event pipeline using Apache Kafka and related tools. The architecture of the pipeline was as follows:

![Project Architecture](images/diagram.png)

### Step 1: Creating Kafka Producers

In this step, we configured the train stations to emit events that we needed for our pipeline. Each train station had a sensor on each side that could trigger an action whenever a train arrived at the station.

Tasks Completed:
- Implemented the code in `producers/models/producer.py`.
- Defined `value` schemas for the arrival and turnstile events in `producers/models/schemas/arrival_value.json` and `producers/models/schemas/turnstile_value.json`, respectively.
- Completed the code in `producers/models/station.py` to create topics for each station in Kafka and emit `arrival` and `turnstile` events when appropriate.

### Step 2: Configuring Kafka REST Proxy Producer

In this step, we sent weather readings into Kafka from weather hardware using Kafka's REST Proxy due to hardware restrictions.

Tasks Completed:
- Defined a `value` schema for the weather event in `producers/models/schemas/weather_value.json`.
- Completed the code in `producers/models/weather.py` to create a topic for weather events and emit `weather` events to Kafka REST Proxy.

### Step 3: Configuring Kafka Connect

In this step, we extracted station information from the PostgreSQL database into Kafka using the Kafka JDBC Source Connector.

Tasks Completed:
- Completed the code and configuration in `producers/connectors.py` to use the Kafka JDBC Source Connector and connect to the database.

### Step 4: Configuring the Faust Stream Processor

In this step, we used Faust Stream Processing to transform the raw Stations table ingested from Kafka Connect.

Tasks Completed:
- Completed the code and configuration in `consumers/faust_stream.py` to ingest data from the Kafka Connect topic and transform the data.

### Step 5: Configuring the KSQL Table

In this step, we used KSQL to aggregate turnstile data for each station.

Tasks Completed:
- Completed the queries in `consumers/ksql.py` to create the necessary KSQL table.

### Step 6: Creating Kafka Consumers

In this final step, we consumed the data in the web server that served the transit status pages to commuters.

Tasks Completed:
- Completed the code in `consumers/consumer.py`, `consumers/models/line.py`, `consumers/models/weather.py`, and `consumers/models/station.py` to consume the data and display it on the website.

## Documentation

In addition to the course content, we referred to the following examples and documentation:

- [Confluent Python Client Documentation](https://docs.confluent.io/current/clients/confluent-kafka-python/#)
- [Confluent Python Client Usage and Examples](https://github.com/confluentinc/confluent-kafka-python#usage)
- [REST Proxy API Reference](https://docs.confluent.io/current/kafka-rest/api.html#post--topics-(string-topic_name))
- [Kafka Connect JDBC Source Connector Configuration Options](https://docs.confluent.io/current/connect/kafka-connect-jdbc/source-connector/source_config_options.html)

## Directory Layout

The project consisted of two main directories, `producers` and `consumers`, with specific tasks indicated in the comments of each file.

## Running and Testing

To run the simulation, we first started up the Kafka ecosystem using Docker Compose:

```bash
%> docker-compose up
```

Once Docker Compose was ready, the following services were available:

| Service                 | Host URL                           | Docker URL                           | Username    | Password |
|-------------------------|------------------------------------|--------------------------------------|-------------|----------|
| Public Transit Status   | [http://localhost:8888](http://localhost:8888) | n/a                                  |             |          |
| Landoop Kafka Connect UI| [http://localhost:8084](http://localhost:8084) | http://connect-ui:8084               |             |          |
| Landoop Kafka Topics UI | [http://localhost:8085](http://localhost:8085) | http://topics-ui:8085                |             |          |
| Landoop Schema Registry UI | [http://localhost:8086](http://localhost:8086) | http://schema-registry-ui:8086       |             |          |
| Kafka                   | PLAINTEXT://localhost:9092,PLAINTEXT://localhost:9093,PLAINTEXT://localhost:9094 | PLAINTEXT://kafka0:9092,PLAINTEXT://kafka1:9093,PLAINTEXT://kafka2:9094 | | |
| REST Proxy              | [http://localhost:8082](http://localhost:8082/) | http://rest-proxy:8082/              |             |          |
| Schema Registry         | [http://localhost:8081](http://localhost:8081/ ) | http://schema-registry:8081/         |             |          |
| Kafka Connect           | [http://localhost:8083](http://localhost:8083) | http://kafka-connect:8083            |             |          |
| KSQL                    | [http://localhost:8088](http://localhost:8088) | http://ksql:8088                     |             |          |
| PostgreSQL              | `jdbc:postgresql://localhost:5432/cta` | `jdbc:postgresql://postgres:5432/cta` | `cta_admin` | `chicago` |

### Running the Simulation

The simulation involved both the `producer` and `consumer` components, which should be run together to complete the end-to-end system.

To run the producer:
```bash
cd producers
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
python simulation.py
```

To run the Faust Stream Processing Application:
```bash
cd consumers
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
faust -A faust_stream worker -l info
```

To run the KSQL Creation Script:
```bash
cd consumers
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
python ksql.py
```

To run the consumer (only after reaching Step 6):
```bash
cd consumers
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
python server.py
```

Running both the producer and consumer together ensures the successful completion of the project.
