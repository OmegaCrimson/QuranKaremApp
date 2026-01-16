import threading
from flask import Flask, render_template, send_from_directory
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from jnius import autoclass, cast
from android.runnable import run_on_ui_thread
from android.permissions import request_permissions, Permission

# --- FLASK SETUP ---
app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

def run_server():
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)

# --- ANDROID WEBVIEW SETUP ---
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
Activity = autoclass('org.kivy.android.PythonActivity').mActivity
LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')

class AndroidWebView(Widget):
    def __init__(self, **kwargs):
        super(AndroidWebView, self).__init__(**kwargs)
        self.webview = None
        # We must keep a reference to any object passed to Java to prevent 
        # Python Garbage Collector from destroying it and crashing the app.
        self.bridge = None 
        Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args):
        # 1. Create the WebView
        self.webview = WebView(Activity)
        
        # 2. Configure Settings
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        
        # 3. Setup WebViewClient to handle page navigation within the WebView
        self.webview.setWebViewClient(WebViewClient())
        
        # 4. Add to Activity (This overlays it on top of Kivy)
        # Use match_parent to fill the screen
        params = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        Activity.addContentView(self.webview, params)
        
        # 5. Load the Flask URL
        self.webview.loadUrl("http://127.0.0.1:5000/")

    def on_pause(self):
        if self.webview:
            self.webview.onPause()
        return True

    def on_resume(self):
        if self.webview:
            self.webview.onResume()

class QuranApp(App):
    def build(self):
        # Request necessary permissions on startup
        request_permissions([
            Permission.INTERNET,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE
        ])
        
        # Start Flask in a background thread
        threading.Thread(target=run_server, daemon=True).start()
        
        # Return the widget that spawns the WebView
        return AndroidWebView()

if __name__ == '__main__':
    QuranApp().run()