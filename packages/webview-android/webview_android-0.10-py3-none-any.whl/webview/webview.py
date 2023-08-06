from android.runnable import run_on_ui_thread as run_thread
from jnius import autoclass


                                
@run_thread
def WebView(link,*args):  
    WebV = autoclass('android.webkit.WebView')   
    WebViewClient = autoclass('android.webkit.WebViewClient')
    activity = autoclass('org.renpy.android.PythonActivity').mActivity
             
    webview = WebV(activity)
    webview.getSettings().setJavaScriptEnabled(True) 
    wvc = WebViewClient()      
    webview.setWebViewClient(wvc)
    activity.setContentView(webview)
    webview.loadUrl(link)
    
    
       
