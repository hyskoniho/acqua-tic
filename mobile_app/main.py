# Kivy imports
from kivy.app import App
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.image import Image as CoreImage

# Python imports
from io import BytesIO
from base64 import b64decode
import sys, traceback
from dotenv import load_dotenv
load_dotenv() # Load environment variables

# Local imports
import database as db

if platform != 'android':
    from kivy.config import Config
    from kivy.core.window import Window
    Window.size = (360, 640)
else:
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.ACCESS_WIFI_STATE, Permission.CHANGE_WIFI_STATE])
    
class MainApp(App):
    def build(self):
        self.icon = 'aquarium.ico'
        
        root = FloatLayout(size_hint=(1,1))
        layout = BoxLayout(orientation='vertical', size_hint=(1, 1), spacing=15, padding=5)
        
        with layout.canvas.before:
            Color(0, 180/255, 216/255, 1)
            self.rect = Rectangle(pos=layout.pos, size=layout.size)
            
        def update_background(instance, value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size

        layout.bind(size=update_background, pos=update_background)

        self.img = Image(size_hint=(1, 0.6), allow_stretch=True, keep_ratio=True)
        layout.add_widget(self.img)
        
        remaining_layout = BoxLayout(orientation='vertical', padding=10, spacing=15, size_hint=(1, 0.3))

        temp_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4))
        temp_label = Label(text='[b]Temperatura[/b]', markup=True, size_hint=(None, 0.3), color='#03045E', halign='left', padding=(25, 0, 0, 0))
        temp_layout.add_widget(temp_label)
        
        temp_field_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.7), spacing=10)
        self.temp_value = TextInput(text='...', size_hint=(0.5, 0.8), readonly=True, background_color='#CAF0F8', is_focusable=False, foreground_color='#03045E', allow_copy=False, multiline=False, font_size=70, halign='center')
        self.temp_button = Button(text='🌡️', size_hint=(0.2, 0.8), background_color='#03045E', color='#CAF0F8', markup=True)
        self.temp_button.bind(on_press=lambda x: self.send_command('heat'))
        temp_field_layout.add_widget(self.temp_value)
        temp_field_layout.add_widget(self.temp_button)
        temp_layout.add_widget(temp_field_layout)
        remaining_layout.add_widget(temp_layout)

        lum_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4))
        lum_label = Label(text='[b]Luminosidade[/b]', markup=True, size_hint=(None, 0.3), color='#03045E', halign='left', padding=(25, 0, 0, 0))
        lum_layout.add_widget(lum_label)
        
        lum_field_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.7), spacing=10)
        self.lum_value = TextInput(text='...', size_hint=(0.5, 0.8), readonly=True, background_color='#CAF0F8', is_focusable=False, foreground_color='#03045E', allow_copy=False, multiline=False, font_size=70, halign='center')
        self.lum_button = Button(text='💡', size_hint=(0.2, 0.8), background_color='#03045E', color='#CAF0F8', markup=True)
        self.lum_button.bind(on_press=lambda x: self.send_command('lamp'))
        lum_field_layout.add_widget(self.lum_value)
        lum_field_layout.add_widget(self.lum_button)
        lum_layout.add_widget(lum_field_layout)
        remaining_layout.add_widget(lum_layout)
        
        layout.add_widget(remaining_layout)
        
        status_layout = BoxLayout(size_hint=(1,0.1), orientation='horizontal', spacing=1, padding=25)
        status_layout.add_widget(Label(text='[b]Status: [/b]', markup=True, color='#03045E', size_hint=(None, None), halign='right'))
        self.status_label = Label(text='Carregando...', color='#03045E', size_hint=(None,None), halign='left')
        status_layout.add_widget(self.status_label)
        layout.add_widget(status_layout)
        
        root.add_widget(layout)
        Clock.schedule_interval(self.load_values, 0.5)
        self.stts = True
        
        return root
    
    def show_error(self, error_message):
        content = BoxLayout(orientation='vertical', size_hint=(1, 1), spacing=10, padding=15)
        
        scroll = ScrollView(size_hint=(1, 0.92))
        scroll.add_widget(Label(text=str(error_message), size_hint=(None, None), text_size=(None, None), halign='left', color='#CAF0F8'))
        content.add_widget(scroll)

        close_button = Button(text='Close', size_hint=(1, 0.08), halign='center')
        close_button.bind(on_press=self.close_popup)
        content.add_widget(close_button)

        self.popup = Popup(title='error...', content=content, size_hint=(0.8, 0.75))
        self.popup.open()

    def close_popup(self, instance):
        self.popup.dismiss()
        
    @staticmethod
    def process_image(image: str | bytes) -> Texture:
        if isinstance(image, str):
            image = BytesIO(b64decode(image))
        elif isinstance(image, bytes):
            image = BytesIO(image)
        return CoreImage(image, ext='png').texture
    
    def send_command(self, instance, value):
        try:
            db.set_command(value)
        except:
            if self.stts:
                self.stts = False
                self.show_error('.'.join(traceback.format_exception(*sys.exc_info())))
        else: 
            if not self.stts: self.stts = True
    
    def load_values(self, instance):
        try:
            values: dict = db.get_collection()
            
            if values['heat']:
                self.temp_button.text = '[b]ON[/b]'
                self.temp_button.background_color = '#03045E'
                self.temp_button.color = '#CAF0F8'
                
            
            else:
                self.temp_button.text = '[b]OFF[/b]'
                self.temp_button.background_color = '#CAF0F8'
                self.temp_button.color = '#03045E'

            if values['lamp']:
                self.lum_button.text = '[b]ON[/b]'
                self.lum_button.background_color = '#03045E'
                self.lum_button.color = '#CAF0F8'
                
            
            else:
                self.lum_button.text = '[b]OFF[/b]'
                self.lum_button.background_color = '#CAF0F8'
                self.lum_button.color = '#03045E'
            
            t: float = values['temp']
            l: int = values['lux']
            self.temp_value.text = f'{t:.2f}°C'
            self.lum_value.text = f'{l}%'
            
            self.img.texture = self.process_image(values['image'])
    
        except:
            self.status_label.text = r'offline!'
            self.status_label.color = '#930000'
            
            if self.stts:
                self.stts = False
                self.show_error('.'.join(traceback.format_exception(*sys.exc_info())))

        else:
            self.status_label.text = r'online!'
            self.status_label.color = '#017a32'

if __name__ == '__main__':
    MainApp().run()
