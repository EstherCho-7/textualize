from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static
from textual.scroll_view import ScrollView
import json

class MyApp(App):
    def compose(self) -> ComposeResult:
        # 초기 Static 위젯을 생성하여 ScrollView에 추가합니다.
        self.chat_content = Static("")
        self.scroll_view = ScrollView(self.chat_content)
        
        yield Header()
        yield self.scroll_view
        yield Input(placeholder="Type something...", name="input")
        yield Footer()

    def on_input_submitted(self, message: Input.Submitted) -> None:
        # 입력된 메시지를 Static 위젯의 내용에 추가합니다.
        if message.value.strip().lower()=="bye":
            self.save_chat_history()
            self.exit()
            return
        new_content = f"{self.chat_content.renderable}\nYou: {message.value}"
        self.chat_content.update(new_content)
        # 입력 필드를 비웁니다.
        #message.value = ""
        
        input_field=self.query_one(Input)
        if input_field:
            input_field.value=""

        self.save_chat_history(message.value)

    def save_chat_history(self, message=None) -> None:
        chat_history_file="chat_history.json"
        chat_messages=[]

        try:
            with open(chat_history_file, "r") as file:
                chat_messages=json.load(file)
        except FileNotFoundError:
            pass

        if message:
            # json에 들어갈 dictionary 값
            chat_messages.append({"message": message})

        with open(chat_history_file, "w") as file:
            json.dump(chat_messages, file, indent=4)

MyApp().run()
