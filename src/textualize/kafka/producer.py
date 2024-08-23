from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static
from textual.scroll_view import ScrollView
from kafka import KafkaProducer
import json

class MyApp(App):
    def compose(self) -> ComposeResult:
        self.chat_content = Static("")
        self.scroll_view = ScrollView(self.chat_content)
        
        yield Header()
        yield self.scroll_view
        self.input_field = Input(placeholder="Type something...", name="input")
        yield self.input_field
        yield Footer()
        
        self.kafka_topic = "chat"
        self.kafka_server = "localhost:9092"
        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_server,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def on_input_submitted(self, message: Input.Submitted) -> None:
        user_message = message.value.strip()
        
        if user_message.lower() == 'bye':
            self.exit()
            return
        
        new_content = f"{self.chat_content.renderable}\nYou: {user_message}"
        self.chat_content.update(new_content)
        
        self.producer.send(self.kafka_topic, {"message": user_message})
        self.input_field.value = ""

