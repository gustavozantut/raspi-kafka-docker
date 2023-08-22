from confluent_kafka.admin import AdminClient, NewTopic

# Define the broker(s) you want to connect to
bootstrap_servers = "192.168.0.101:9092,192.168.14.2:9092"

# Create an AdminClient instance
admin_client = AdminClient({"bootstrap.servers": bootstrap_servers})

# Define topic configuration
topic_config = {
    "topic": "sensors_dht11",
    "partitions": 2,
    "replication.factor": 2,  # Set the desired replication factor
    "config": {
        "min.insync.replicas": 2  # Set the desired minimum in-sync replicas
    }
}

# Create a NewTopic instance
new_topic = NewTopic(
    topic_config["topic"],
    num_partitions=topic_config["partitions"],
    replication_factor=topic_config["replication.factor"],
    config={
        "min.insync.replicas": str(topic_config["config"]["min.insync.replicas"])
    }
)

# Create the topic
admin_client.create_topics([new_topic])
print(admin_client.list_topics().topics)
