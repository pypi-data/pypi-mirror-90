import gc
from io import StringIO
from typing import Optional

from PyQt5.QtCore import QSize, Qt, QCoreApplication
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QPushButton, QHBoxLayout

from bauh import __app_name__
from bauh.api.abstract.controller import SoftwareManager
from bauh.api.abstract.view import MessageType
from bauh.view.core.controller import GenericSoftwareManager
from bauh.view.qt import dialog
from bauh.view.qt.components import to_widget, new_spacer
from bauh.view.qt.dialog import ConfirmationDialog
from bauh.view.qt.qt_utils import centralize
from bauh.view.util import util
from bauh.view.util.translation import I18n


class SettingsWindow(QWidget):

    def __init__(self, manager: SoftwareManager, i18n: I18n, screen_size: QSize, window: QWidget, parent: Optional[QWidget] = None):
        super(SettingsWindow, self).__init__(parent=parent, flags=Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle('{} ({})'.format(i18n['settings'].capitalize(), __app_name__))
        self.setLayout(QVBoxLayout())
        self.manager = manager
        self.i18n = i18n
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.window = window

        self.settings_model = self.manager.get_settings(screen_size.width(), screen_size.height())

        tab_group = to_widget(self.settings_model, i18n)
        tab_group.setObjectName('settings')
        self.layout().addWidget(tab_group)

        lower_container = QWidget()
        lower_container.setObjectName('lower_container')
        lower_container.setProperty('container', 'true')
        lower_container.setLayout(QHBoxLayout())
        lower_container.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        bt_close = QPushButton()
        bt_close.setObjectName('cancel')
        bt_close.setAutoDefault(True)
        bt_close.setCursor(QCursor(Qt.PointingHandCursor))
        bt_close.setText(self.i18n['close'].capitalize())
        bt_close.clicked.connect(lambda: self.close())
        lower_container.layout().addWidget(bt_close)

        lower_container.layout().addWidget(new_spacer())

        bt_change = QPushButton()
        bt_change.setAutoDefault(True)
        bt_change.setObjectName('ok')
        bt_change.setCursor(QCursor(Qt.PointingHandCursor))
        bt_change.setText(self.i18n['change'].capitalize())
        bt_change.clicked.connect(self._save_settings)
        lower_container.layout().addWidget(bt_change)

        self.layout().addWidget(lower_container)

    def show(self):
        super(SettingsWindow, self).show()
        centralize(self)

    def closeEvent(self, event):
        if self.window and self.window.settings_window == self:
            self.deleteLater()
            self.window.settings_window = None
        elif not self.window:
            QCoreApplication.exit()

        gc.collect()

    def handle_display(self):
        if self.isMinimized():
            self.setWindowState(Qt.WindowNoState)
        elif self.isHidden():
            self.show()
        else:
            self.setWindowState(self.windowState() and Qt.WindowMinimized or Qt.WindowActive)

    def _save_settings(self):
        success, warnings = self.manager.save_settings(self.settings_model)

        if success:
            if not self.window:
                dialog.show_message(title=self.i18n['success'].capitalize(),
                                    body=self.i18n['settings.changed.success.warning'],
                                    type_=MessageType.INFO)
                QCoreApplication.exit()
            elif ConfirmationDialog(title=self.i18n['warning'].capitalize(),
                                    body="<p>{}</p><p>{}</p>".format(self.i18n['settings.changed.success.warning'],
                                                                     self.i18n['settings.changed.success.reboot']),
                                    i18n=self.i18n).ask():
                self.close()
                util.restart_app()
            else:
                if isinstance(self.manager, GenericSoftwareManager):
                    self.manager.reset_cache()

                self.manager.prepare(task_manager=None, root_password=None, internet_available=None)

                if self.window and self.window.isVisible():
                    self.window.update_custom_actions()
                    self.window.verify_warnings()
                    self.window.types_changed = True
                    self.window.begin_refresh_packages()
                self.close()
        else:
            msg = StringIO()
            msg.write("<p>{}</p>".format(self.i18n['settings.error']))

            for w in warnings:
                msg.write('<p style="font-weight: bold">* ' + w + '</p><br/>')

            msg.seek(0)
            dialog.show_message(title=self.i18n['warning'].capitalize(), body=msg.read(), type_=MessageType.WARNING)
