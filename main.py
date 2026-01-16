import os
import requests
from kivy.app import App
from kivy.utils import platform
from jnius import autoclass
from android.runnable import run_on_ui_thread

# استدعاء كلاسات أندرويد للتحكم في الـ WebView
PythonActivity = autoclass('org.kivy.android.PythonActivity')
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
WebChromeClient = autoclass('android.webkit.WebChromeClient')

class PythonBridge:
    """هذا الكلاس يسمح لـ JavaScript باستدعاء دوال البايثون"""
    def __init__(self):
        if platform == 'android':
            from android.storage import app_storage_path
            self.storage_dir = os.path.join(app_storage_path(), "audio")
        else:
            self.storage_dir = "audio"
            
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def is_downloaded(self, surah_id):
        filepath = os.path.join(self.storage_dir, f"{surah_id}.mp3")
        return os.path.exists(filepath)

    def download_audio(self, url, surah_id):
        try:
            filepath = os.path.join(self.storage_dir, f"{surah_id}.mp3")
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)
                return f"file://{filepath}"
            return "error"
        except Exception as e:
            return str(e)

    def get_local_path(self, surah_id):
        filepath = os.path.join(self.storage_dir, f"{surah_id}.mp3")
        return f"file://{filepath}"

class QuranApp(App):
    @run_on_ui_thread
    def build_webview(self):
        webview = WebView(PythonActivity.mActivity)
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setAllowContentAccess(True)
        
        # ربط الجسر باسم 'python' لاستخدامه في JS
        self.bridge = PythonBridge()
        webview.addJavascriptInterface(self.bridge, "python")
        
        webview.setWebViewClient(WebViewClient())
        webview.setWebChromeClient(WebChromeClient())
        PythonActivity.mActivity.setContentView(webview)
        webview.loadUrl('file:///android_asset/index.html')

    def build(self):
        self.build_webview()
        return None

if __name__ == '__main__':
    QuranApp().run()