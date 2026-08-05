import os
import sys

# בדיקת פלטפורמה - היבואים של Kivy ו-Android מבוצעים רק בסביבת אנדרואיד
try:
    from kivy.utils import platform # type: ignore
    IS_ANDROID = (platform == 'android')
except ImportError:
    IS_ANDROID = False

if IS_ANDROID:
    from kivy.app import App                   # type: ignore
    from kivy.clock import Clock               # type: ignore
    from kivy.core.window import Window        # type: ignore
    from kivy.uix.boxlayout import BoxLayout   # type: ignore

    Window.clearcolor = (0.1, 0.1, 0.1, 1)

base_dir = os.path.dirname(os.path.abspath(__file__))


if IS_ANDROID:
    class PhoneMainApp(App):
        def build(self):
            self.root_layout = BoxLayout(orientation='vertical')
            Clock.schedule_once(self._init_android_webview, 0.5)
            return self.root_layout

        def _init_android_webview(self, dt):
            try:
                from jnius import autoclass, PythonJavaClass, java_method  # type: ignore
                from android.runnable import run_on_ui_thread              # type: ignore

                Activity = autoclass('org.kivy.android.PythonActivity').mActivity
                WebView = autoclass('android.webkit.WebView')
                WebViewClient = autoclass('android.webkit.WebViewClient')

                app_self = self

                class JSBridge(PythonJavaClass):
                    __javainterfaces__ = ['java/lang/Object']
                    __javacontext__ = 'app'

                    def __init__(self):
                        super().__init__()

                    @java_method('(Ljava/lang/String;)V')
                    def page_go(self, page_path):
                        """
                        מעבר בין קבצי HTML באנדרואיד בלבד.
                        קריאה מ-JS: window.Android.page_go('Extratag_Vcall/index.html')
                        """
                        full_path = os.path.join(base_dir, page_path)
                        print(f"[Android JSBridge] Navigating to: {full_path}")

                        @run_on_ui_thread
                        def navigate():
                            if os.path.exists(full_path):
                                app_self.webview.loadUrl(f"file://{full_path}")
                            else:
                                print(f"[ERROR] Page not found: {full_path}")

                        navigate()

                @run_on_ui_thread
                def create_webview():
                    self.webview = WebView(Activity)
                    settings = self.webview.getSettings()
                    
                    settings.setJavaScriptEnabled(True)
                    settings.setDomStorageEnabled(True)
                    settings.setAllowFileAccessFromFileURLs(True)
                    settings.setAllowUniversalAccessFromFileURLs(True)
                    
                    bridge = JSBridge()
                    self.webview.addJavascriptInterface(bridge, "Android")
                    self.webview.setWebViewClient(WebViewClient())
                    
                    initial_page = os.path.join(base_dir, "Extratag_Email", "index.html")
                    if os.path.exists(initial_page):
                        self.webview.loadUrl(f"file://{initial_page}")

                    Activity.setContentView(self.webview)

                create_webview()

            except Exception as e:
                print(f"[ERROR] Failed to set Android WebView: {e}")

    if __name__ == '__main__':
        PhoneMainApp().run()
else:
    if __name__ == '__main__':
        print("[INFO] phone_main.py is configured strictly for Android environment execution.")
        print("[INFO] Build project with Buildozer / GitHub Actions workflow to run on target device.")