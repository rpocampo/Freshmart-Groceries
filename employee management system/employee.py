import pika
import json

class EmployeeService:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='employee_service')

    def process_message(self, ch, method, properties, body):
        message = json.loads(body)
        if message['action'] == 'add_employee':
            print(f"Adding employee: {message['data']}")
        elif message['action'] == 'get_employee':
            print(f"Fetching employee data for: {message['data']}")
        else:
            print("Unknown action received.")

    def start_listening(self):
        self.channel.basic_consume(queue='employee_service', on_message_callback=self.process_message, auto_ack=True)
        print("Employee Service started listening...")
        self.channel.start_consuming()

if __name__ == "__main__":
    service = EmployeeService()
    service.start_listening()
