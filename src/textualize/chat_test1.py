import threading
from kafka import KafkaProducer, KafkaConsumer
from json import dumps, loads
from datetime import datetime
import json
import time

producer = KafkaProducer(
    bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
    value_serializer=lambda x: dumps(x, default=str).encode('utf-8')
)

consumer = KafkaConsumer(
    'haha',
    bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='chat-group6',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)


def producer_thread():
    try:
        print("채팅 프로그램 - 메시지 발신자")
        print("메시지를 입력하세요. (종료시 'exit' 입력)")

        while True:
            username = "USER3"
            msg = input(f"{username}: ")
            if msg.lower() == 'exit':
                break
            data = {'username': username, 'message': msg, 'time': time.time()}
            producer.send('haha', value=data)
            producer.flush()
    except KeyboardInterrupt:
        print("Producer 종료")
    finally:
        producer.close()

def consumer_thread():
    try:
        print("채팅 프로그램 - 메시지 수신")
        print("메시지 대기 중...")

        for m in consumer:
            data = m.value
            sender = data['username']
            formatted_time = datetime.fromtimestamp(data['time']).strftime('%Y-%m-%d %H:%M:%S')
            chatting_log = {
                'received_time': formatted_time,
                'message': data['message'],
                'sender': sender
            }

            print(f"(받은 시간 : {formatted_time}) [{sender}]: {data['message']}")
            chatting_history.append(chatting_log)
    except KeyboardInterrupt:
        print("Consumer 종료")
    finally:
        consumer.close()

producer_thread_instance = threading.Thread(target=producer_thread)
consumer_thread_instance = threading.Thread(target=consumer_thread)

producer_thread_instance.start()
consumer_thread_instance.start()

producer_thread_instance.join()
consumer_thread_instance.join()

