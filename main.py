import threading
import os
from flask import Flask, render_template, send_from_directory
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from jnius import autoclass, PythonJavaClass, java_method
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

# --- ANDROID WEBVIEW & JS INTERFACE ---
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
Activity = autoclass('org.kivy.android.PythonActivity').mActivity
LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')

# Logic bridge between Python and Javascript
class PythonBridge(PythonJavaClass):
    __javainterfaces__ = ['android/webkit/JavascriptInterface']
    __javacontext__ = 'app'

    def __init__(self):
        super().__init__()

    @java_method('(I)Z')
    def is_downloaded(self, surah_id):
        # Logic to check if file exists (Stub)
        # file_path = f"/storage/emulated/0/Download/Surah_{surah_id}.mp3"
        # return os.path.exists(file_path)
        return False

    @java_method('(Ljava/lang/String;I)Ljava/lang/String;')
    def download_audio(self, url, surah_id):
        # Logic to download file (Stub)
        # In a real app, use requests to download 'url' to storage
        print(f"Downloading {url} for surah {surah_id}")
        return "success" 
        # return "error"

    @java_method('(I)Ljava/lang/String;')
    def get_local_path(self, surah_id):
        return f"/storage/emulated/0/Download/Surah_{surah_id}.mp3"

class AndroidWebView(Widget):
    def __init__(self, **kwargs):
        super(AndroidWebView, self).__init__(**kwargs)
        self.webview = None
        self.create_webview()

    @run_on_ui_thread
    def create_webview(self):
        self.webview = WebView(Activity)
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        
        # Attach the Python bridge to 'window.python' in JS
        self.webview.addJavascriptInterface(PythonBridge(), "python")
        
        self.webview.setWebViewClient(WebViewClient())
        
        # Use addContentView instead of setContentView to prevent Kivy crash
        Activity.addContentView(self.webview, LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT))
        
        self.webview.loadUrl("http://127.0.0.1:5000/")

    # Handle back button to go back in browser history
    def on_back_pressed(self):
        if self.webview and self.webview.canGoBack():
            self.webview.goBack()
            return True
        return False

class QuranApp(App):
    def build(self):
        # Request Permissions at startup
        request_permissions([
            Permission.INTERNET, 
            Permission.READ_EXTERNAL_STORAGE, 
            Permission.WRITE_EXTERNAL_STORAGE
        ])
        
        # Start Flask
        threading.Thread(target=run_server, daemon=True).start()
        
        self.webview_widget = AndroidWebView()
        return self.webview_widget

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    QuranApp().run()
