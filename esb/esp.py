import pika
import json

class ESB:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='esb_queue')

    def publish_message(self, service, message):
        self.channel.basic_publish(
            exchange='', 
            routing_key=service, 
            body=json.dumps(message)
        )
        print(f"Message sent to {service}: {message}")

    def start_listening(self):
        def callback(ch, method, properties, body):
            message = json.loads(body)
            service = message['service']
            print(f"ESB received message: {message}")
            self.publish_message(service, message)

        self.channel.basic_consume(queue='esb_queue', on_message_callback=callback, auto_ack=True)
        print("ESB started listening...")
        self.channel.start_consuming()

if __name__ == "__main__":
    esb = ESB()
    esb.start_listening()
