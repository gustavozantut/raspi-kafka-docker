from kafka import KafkaConsumer

bootstrap_servers = "100.108.104.205:9092,100.108.97.215:9092,100.108.97.215:9093"  # Replace with the IP address of your Kafka broker
kafka_topic = "plate_detector"  # Use the same topic name that you used in the producer script

def consume_kafka_data():
    consumer = KafkaConsumer(
        kafka_topic,
        bootstrap_servers=bootstrap_servers,
        group_id="dht11_consumer_1",
        value_deserializer=lambda x: x.decode('utf-8')  # Specify the deserializer for the message value
    )

    for message in consumer:
        print(f"Received:\n {message.value}")

if __name__ == "__main__":
    consume_kafka_data()