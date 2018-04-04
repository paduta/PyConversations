# This file created with KivyCreatorProject
# <https://github.com/HeaTTheatR/KivyCreatorProgect
#
# Copyright В© 2017 Easy
#
# For suggestions and questions:
# <kivydevelopment@gmail.com>
# 
# LICENSE: MIT

# РўРѕС‡РєР° РІС…РѕРґР° РІ РїСЂРёР»РѕР¶РµРЅРёРµ. Р—Р°РїСѓСЃРєР°РµС‚ РѕСЃРЅРѕРІРЅРѕР№ РїСЂРѕРіСЂР°РјРјРЅС‹Р№ РєРѕРґ program.py.
# Р’ СЃР»СѓС‡Р°Рµ РѕС€РёР±РєРё, РІС‹РІРѕРґРёС‚ РЅР° СЌРєСЂР°РЅ РѕРєРЅРѕ СЃ РµС‘ С‚РµРєСЃС‚РѕРј.

import os
import sys
import traceback

# РќРёРєРЅРµР№Рј Рё РёРјСЏ СЂРµРїРѕР·РёС‚РѕСЂРёСЏ РЅР° github,
# РєСѓРґР° Р±СѓРґРµС‚ РѕС‚РїСЂР°РІР»РµРЅ РѕС‚С‡С‘С‚ Р±Р°Рі СЂРµРїРѕСЂС‚Р°.
NICK_NAME_AND_NAME_REPOSITORY = 'https://github.com/User/PyConversations'

directory = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.join(directory, 'libs/applibs'))

try:
    import webbrowser
    try:
        import six.moves.urllib
    except ImportError:
        pass

    import kivy
    kivy.require('1.9.2')

    from kivy.config import Config
    Config.set('kivy', 'keyboard_mode', 'system')
    Config.set('kivy', 'log_enable', 0)

    from kivy import platform
    if platform == 'android':
        from plyer import orientation
        orientation.set_sensor(mode='any')

    from kivymd.theming import ThemeManager
    # Activity Р±Р°Рі СЂРµРїРѕСЂС‚Р°.
    from bugreporter import BugReporter
except Exception:
    traceback.print_exc(file=open(os.path.join(directory, 'error.log'), 'w'))
    sys.exit(1)


__version__ = '1.0'


def main():
    def create_error_monitor():
        class _App(App):
            theme_cls = ThemeManager()
            theme_cls.primary_palette = 'BlueGrey'

            def build(self):
                box = BoxLayout()
                box.add_widget(report)
                return box
        app = _App()
        app.run()

    app = None

    try:
        from loadplugin import load_plugin # С„СѓРЅРєС†РёСЏ Р·Р°РіСЂСѓР·РєРё РїР»Р°РіРёРЅРѕРІ
        from pyconversations import PyConversations  # РѕСЃРЅРѕРІРЅРѕР№ РєР»Р°СЃСЃ РїСЂРѕРіСЂР°РјРјС‹

        # Р—Р°РїСѓСЃРє РїСЂРёР»РѕР¶РµРЅРёСЏ.
        app = PyConversations()
        load_plugin(app, __version__)
        app.run()
    except Exception:
        from kivy.app import App
        from kivy.uix.boxlayout import BoxLayout


        text_error = traceback.format_exc()
        traceback.print_exc(file=open(os.path.join(directory, 'error.log'), 'w'))

        if app:
            try:
                app.stop()
            except AttributeError:
                app = None

        def callback_report(*args):
            '''Р¤СѓРЅРєС†РёСЏ РѕС‚РїСЂР°РІРєРё Р±Р°Рі-СЂРµРїРѕСЂС‚Р°.'''

            try:
                txt = six.moves.urllib.parse.quote(
                    report.txt_traceback.text.encode('utf-8')
                )
                url = f'https://github.com/{NICK_NAME_AND_NAME_REPOSITORY}/issues/new?body=' + txt
                webbrowser.open(url)
            except Exception:
                sys.exit(1)

        report = BugReporter(
            callback_report=callback_report, txt_report=text_error,
            icon_background=os.path.join('data', 'images', 'icon.png')
        )

        if app:
            try:
                app.screen.clear_widgets()
                app.screen.add_widget(report)
            except AttributeError:
            	create_error_monitor()
        else:
            create_error_monitor()


if __name__ in ('__main__', '__android__'):
    main()
