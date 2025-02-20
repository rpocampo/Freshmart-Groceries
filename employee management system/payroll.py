import pika
import json

class PayrollService:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='payroll_service')

    def process_message(self, ch, method, properties, body):
        message = json.loads(body)
        if message['action'] == 'process_salary':
            print(f"Processing salary for Employee ID {message['data']}")
        else:
            print("Unknown action received.")

    def start_listening(self):
        self.channel.basic_consume(queue='payroll_service', on_message_callback=self.process_message, auto_ack=True)
        print("Payroll Service started listening...")
        self.channel.start_consuming()

if __name__ == "__main__":
    service = PayrollService()
    service.start_listening()
