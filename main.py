import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class LaunchPad(QMainWindow):
    link = 'http://www.google.com'
    def __init__(self):
        super().__init__()
        self.portal = QWebEngineView()
        self.portal.setUrl(QUrl(LaunchPad.link))
        self.setCentralWidget(self.portal)
        self.showMaximized()
        self.setWindowIcon(QIcon('infinityjpeg.png'))
        self.short_url = list()
        self.short_act = list()

        self.menu = self.menuBar()
        more = self.menu.addMenu('More')

        y = QAction('Youtube',self)
        y.triggered.connect(self.goto_youtube)
        self.menu.addAction(y)

        w = QAction('Wikipedia',self)
        w.triggered.connect(self.goto_wikipedia)
        self.menu.addAction(w)

        new_window = QAction('New Window',self)
        new_window.triggered.connect(self.open_new_window)
        more.addAction(new_window)

        set_home = QAction('Set as Homepage',self)
        set_home.triggered.connect(self.set_base)
        more.addAction(set_home)

        add_short = QAction('Add in Shortcuts',self)
        add_short.triggered.connect(self.short_add)
        more.addAction(add_short)

        rem_short = QAction('Remove from shortcuts',self)
        rem_short.triggered.connect(self.short_remove)
        more.addAction(rem_short)

        res = QAction('Reset',self)
        res.triggered.connect(self.reset_window)
        more.addAction(res)

        tools = QToolBar()
        self.addToolBar(tools)

        past = QAction('<-', self)
        past.setStatusTip("Go to previous page")
        past.triggered.connect(self.portal.back)
        tools.addAction(past)

        future = QAction('->', self)
        future.setStatusTip("Go to Next page")
        future.triggered.connect(self.portal.forward)
        tools.addAction(future)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.goto_url)
        tools.addWidget(self.url_bar)

        self.portal.urlChanged.connect(self.update_url)

        clear_btn = QAction('Clear',self)
        clear_btn.setStatusTip('Clear url bar text')
        clear_btn.triggered.connect(self.clear_url)
        tools.addAction(clear_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.setStatusTip('Reload page')
        reload_btn.triggered.connect(self.portal.reload)
        tools.addAction(reload_btn)

        base_btn = QAction('Home', self)
        base_btn.setStatusTip("Go to home page")
        base_btn.triggered.connect(self.goto_base)
        tools.addAction(base_btn)

    def open_new_window(self):
        self.w = LaunchPad()
        self.showMinimized()

    def set_base(self):
        if LaunchPad.link != self.url_bar.text():
            LaunchPad.link = self.url_bar.text()

    def goto_youtube(self):
        self.portal.setUrl(QUrl('https://www.youtube.com'))
        self.url_bar.setText('https://www.youtube.com')

    def goto_wikipedia(self):
        self.portal.setUrl(QUrl('https://www.wikipedia.org'))
        self.url_bar.setText('https://www.wikipedia.org')

    def short_add(self):
        if self.url_bar.text() not in self.short_url[:]:
            self.short_url.append(self.url_bar.text())
            t = self.url_bar.text().split('//')
            u = self.url_bar.text()
            s = QAction(t[1],self)
            s.triggered.connect(lambda:self.set_url(u))
            self.menu.addAction(s)
            self.short_act.append(s)

    def set_url(self,q):
        self.portal.setUrl(QUrl(q))

    def short_remove(self):
        if self.url_bar.text() in self.short_url:
            act = self.menu.actions()[self.short_url.index(self.url_bar.text())+3]
            self.menu.removeAction(act)
            w = self.short_act[self.short_url.index(self.url_bar.text())]
            self.short_act.remove(w)
            self.short_url.remove(self.url_bar.text())

    def reset_window(self):
        for i in self.menu.actions()[3:]:
            self.menu.removeAction(i)
        LaunchPad.link = 'http://www.google.com'

    def clear_url(self):
        self.url_bar.clear()

    def goto_base(self):
        self.portal.setUrl(QUrl(self.link))

    def goto_url(self):
        if 'https://' not in self.url_bar.text():
            url = 'https://' + self.url_bar.text()
        else:
            url = self.url_bar.text()
        self.portal.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())


if __name__=="__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Infinity Browser")
    base = LaunchPad()
    sys.exit(app.exec())