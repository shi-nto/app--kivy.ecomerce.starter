# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.button import Button
import numpy as np

# Define the UI using Kivy language
kv_string = '''
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 10
    
    TextInput:
        id: text_input
        hint_text: 'Enter text here'
        font_size: 18
        multiline: False
        size_hint_y: None
        height: 50
    
    Label:
        id: response_label
        text: 'Button response will appear here'
        font_size: 16
        size_hint_y: None
        height: 50
        halign: 'center'
    
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: 60
        spacing: 10
        
        AnimatedButton:
            text: 'Button 1'
            on_press: app.button1_pressed()
            canvas.before:
                PushMatrix
                Scale:
                    origin: self.center
                    x: self.scale
                    y: self.scale
            canvas.after:
                PopMatrix
        
        AnimatedButton:
            text: 'Button 2'
            on_press: app.button2_pressed()
            canvas.before:
                PushMatrix
                Scale:
                    origin: self.center
                    x: self.scale
                    y: self.scale
            canvas.after:
                PopMatrix
'''

class AnimatedButton(Button):
    background_color = ListProperty([1, 1, 1, 1])
    scale = NumericProperty(1.0)
    
    def __init__(self, **kwargs):
        super(AnimatedButton, self).__init__(**kwargs)
        self.original_size = None
        self.bind(on_press=self.animate_press)
        self.bind(on_release=self.animate_release)
        Clock.schedule_once(self.start_idle_animation, 0.5)

    def on_size(self, *args):
        self.original_size = self.size

    def animate_press(self, instance):
        # Generate color values using NumPy
        color = np.array([0.8, 0.2, 0.2, 1.0])
        Animation(background_color=list(color), scale=0.95, duration=0.1).start(self)
        
    def animate_release(self, instance):
        # Reset to original state
        base_color = np.array([0.3, 0.6, 1.0, 1.0])
        Animation(background_color=list(base_color), scale=1.0, duration=0.2).start(self)
        
    def start_idle_animation(self, dt):
        # Use NumPy to create a pulsating effect for idle state
        self.pulse_time = 0
        Clock.schedule_interval(self.update_pulse, 1/30)
        
    def update_pulse(self, dt):
        self.pulse_time += dt
        # Use NumPy to calculate smooth color pulsation based on sine wave
        base_color = np.array([0.3, 0.6, 1.0, 1.0])
        pulse_factor = (np.sin(self.pulse_time * 2) * 0.1) + 0.9
        pulse_color = base_color * pulse_factor
        # Clamp values to valid range
        pulse_color = np.clip(pulse_color, 0.0, 1.0)
        # Convert NumPy values to Python native types
        self.background_color = [float(c) for c in pulse_color]
        
        # Subtle size pulsation with explicit float conversion
        size_pulse = (np.sin(self.pulse_time * 1.5) * 0.03) + 1.0
        # Convert NumPy float64 to Python float
        self.scale = float(size_pulse)

class BasicApp(App):
    def build(self):
        # Load the UI from the kv string
        return Builder.load_string(kv_string)
    
    def button1_pressed(self):
        text = self.root.ids.text_input.text
        response = f"Button 1 pressed! Text is: {text}"
        print(response)
        self.root.ids.response_label.text = response
    
    def button2_pressed(self):
        text = self.root.ids.text_input.text
        response = f"Button 2 pressed! Text is: {text}"
        print(response)
        self.root.ids.response_label.text = response

if __name__ == '__main__':
    BasicApp().run()