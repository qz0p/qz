from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Line, Rectangle
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.app import App
from utils import menu, findout, PASTEL_COLORS
from datetime import datetime, timedelta
import random
import json

# 한글 폰트 등록
LabelBase.register(name="GabiaHeuldot", fn_regular="fonts/GabiaHeuldot.ttf")
# KV 파일 로드
Builder.load_file('timetable.kv')

class CustomButton(Button):
    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        self.canvas.before.clear()


        with self.canvas.before:
            Color(0, 0, 0, 1)  # 버튼 배경을 검은색으로 설정
            self.rect = Rectangle(size=self.size, pos=self.pos)
            Color(1, 1, 1, 1)  # 테두리 색상은 흰색으로 설정
            self.line = Line(rectangle=(self.x, self.y, self.width, self.height), width=2)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.line.rectangle = [self.x, self.y, self.width, self.height]

class TimeTableScreen(Screen):
    date = StringProperty()
    grade = StringProperty()
    cla = StringProperty()

    def on_pre_enter(self):
        self.date = datetime.today().strftime('%Y-%m-%d')
        Clock.schedule_once(self.load_data, 0)

    def load_data(self, dt):
        self.ids.timetable_grid.clear_widgets()
        headers = ["교시", "오늘", "내일", "모레"]
        for header in headers:
            label = Label(text=header, font_size=18, bold=True, color=(1, 1, 1, 1), font_name="GabiaHeuldot")
            self.ids.timetable_grid.add_widget(label)

        timetable_data = []
        start_date = datetime.today()

        for offset in range(3):  # 오늘, 내일, 모레
            target_date = (start_date + timedelta(days=offset)).strftime("%Y%m%d")
            timetable = findout(self.grade, self.cla, target_date)
            timetable_data.append(timetable)

        for period in range(1, 8):
            self.ids.timetable_grid.add_widget(Label(text=f"{period}교시", font_size=18, color=(1, 1, 1, 1), font_name="GabiaHeuldot"))
            for day_index, timetable in enumerate(timetable_data):
                period_subject = next((item for item in timetable if "time" in item and int(item["time"]) == period), None)
                if period_subject:
                    subject, color = period_subject["subject"], random.choice(PASTEL_COLORS)
                    box = BoxLayout(size_hint_y=None, height=60, padding=5, spacing=5)
                    with box.canvas.before:
                        Color(*color)
                        Rectangle(size=box.size, pos=box.pos)
                    label = Label(text=subject, font_size=18, color=(1, 1, 1, 1), font_name="GabiaHeuldot")
                    box.add_widget(label)
                    self.ids.timetable_grid.add_widget(box)
                else:
                    self.ids.timetable_grid.add_widget(Label(text="없음", font_size=18, color=(1, 1, 1, 1), font_name="GabiaHeuldot"))

    def save_timetable(self):
        timetable_data = []
        start_date = datetime.today()
        for offset in range(3):  # 오늘, 내일, 모레
            target_date = (start_date + timedelta(days=offset)).strftime("%Y%m%d")
            timetable = findout(self.grade, self.cla, target_date)
            timetable_data.append(timetable)

        with open("timetable.json", "w", encoding='utf-8') as file:
            json.dump(timetable_data, file, ensure_ascii=False, indent=4)

class MenuScreen(Screen):
    def on_pre_enter(self):
        self.date = datetime.today().strftime('%Y%m%d')
        Clock.schedule_once(self.load_data, 0)

    def load_data(self, dt):
        today = datetime.today().strftime("%Y%m%d")
        menu_list = menu(today)
        self.ids.meal_schedule_grid.clear_widgets()
        for dish in menu_list:
            box = BoxLayout(size_hint_y=None, height=40, padding=5, spacing=5)
            label = Label(text=dish, font_size=18, size_hint_y=None, height=40, font_name="GabiaHeuldot", color=(1, 1, 1, 1))
            box.add_widget(label)
            self.ids.meal_schedule_grid.add_widget(box)

class MyApp(App):
    def build(self):
        sm = ScreenManager(transition=WipeTransition())
        timetable_screen = TimeTableScreen(name='timetable')
        menu_screen = MenuScreen(name='menu')
        sm.add_widget(timetable_screen)
        sm.add_widget(menu_screen)

        layout = BoxLayout(orientation='vertical')
        nav_layout = BoxLayout(size_hint_y=None, height=50)
        timetable_btn = CustomButton(text='TimeTable', on_release=lambda x: setattr(sm, 'current', 'timetable'))
        menu_btn = CustomButton(text='Menu', on_release=lambda x: setattr(sm, 'current', 'menu'))
        save_btn = CustomButton(text='Save TimeTable', on_release=lambda x: timetable_screen.save_timetable())

        nav_layout.add_widget(timetable_btn)
        nav_layout.add_widget(menu_btn)
        nav_layout.add_widget(save_btn)

        input_layout = BoxLayout(size_hint_y=None, height=50)
        grade_input = TextInput(hint_text='Grade', multiline=False)
        class_input = TextInput(hint_text='Class', multiline=False)
        set_button = Button(text='Set', on_release=lambda x: self.set_class(timetable_screen, grade_input.text, class_input.text))

        input_layout.add_widget(Label(text='Grade:'))
        input_layout.add_widget(grade_input)
        input_layout.add_widget(Label(text='Class:'))
        input_layout.add_widget(class_input)
        input_layout.add_widget(set_button)

        main_content = BoxLayout()
        main_content.add_widget(sm)  # 메인 컨텐츠 추가

        layout.add_widget(input_layout)  # 입력 필드 추가
        layout.add_widget(main_content)  # 전체 레이아웃에 메인 컨텐츠 추가
        layout.add_widget(nav_layout)  # 네비게이션 버튼을 하단으로 이동
        return layout

    def set_class(self, timetable_screen, grade, cla):
        timetable_screen.grade = grade
        timetable_screen.cla = cla
        timetable_screen.load_data(None)

if __name__ == '__main__':
    MyApp().run()
