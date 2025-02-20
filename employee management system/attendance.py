import pika
import json

class AttendanceService:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='attendance_service')

    def process_message(self, ch, method, properties, body):
        message = json.loads(body)
        if message['action'] == 'mark_attendance':
            print(f"Marking attendance for Employee ID {message['data']}")
        else:
            print("Unknown action received.")

    def start_listening(self):
        self.channel.basic_consume(queue='attendance_service', on_message_callback=self.process_message, auto_ack=True)
        print("Attendance Service started listening...")
        self.channel.start_consuming()

if __name__ == "__main__":
    service = AttendanceService()
    service.start_listening()
