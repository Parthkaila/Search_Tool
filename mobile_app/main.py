from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
import requests
import json
from datetime import datetime


class GoogleMapsScraper(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.collected_data = []
        self.is_collecting = False
        
        # Title
        title = Label(
            text='Google Maps Data Collector',
            size_hint=(1, 0.08),
            font_size='20sp',
            bold=True,
            color=(0.2, 0.6, 1, 1)
        )
        self.add_widget(title)
        
        # Server URL input
        server_layout = BoxLayout(size_hint=(1, 0.08), spacing=5)
        server_layout.add_widget(Label(text='Server URL:', size_hint=(0.3, 1)))
        self.server_input = TextInput(
            text='http://your-server.onrender.com',
            multiline=False,
            size_hint=(0.7, 1)
        )
        server_layout.add_widget(self.server_input)
        self.add_widget(server_layout)
        
        # Keywords input
        self.add_widget(Label(text='Keywords (one per line):', size_hint=(1, 0.05)))
        self.keywords_input = TextInput(
            hint_text='restaurant\ndentist\ngym',
            multiline=True,
            size_hint=(1, 0.2)
        )
        self.add_widget(self.keywords_input)
        
        # Location input
        location_layout = BoxLayout(size_hint=(1, 0.08), spacing=5)
        location_layout.add_widget(Label(text='Location:', size_hint=(0.3, 1)))
        self.location_input = TextInput(
            hint_text='e.g., Mumbai, India',
            multiline=False,
            size_hint=(0.7, 1)
        )
        location_layout.add_widget(self.location_input)
        self.add_widget(location_layout)
        
        # Max results
        max_layout = BoxLayout(size_hint=(1, 0.08), spacing=5)
        max_layout.add_widget(Label(text='Max Results:', size_hint=(0.3, 1)))
        self.max_results_input = TextInput(
            text='20',
            multiline=False,
            input_filter='int',
            size_hint=(0.7, 1)
        )
        max_layout.add_widget(self.max_results_input)
        self.add_widget(max_layout)
        
        # Filter options
        filter_layout = GridLayout(cols=1, size_hint=(1, 0.12), spacing=5)
        
        dup_layout = BoxLayout(size_hint=(1, 0.5))
        self.remove_dup_checkbox = CheckBox(active=True, size_hint=(0.1, 1))
        dup_layout.add_widget(self.remove_dup_checkbox)
        dup_layout.add_widget(Label(text='Remove duplicates', size_hint=(0.9, 1)))
        filter_layout.add_widget(dup_layout)
        
        phone_layout = BoxLayout(size_hint=(1, 0.5))
        self.remove_nophone_checkbox = CheckBox(active=False, size_hint=(0.1, 1))
        phone_layout.add_widget(self.remove_nophone_checkbox)
        phone_layout.add_widget(Label(text='Remove without phone', size_hint=(0.9, 1)))
        filter_layout.add_widget(phone_layout)
        
        self.add_widget(filter_layout)
        
        # Progress bar
        self.progress_bar = ProgressBar(max=100, size_hint=(1, 0.06))
        self.add_widget(self.progress_bar)
        
        # Status label
        self.status_label = Label(
            text='Ready to collect data',
            size_hint=(1, 0.06),
            color=(0.3, 0.7, 0.3, 1)
        )
        self.add_widget(self.status_label)
        
        # Results count
        self.results_label = Label(
            text='Collected: 0 rows',
            size_hint=(1, 0.05)
        )
        self.add_widget(self.results_label)
        
        # Buttons
        button_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        self.collect_btn = Button(
            text='Collect Data',
            background_color=(0.2, 0.6, 1, 1),
            bold=True
        )
        self.collect_btn.bind(on_press=self.start_collection)
        button_layout.add_widget(self.collect_btn)
        
        self.stop_btn = Button(
            text='Stop',
            background_color=(1, 0.3, 0.3, 1),
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_collection)
        button_layout.add_widget(self.stop_btn)
        
        self.export_btn = Button(
            text='Export Excel',
            background_color=(0.2, 0.8, 0.4, 1),
            disabled=True
        )
        self.export_btn.bind(on_press=self.export_to_excel)
        button_layout.add_widget(self.export_btn)
        
        self.add_widget(button_layout)
    
    def start_collection(self, instance):
        keywords = [k.strip() for k in self.keywords_input.text.split('\n') if k.strip()]
        if not keywords:
            self.status_label.text = 'Error: Enter at least one keyword'
            self.status_label.color = (1, 0.3, 0.3, 1)
            return
        
        server_url = self.server_input.text.strip()
        if not server_url:
            self.status_label.text = 'Error: Enter server URL'
            self.status_label.color = (1, 0.3, 0.3, 1)
            return
        
        self.is_collecting = True
        self.collect_btn.disabled = True
        self.stop_btn.disabled = False
        self.export_btn.disabled = True
        self.progress_bar.value = 0
        self.collected_data = []
        
        # Start collection in background
        Clock.schedule_once(lambda dt: self.collect_data(keywords, server_url), 0.1)
    
    def collect_data(self, keywords, server_url):
        try:
            location = self.location_input.text.strip()
            max_results = int(self.max_results_input.text or '20')
            
            for index, keyword in enumerate(keywords):
                if not self.is_collecting:
                    break
                
                self.status_label.text = f'Collecting: {keyword}'
                self.status_label.color = (0.2, 0.6, 1, 1)
                
                # Make API request to backend server
                try:
                    response = requests.post(
                        f'{server_url}/api/scrape',
                        json={
                            'keyword': keyword,
                            'location': location,
                            'max_results': max_results
                        },
                        timeout=300
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        results = data.get('results', [])
                        self.collected_data.extend(results)
                        self.results_label.text = f'Collected: {len(self.collected_data)} rows'
                    else:
                        self.status_label.text = f'Error: {response.status_code}'
                        self.status_label.color = (1, 0.3, 0.3, 1)
                
                except requests.exceptions.RequestException as e:
                    self.status_label.text = f'Connection error: {str(e)[:50]}'
                    self.status_label.color = (1, 0.3, 0.3, 1)
                
                self.progress_bar.value = ((index + 1) / len(keywords)) * 100
            
            if self.is_collecting:
                self.status_label.text = 'Collection completed!'
                self.status_label.color = (0.2, 0.8, 0.4, 1)
            else:
                self.status_label.text = 'Collection stopped by user'
                self.status_label.color = (1, 0.6, 0.2, 1)
            
            self.collect_btn.disabled = False
            self.stop_btn.disabled = True
            if self.collected_data:
                self.export_btn.disabled = False
            
        except Exception as e:
            self.status_label.text = f'Error: {str(e)[:50]}'
            self.status_label.color = (1, 0.3, 0.3, 1)
            self.collect_btn.disabled = False
            self.stop_btn.disabled = True
    
    def stop_collection(self, instance):
        self.is_collecting = False
        self.status_label.text = 'Stopping collection...'
        self.status_label.color = (1, 0.6, 0.2, 1)
    
    def export_to_excel(self, instance):
        try:
            response = requests.post(
                f'{self.server_input.text.strip()}/api/export-excel',
                json={
                    'data': self.collected_data,
                    'remove_duplicates': self.remove_dup_checkbox.active,
                    'remove_without_phone': self.remove_nophone_checkbox.active
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                row_count = result.get('rows', len(self.collected_data))
                self.status_label.text = f'Excel created: {row_count} rows'
                self.status_label.color = (0.2, 0.8, 0.4, 1)
            else:
                self.status_label.text = f'Export error: {response.status_code}'
                self.status_label.color = (1, 0.3, 0.3, 1)
        
        except Exception as e:
            self.status_label.text = f'Export error: {str(e)[:50]}'
            self.status_label.color = (1, 0.3, 0.3, 1)


class GoogleMapsScraperApp(App):
    def build(self):
        return GoogleMapsScraper()


if __name__ == '__main__':
    GoogleMapsScraperApp().run()
