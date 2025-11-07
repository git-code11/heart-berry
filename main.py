from kivy.config import Config
Config.set("graphics", "width", 480)
Config.set("graphics", "height", 360)
Config.set('graphics', 'resizable', 0)
Config.set("graphics", "fullscreen", 0)
# Config.set("graphics", "left", 500)
# Config.set("graphics", "top", 0)


if __name__ == '__main__':
    from app import HeartApp
    HeartApp().run()
