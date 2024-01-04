from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock
import wolframalpha
app_id = "3WRQQ2-UA6H4JP223"
client = wolframalpha.Client(app_id)
Window.size = (dp(250),dp(350))

class ChatBotApp(App):
    def build(self):
        # Layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # ScrollView for messages
        scroll_view = ScrollView(size_hint=(1, 0.93))
        self.message_layout = BoxLayout(orientation='vertical', spacing=2, size_hint_y=None)
        self.message_layout.bind(minimum_height=self.message_layout.setter('height'))
        scroll_view.add_widget(self.message_layout)
        layout.add_widget(scroll_view)

        sublayout = GridLayout(spacing=10, cols=2, size_hint=(1, 0.07))
        # Text Input
        self.text_input = TextInput(multiline=False, size_hint=(0.9, 0.07), hint_text="Type your query here...")
        sublayout.add_widget(self.text_input)

        # Enter Button
        self.enter_button = Button(text='Enter', size_hint=(0.1, 0.07), disabled=True)
        self.enter_button.bind(on_press=self.on_enter_button_press)
        sublayout.add_widget(self.enter_button)
        layout.add_widget(sublayout)

        
        self.text_input.bind(text=self.on_text_input_change,on_text_validate=self.on_enter_button_press)

        return layout

    def on_text_input_change(self, instance, value):
        
        self.enter_button.disabled = not bool(value)

    def on_enter_button_press(self, instance):

        input_text = self.text_input.text

        if input_text:
            try:

                res = client.query(input_text)
                output_text = next(res.results).text

                

                # Add input and output labels to message layout
                input_label = Label(
                    text=f'User: {input_text}',
                    size_hint_y=None,
                    text_size=(self.message_layout.width, None),
                    color=(0.5, 1, 0.9, 1)  
                )

                output_label = Label(
                    text=f'Response: {output_text}',
                    size_hint_y=None,
                    text_size=(self.message_layout.width, None),
                    color=(0.4, 0.6, 1, 1)  
                )

                self.message_layout.add_widget(input_label)
                self.message_layout.add_widget(output_label)


                Clock.schedule_once(lambda dt: self.update_texture_size(input_label))
                Clock.schedule_once(lambda dt: self.update_texture_size(output_label))

            except Exception as e:
                # Displaying a user-friendly error message
                error_message = f"Error: {str(e)}"
                error_label = Label(
                    text=error_message,
                    size_hint_y=None,
                    text_size=(self.message_layout.width, None),
                    color=(1, 0, 0, 1)  
                )
                self.message_layout.add_widget(error_label)

            finally:
                # Clear text input
                self.text_input.text = ''

                # Scroll to the latest message
                self.message_layout.parent.scroll_y = 0


    def update_texture_size(self, label):
        label.height = max(dp(50), label.texture_size[1])


    
ChatBotApp().run()
