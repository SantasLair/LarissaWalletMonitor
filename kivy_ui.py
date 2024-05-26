import kivy
from kivy.app import App
from kivy.uix.label import Label


class WalletMonitorApp(App):
    def build(self):
        return Label(text='Hell, Wallets!')
