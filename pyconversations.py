# -*- coding: utf-8 -*-
#
# This file created with KivyCreatorProject
# <https://github.com/HeaTTheatR/KivyCreatorProgect
#
# Copyright В© 2017 Easy
#
# For suggestions and questions:
# <kivydevelopment@gmail.com>
# 
# LICENSE: MIT

import os
import sys
from ast import literal_eval

from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.clock import Clock
from kivy.utils import get_color_from_hex, get_hex_from_color
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty

from main import __version__
from libs.translation import Translation
from libs.uix.baseclass.startscreen import StartScreen
from libs.uix.lists import Lists
from libs.utils.showplugins import ShowPlugins

from kivymd.theming import ThemeManager
from kivymd.label import MDLabel

from toast import toast
from dialogs import card


class PyConversations(App):
    '''Р¤СѓРЅРєС†РёРѕРЅР°Р» РїСЂРѕРіСЂР°РјРјС‹.'''

    title = 'PyConversations'
    icon = 'icon.png'
    nav_drawer = ObjectProperty()
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Grey'
    lang = StringProperty('en')

    def __init__(self, **kvargs):
        super(PyConversations, self).__init__(**kvargs)
        Window.bind(on_keyboard=self.events_program)
        Window.soft_input_mode = 'below_target'

        self.list_previous_screens = ['base']
        self.window = Window
        self.plugin = ShowPlugins(self)
        self.config = ConfigParser()
        self.manager = None
        self.window_language = None
        self.exit_interval = False
        self.dict_language = literal_eval(
            open(
                os.path.join(self.directory, 'data', 'locales', 'locales.txt')).read()
        )
        self.translation = Translation(
            self.lang, 'Ttest', os.path.join(self.directory, 'data', 'locales')
        )

    def get_application_config(self):
        return super(PyConversations, self).get_application_config(
                        '{}/%(appname)s.ini'.format(self.directory))

    def build_config(self, config):
        '''РЎРѕР·РґР°С‘С‚ С„Р°Р№Р» РЅР°СЃС‚СЂРѕРµРє РїСЂРёР»РѕР¶РµРЅРёСЏ pyconversations.ini.'''

        config.adddefaultsection('General')
        config.setdefault('General', 'language', 'en')

    def set_value_from_config(self):
        '''РЈСЃС‚Р°РЅР°РІР»РёРІР°РµС‚ Р·РЅР°С‡РµРЅРёСЏ РїРµСЂРµРјРµРЅРЅС‹С… РёР· С„Р°Р№Р»Р° РЅР°СЃС‚СЂРѕРµРє pyconversations.ini.'''

        self.config.read(os.path.join(self.directory, 'pyconversations.ini'))
        self.lang = self.config.get('General', 'language')

    def build(self):
        self.set_value_from_config()
        self.load_all_kv_files(os.path.join(self.directory, 'libs', 'uix', 'kv'))
        self.screen = StartScreen()  # РіР»Р°РІРЅС‹Р№ СЌРєСЂР°РЅ РїСЂРѕРіСЂР°РјРјС‹
        self.manager = self.screen.ids.manager
        self.nav_drawer = self.screen.ids.nav_drawer

        return self.screen

    def load_all_kv_files(self, directory_kv_files):
        for kv_file in os.listdir(directory_kv_files):
            kv_file = os.path.join(directory_kv_files, kv_file)
            if os.path.isfile(kv_file):
                with open(kv_file, encoding='utf-8') as kv:
                    Builder.load_string(kv.read())

    def events_program(self, instance, keyboard, keycode, text, modifiers):
        '''Р’С‹Р·С‹РІР°РµС‚СЃСЏ РїСЂРё РЅР°Р¶Р°С‚РёРё РєРЅРѕРїРєРё РњРµРЅСЋ РёР»Рё Back Key
        РЅР° РјРѕР±РёР»СЊРЅРѕРј СѓСЃС‚СЂРѕР№СЃС‚РІРµ.'''

        if keyboard in (1001, 27):
            if self.nav_drawer.state == 'open':
                self.nav_drawer.toggle_nav_drawer()
            self.back_screen(event=keyboard)
        elif keyboard in (282, 319):
            pass

        return True

    def back_screen(self, event=None):
        '''РњРµРЅРµРґР¶РµСЂ СЌРєСЂР°РЅРѕРІ. Р’С‹Р·С‹РІР°РµС‚СЃСЏ РїСЂРё РЅР°Р¶Р°С‚РёРё Back Key
        Рё С€РµРІСЂРѕРЅР° "РќР°Р·Р°Рґ" РІ ToolBar.'''

        # РќР°Р¶Р°С‚Р° BackKey.
        if event in (1001, 27):
            if self.manager.current == 'base':
                self.dialog_exit()
                return
            try:
                self.manager.current = self.list_previous_screens.pop()
            except:
                self.manager.current = 'base'
            self.screen.ids.action_bar.title = self.title
            self.screen.ids.action_bar.left_action_items = \
                [['menu', lambda x: self.nav_drawer._toggle()]]

    def show_plugins(self, *args):
        '''Р’С‹РІРѕРґРёС‚ РЅР° СЌРєСЂР°РЅ СЃРїРёСЃРѕРє РїР»Р°РіРёРЅРѕРІ.'''

        self.plugin.show_plugins()

    def show_about(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.screen.ids.about.ids.label.text = \
            self.translation._(
                u'[size=20][b]PyConversations[/b][/size]\n\n'
                u'[b]Version:[/b] {version}\n'
                u'[b]License:[/b] MIT\n\n'
                u'[size=20][b]Developer[/b][/size]\n\n'
                u'[ref=SITE_PROJECT]'
                u'[color={link_color}]NAME_AUTHOR[/color][/ref]\n\n'
                u'[b]Source code:[/b] '
                u'[ref=https://github.com/User/PyConversations]'
                u'[color={link_color}]GitHub[/color][/ref]').format(
                version=__version__,
                link_color=get_hex_from_color(self.theme_cls.primary_color)
            )
        self.manager.current = 'about'
        self.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.back_screen(27)]]

    def show_license(self, *args):
        self.screen.ids.license.ids.text_license.text = \
            self.translation._('%s') % open(
                os.path.join(self.directory, 'LICENSE'), encoding='utf-8').read()
        self.nav_drawer._toggle()
        self.manager.current = 'license'
        self.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.back_screen()]]
        self.screen.ids.action_bar.title = \
            self.translation._('MIT LICENSE')

    def select_locale(self, *args):
        '''Р’С‹РІРѕРґРёС‚ РѕРєРЅРѕ СЃРѕ СЃРїРёСЃРєРѕРј РёРјРµСЋС‰РёС…СЃСЏ СЏР·С‹РєРѕРІС‹С… Р»РѕРєР°Р»РёР·Р°С†РёР№ РґР»СЏ
        СѓСЃС‚Р°РЅРѕРІРєРё СЏР·С‹РєР° РїСЂРёР»РѕР¶РµРЅРёСЏ.'''

        def select_locale(name_locale):
            '''РЈСЃС‚Р°РЅР°РІР»РёРІР°РµС‚ РІС‹Р±СЂР°РЅРЅСѓСЋ Р»РѕРєР°Р»РёР·Р°С†РёСЋ.'''

            for locale in self.dict_language.keys():
                if name_locale == self.dict_language[locale]:
                    self.lang = locale
                    self.config.set('General', 'language', self.lang)
                    self.config.write()

        dict_info_locales = {}
        for locale in self.dict_language.keys():
            dict_info_locales[self.dict_language[locale]] = \
                ['locale', locale == self.lang]

        if not self.window_language:
            self.window_language = card(
                Lists(
                    dict_items=dict_info_locales,
                    events_callback=select_locale, flag='one_select_check'
                ),
                size=(.85, .55)
            )
        self.window_language.open()

    def dialog_exit(self):
        def check_interval_press(interval):
            self.exit_interval += interval
            if self.exit_interval > 5:
                self.exit_interval = False
                Clock.unschedule(check_interval_press)

        if self.exit_interval:
            sys.exit(0)
            
        Clock.schedule_interval(check_interval_press, 1)
        toast(self.translation._('Press Back to Exit'))
    def on_lang(self, instance, lang):
        self.translation.switch_lang(lang)
