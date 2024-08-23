from kafka import KafkaConsumer
import json

def consume_and_store_messages(kafka_topic: str, kafka_server: str):
    consumer = KafkaConsumer(
        kafka_topic,
        bootstrap_servers=kafka_server,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    with open("chat_history.json", "a") as file:
        for message in consumer:
            file.write(json.dumps(message.value) + "\n")

