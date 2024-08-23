from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, TextLog, Static

class ChatApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield TextLog(name="chat")
        yield Input(placeholder="Type your message here...", name="input")
        yield Footer()

    def on_input_submitted(self, message: Input.Submitted) -> None:
        chat_window = self.query_one(TextLog)
        chat_window.write(f"You: {message.value}")
        message.value = ""  # Clear the input field

if __name__ == "__main__":
    ChatApp().run()

