import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QComboBox, QAction, QStyleFactory, QCheckBox, QToolBar, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sunny Web - Der Browser Ihres Vertrauens")
        self.setWindowIcon(QIcon("logo.png"))
        self.setStyleSheet("background-color: #f0f0f0;")
        
        self.webview = QWebEngineView()
        self.setCentralWidget(self.webview)
        
        toolbar = self.addToolBar("Navigation")
        toolbar.setStyleSheet("background-color: #d1d1d1;")
        self.toolbar = toolbar  # Speichern der Referenz zum späteren Zugriff
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("URL eingeben")
        self.url_input.setStyleSheet("background-color: white;")
        toolbar.addWidget(self.url_input)
        
        self.go_button = QPushButton("Go")
        self.go_button.setStyleSheet("background-color: #4CAF50; color: white;")
        toolbar.addWidget(self.go_button)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Suche")
        self.search_input.setStyleSheet("background-color: white;")
        toolbar.addWidget(self.search_input)
        
        self.search_button = QPushButton("Suchen")
        self.search_button.setStyleSheet("background-color: #4CAF50; color: white;")
        toolbar.addWidget(self.search_button)
        
        self.language_combo = QComboBox()
        self.language_combo.addItem("Deutsch")
        self.language_combo.addItem("Englisch")
        self.language_combo.setStyleSheet("background-color: white;")
        toolbar.addWidget(self.language_combo)
        
        self.reload_action = QAction(QIcon("reload.png"), "Neu laden", self)
        self.reload_action.triggered.connect(self.webview.reload)
        toolbar.addAction(self.reload_action)

        self.back_action = QAction(QIcon("back.png"), "Zurück", self)
        self.back_action.triggered.connect(self.webview.back)
        toolbar.addAction(self.back_action)
        
        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)
        toolbar.addWidget(self.dark_mode_checkbox)
        
        self.go_button.clicked.connect(self.load_url)
        self.search_button.clicked.connect(self.start_search)
        
        self.search_input.returnPressed.connect(self.start_search)
        self.search_input.setVisible(False)
        self.search_button.setVisible(False)
        
        self.webview.urlChanged.connect(self.update_url_input)
        self.webview.loadStarted.connect(self.on_load_started)
        self.webview.loadFinished.connect(self.on_load_finished)
        
        self.load_custom_homepage()

    def load_url(self):
        url = self.url_input.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.webview.setUrl(QUrl(url))  # Verzögertes Laden der URL
        
    def start_search(self):
        query = self.search_input.text()
        if query:
            url = f"https://www.ecosia.org/search?q={query}"
            self.webview.setUrl(QUrl(url))  # Verzögertes Laden der Suchergebnisse
        
        self.url_input.setPlaceholderText("URL eingeben")
    
    def update_url_input(self, url):
        if not self.webview.url().isEmpty() and url != self.webview.url().toString():
            self.url_input.setText(url.toString())
    
    def toggle_dark_mode(self, state):
        if state == Qt.Checked:
            self.setStyleSheet("background-color: #202020; color: #ffffff;")
            self.toolbar.setStyleSheet("background-color: #404040;")
            self.webview.setStyleSheet("background-color: #202020; color: #ffffff;")
            self.url_input.setStyleSheet("background-color: #404040; color: #ffffff;")
            self.go_button.setStyleSheet("background-color: #4CAF50; color: white;")
            self.search_input.setStyleSheet("background-color: #404040; color: #ffffff;")
            self.search_button.setStyleSheet("background-color: #4CAF50; color: white;")
            self.language_combo.setStyleSheet("background-color: #404040; color: #ffffff;")
        else:
            self.setStyleSheet("background-color: #f0f0f0; color: #000000;")
            self.toolbar.setStyleSheet("background-color: #d1d1d1;")
            self.webview.setStyleSheet("background-color: #f0f0f0; color: #000000;")
            self.url_input.setStyleSheet("background-color: white; color: #000000;")
            self.go_button.setStyleSheet("background-color: #4CAF50; color: white;")
            self.search_input.setStyleSheet("background-color: white; color: #000000;")
            self.search_button.setStyleSheet("background-color: #4CAF50; color: white;")
            self.language_combo.setStyleSheet("background-color: white; color: #000000;")
    
    def on_load_started(self):
        self.go_button.setEnabled(False)
    
    def on_load_finished(self, ok):
        self.go_button.setEnabled(True)
        if not ok:
            QMessageBox.warning(self, "Warnung", "Die Seite ist unsicher! Bitte fahren Sie fort auf eigene Gefahr.")
    
    def load_custom_homepage(self):
        # Laden der benutzerdefinierten Startseite
        html_content = """
        <html>
            <head>
                <title>Willkommen bei Sunny Web</title>
                <style>
                    @keyframes fade-in {
                        0% { opacity: 0; }
                        100% { opacity: 1; }
                    }
                    .logo {
                        animation: fade-in 2s;
                    }
                </style>
            </head>
            <body style="font-family: Arial, sans-serif; text-align: center;">
                <h1>Willkommen bei Sunny Web</h1>
                <img src="logo.png" class="logo">
                <p>Bitte geben Sie eine URL ein oder verwenden Sie die Suchfunktion.</p>
            </body>
        </html>
        """
        self.webview.setHtml(html_content)

        # Leeren der URL-Leiste
        self.url_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())
