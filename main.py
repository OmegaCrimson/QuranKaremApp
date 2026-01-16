# main.py
from kivy.app import App
from jnius import autoclass
from android.runnable import run_on_ui_thread

# Android classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = PythonActivity.mActivity

@run_on_ui_thread
def show_local_html():
    webview = WebView(activity)
    settings = webview.getSettings()
    settings.setJavaScriptEnabled(True)
    webview.setWebViewClient(WebViewClient())
    activity.setContentView(webview)
    # Load bundled asset
    webview.loadUrl('file:///android_asset/index.html')

class LocalHtmlApp(App):
    def build(self):
        # Show the local HTML immediately
        show_local_html()
        # Kivy expects a widget return; returning None is acceptable here
        return

if __name__ == '__main__':
    LocalHtmlApp().run()
