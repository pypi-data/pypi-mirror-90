# webview

Create WebViews for android with this little python module (still in development).

To create a webview with python for android you need to use kivy / kivymd 
or pydroid3, you can create a webview app with kivy like this:

## Examples:
```
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from webview import WebView
from kivy.lang.builder import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen

Builder.load_string("""
<MyWebView>
    MDFlatButton:
        text: "Push"
        pos_hint: {"center_x": .5, "center_y": .4}
        on_press: root.Push()
""")

class MyWebView(MDScreen):
    def Push(self):
        WebView("https://www.google.com")
     

class MyWebApp(MDApp):
    def build(self):
        return MyWebView()


if __name__ == '__main__':
    MyWebApp().run()
    
```

This example can be used in Pydroid3 and in a kivy / kivymd app


## installation:
```
pip3 install webview-android
```

