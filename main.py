import threading
from flask import Flask, render_template, send_from_directory
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import os

# --- FLASK SETUP ---
app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

def run_server():
    # Run flask on localhost
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)

# --- KIVY WEBVIEW SETUP ---
# Standard Kivy doesn't have WebView. We use the Android native one via jnius.
from jnius import autoclass
from kivy.uix.widget import Widget
from android.runnable import run_on_ui_thread

WebViewAndroid = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
Activity = autoclass('org.kivy.android.PythonActivity').mActivity

class AndroidWebView(Widget):
    def __init__(self, **kwargs):
        super(AndroidWebView, self).__init__(**kwargs)
        self.generate_webview()

    @run_on_ui_thread
    def generate_webview(self):
        webview = WebViewAndroid(Activity)
        webview.getSettings().setJavaScriptEnabled(True)
        webview.setWebViewClient(WebViewClient())
        webview.loadUrl("http://127.0.0.1:5000/")
        Activity.setContentView(webview)

class QuranApp(App):
    def build(self):
        # Start Flask in a background thread
        threading.Thread(target=run_server, daemon=True).start()
        
        # Return the WebView widget
        return AndroidWebView()

if __name__ == '__main__':
    QuranApp().run()