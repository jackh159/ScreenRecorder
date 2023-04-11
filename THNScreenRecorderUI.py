# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'THNScreenRecorderUI.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)
import files_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1400, 601)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1400, 200))
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        sizePolicy.setHeightForWidth(self.central_widget.sizePolicy().hasHeightForWidth())
        self.central_widget.setSizePolicy(sizePolicy)
        self.central_widget.setMinimumSize(QSize(1000, 200))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        self.central_widget.setFont(font)
        self.gridLayout = QGridLayout(self.central_widget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.w_edge_bottom_left = QWidget(self.central_widget)
        self.w_edge_bottom_left.setObjectName(u"w_edge_bottom_left")
        self.w_edge_bottom_left.setMinimumSize(QSize(0, 10))

        self.gridLayout.addWidget(self.w_edge_bottom_left, 3, 0, 1, 1)

        self.w_edge_bottom_right = QWidget(self.central_widget)
        self.w_edge_bottom_right.setObjectName(u"w_edge_bottom_right")
        self.w_edge_bottom_right.setMinimumSize(QSize(0, 10))

        self.gridLayout.addWidget(self.w_edge_bottom_right, 3, 2, 1, 1)

        self.w_edge_bottom = QWidget(self.central_widget)
        self.w_edge_bottom.setObjectName(u"w_edge_bottom")
        sizePolicy.setHeightForWidth(self.w_edge_bottom.sizePolicy().hasHeightForWidth())
        self.w_edge_bottom.setSizePolicy(sizePolicy)
        self.w_edge_bottom.setMinimumSize(QSize(800, 10))

        self.gridLayout.addWidget(self.w_edge_bottom, 3, 1, 1, 1)

        self.w_drag = QWidget(self.central_widget)
        self.w_drag.setObjectName(u"w_drag")
        self.w_drag.setMinimumSize(QSize(800, 200))
        self.gridLayout_2 = QGridLayout(self.w_drag)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.vertical_spacer_upper = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.vertical_spacer_upper, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.w_drag, 2, 1, 1, 1)

        self.w_edge_top_right = QWidget(self.central_widget)
        self.w_edge_top_right.setObjectName(u"w_edge_top_right")

        self.gridLayout.addWidget(self.w_edge_top_right, 0, 2, 1, 1)

        self.w_mask = QWidget(self.central_widget)
        self.w_mask.setObjectName(u"w_mask")
        sizePolicy.setHeightForWidth(self.w_mask.sizePolicy().hasHeightForWidth())
        self.w_mask.setSizePolicy(sizePolicy)
        self.w_mask.setMinimumSize(QSize(800, 60))
        self.w_mask.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setFamilies([u"Fjalla One"])
        font1.setPointSize(12)
        self.w_mask.setFont(font1)
        self.horizontalLayout = QHBoxLayout(self.w_mask)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, 4, 4, 4)
        self.btn_bg_toggle = QPushButton(self.w_mask)
        self.btn_bg_toggle.setObjectName(u"btn_bg_toggle")
        self.btn_bg_toggle.setMinimumSize(QSize(60, 50))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(12)
        self.btn_bg_toggle.setFont(font2)
        self.btn_bg_toggle.setStyleSheet(u"QPushButton {\n"
"	color: rgb(240, 240, 240);\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(47, 81, 101);\n"
"}\n"
"QPushButton:disabled {\n"
"	color: rgb(95, 95, 95);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(97, 179, 184);\n"
"	border: 2px solid rgb(47, 81, 101);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(47, 81, 101);\n"
"	border: 2px solid rgb(97, 179, 184);\n"
"}")
        icon = QIcon()
        icon.addFile(u":/48x48/icons/48x48/icons8-toggle-on-48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_bg_toggle.setIcon(icon)
        self.btn_bg_toggle.setIconSize(QSize(34, 34))

        self.horizontalLayout.addWidget(self.btn_bg_toggle)

        self.txtBox_clip_name = QLineEdit(self.w_mask)
        self.txtBox_clip_name.setObjectName(u"txtBox_clip_name")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.txtBox_clip_name.sizePolicy().hasHeightForWidth())
        self.txtBox_clip_name.setSizePolicy(sizePolicy1)
        self.txtBox_clip_name.setMinimumSize(QSize(200, 50))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(16)
        font3.setBold(False)
        font3.setItalic(False)
        self.txtBox_clip_name.setFont(font3)
        self.txtBox_clip_name.setAcceptDrops(True)
        self.txtBox_clip_name.setStyleSheet(u"QLineEdit {\n"
"	font: 63 16pt \"Segoe UI\";\n"
"	color: rgb(240, 240, 240);\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(47, 81, 101);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(47, 81, 101);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")
        self.txtBox_clip_name.setMaxLength(32)

        self.horizontalLayout.addWidget(self.txtBox_clip_name)

        self.ddl_project_list = QComboBox(self.w_mask)
        self.ddl_project_list.setObjectName(u"ddl_project_list")
        self.ddl_project_list.setMinimumSize(QSize(160, 50))
        self.ddl_project_list.setMaximumSize(QSize(160, 16777215))
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setPointSize(12)
        font4.setBold(True)
        self.ddl_project_list.setFont(font4)
        self.ddl_project_list.setStyleSheet(u"QComboBox{\n"
"	color: rgb(240, 240, 240);	\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(47, 81, 101);\n"
"\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:disabled{\n"
"	color: rgb(95, 95, 95);\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(47, 81, 101);\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"	background-color: rgb(47, 81, 101);\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	padding: 10px;\n"
"	color: rgb(220, 220, 220);\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"")
        self.ddl_project_list.setFrame(True)

        self.horizontalLayout.addWidget(self.ddl_project_list)

        self.btn_record = QPushButton(self.w_mask)
        self.btn_record.setObjectName(u"btn_record")
        sizePolicy1.setHeightForWidth(self.btn_record.sizePolicy().hasHeightForWidth())
        self.btn_record.setSizePolicy(sizePolicy1)
        self.btn_record.setMinimumSize(QSize(100, 50))
        self.btn_record.setMaximumSize(QSize(16777215, 16777215))
        font5 = QFont()
        font5.setFamilies([u"Segoe UI Semibold"])
        font5.setPointSize(12)
        font5.setBold(True)
        self.btn_record.setFont(font5)
        self.btn_record.setLayoutDirection(Qt.LeftToRight)
        self.btn_record.setStyleSheet(u"QPushButton {\n"
"	color: rgb(240, 240, 240);\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(47, 81, 101);\n"
"}\n"
"QPushButton:disabled {\n"
"	color: rgb(95, 95, 95);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(97, 179, 184);\n"
"	border: 2px solid rgb(47, 81, 101);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(47, 81, 101);\n"
"	border: 2px solid rgb(97, 179, 184);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/30x30/icons/30x30/icons8-record-30.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_record.setIcon(icon1)
        self.btn_record.setIconSize(QSize(50, 50))

        self.horizontalLayout.addWidget(self.btn_record)

        self.btn_pause = QPushButton(self.w_mask)
        self.btn_pause.setObjectName(u"btn_pause")
        self.btn_pause.setMinimumSize(QSize(120, 50))
        self.btn_pause.setFont(font4)
        self.btn_pause.setStyleSheet(u"QPushButton {\n"
"	color: rgb(240, 240, 240);\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(47, 81, 101);\n"
"}\n"
"QPushButton:disabled {\n"
"	color: rgb(95, 95, 95);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(97, 179, 184);\n"
"	border: 2px solid rgb(47, 81, 101);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(47, 81, 101);\n"
"	border: 2px solid rgb(97, 179, 184);\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/48x48/icons/48x48/icons8-pause-squared-48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_pause.setIcon(icon2)
        self.btn_pause.setIconSize(QSize(34, 34))

        self.horizontalLayout.addWidget(self.btn_pause)

        self.btn_cancel = QPushButton(self.w_mask)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setMinimumSize(QSize(100, 50))
        self.btn_cancel.setFont(font4)
        self.btn_cancel.setStyleSheet(u"QPushButton {\n"
"	color: rgb(240, 240, 240);\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(47, 81, 101);\n"
"}\n"
"QPushButton:disabled {\n"
"	color: rgb(95, 95, 95);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(97, 179, 184);\n"
"	border: 2px solid rgb(47, 81, 101);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(47, 81, 101);\n"
"	border: 2px solid rgb(97, 179, 184);\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/48x48/icons/48x48/icons8-stop-squared-48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_cancel.setIcon(icon3)
        self.btn_cancel.setIconSize(QSize(34, 34))

        self.horizontalLayout.addWidget(self.btn_cancel)

        self.btn_review_folder = QPushButton(self.w_mask)
        self.btn_review_folder.setObjectName(u"btn_review_folder")
        self.btn_review_folder.setMinimumSize(QSize(50, 50))
        self.btn_review_folder.setStyleSheet(u"QPushButton {\n"
"	color: rgb(240, 240, 240);\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(47, 81, 101);\n"
"}\n"
"QPushButton:disabled {\n"
"	color: rgb(95, 95, 95);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(97, 179, 184);\n"
"	border: 2px solid rgb(47, 81, 101);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(47, 81, 101);\n"
"	border: 2px solid rgb(97, 179, 184);\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u":/24x24/icons/24x24/icons8-opened-folder-24.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_review_folder.setIcon(icon4)
        self.btn_review_folder.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.btn_review_folder)

        self.btn_help = QPushButton(self.w_mask)
        self.btn_help.setObjectName(u"btn_help")
        self.btn_help.setMinimumSize(QSize(50, 50))
        self.btn_help.setMaximumSize(QSize(16777215, 16777215))
        self.btn_help.setFont(font)
        self.btn_help.setStyleSheet(u"QPushButton {\n"
"	color: rgb(240, 240, 240);\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(47, 81, 101);\n"
"}\n"
"QPushButton:disabled {\n"
"	color: rgb(95, 95, 95);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(97, 179, 184);\n"
"	border: 2px solid rgb(47, 81, 101);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(47, 81, 101);\n"
"	border: 2px solid rgb(97, 179, 184);\n"
"}")
        icon5 = QIcon()
        icon5.addFile(u":/24x24/icons/24x24/icons8-question-mark-24.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_help.setIcon(icon5)
        self.btn_help.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.btn_help)

        self.btn_exit = QPushButton(self.w_mask)
        self.btn_exit.setObjectName(u"btn_exit")
        self.btn_exit.setMinimumSize(QSize(50, 50))
        self.btn_exit.setMaximumSize(QSize(16777215, 16777215))
        self.btn_exit.setFont(font2)
        self.btn_exit.setStyleSheet(u"QPushButton {\n"
"	color: rgb(240, 240, 240);\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(47, 81, 101);\n"
"}\n"
"QPushButton:disabled {\n"
"	color: rgb(95, 95, 95);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(97, 179, 184);\n"
"	border: 2px solid rgb(47, 81, 101);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(47, 81, 101);\n"
"	border: 2px solid rgb(97, 179, 184);\n"
"}")
        icon6 = QIcon()
        icon6.addFile(u":/24x24/icons/24x24/icons8-close-24.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_exit.setIcon(icon6)
        self.btn_exit.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.btn_exit)


        self.gridLayout.addWidget(self.w_mask, 1, 1, 1, 1)

        self.w_edge_right = QWidget(self.central_widget)
        self.w_edge_right.setObjectName(u"w_edge_right")
        self.w_edge_right.setMinimumSize(QSize(10, 0))
        self.w_edge_right.setMaximumSize(QSize(10, 16777215))

        self.gridLayout.addWidget(self.w_edge_right, 1, 2, 2, 1)

        self.w_edge_left = QWidget(self.central_widget)
        self.w_edge_left.setObjectName(u"w_edge_left")
        self.w_edge_left.setMinimumSize(QSize(10, 0))
        self.w_edge_left.setMaximumSize(QSize(10, 16777215))

        self.gridLayout.addWidget(self.w_edge_left, 1, 0, 2, 1)

        self.w_edge_topLeft = QWidget(self.central_widget)
        self.w_edge_topLeft.setObjectName(u"w_edge_topLeft")
        self.w_edge_topLeft.setMinimumSize(QSize(10, 10))
        self.w_edge_topLeft.setMaximumSize(QSize(16777215, 10))

        self.gridLayout.addWidget(self.w_edge_topLeft, 0, 0, 1, 1)

        self.w_edge_top = QWidget(self.central_widget)
        self.w_edge_top.setObjectName(u"w_edge_top")
        sizePolicy.setHeightForWidth(self.w_edge_top.sizePolicy().hasHeightForWidth())
        self.w_edge_top.setSizePolicy(sizePolicy)
        self.w_edge_top.setMinimumSize(QSize(800, 10))
        self.w_edge_top.setMaximumSize(QSize(16777215, 10))

        self.gridLayout.addWidget(self.w_edge_top, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.central_widget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.btn_bg_toggle.setToolTip(QCoreApplication.translate("MainWindow", u"Toggle background visibility", None))
#endif // QT_CONFIG(tooltip)
        self.btn_bg_toggle.setText("")
#if QT_CONFIG(tooltip)
        self.btn_record.setToolTip(QCoreApplication.translate("MainWindow", u"Start recording", None))
#endif // QT_CONFIG(tooltip)
        self.btn_record.setText(QCoreApplication.translate("MainWindow", u"Record", None))
#if QT_CONFIG(tooltip)
        self.btn_pause.setToolTip(QCoreApplication.translate("MainWindow", u"Pause recording", None))
#endif // QT_CONFIG(tooltip)
        self.btn_pause.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
#if QT_CONFIG(tooltip)
        self.btn_cancel.setToolTip(QCoreApplication.translate("MainWindow", u"Cancel recording", None))
#endif // QT_CONFIG(tooltip)
        self.btn_cancel.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
#if QT_CONFIG(tooltip)
        self.btn_review_folder.setToolTip(QCoreApplication.translate("MainWindow", u"Open review folder", None))
#endif // QT_CONFIG(tooltip)
        self.btn_review_folder.setText("")
#if QT_CONFIG(tooltip)
        self.btn_help.setToolTip(QCoreApplication.translate("MainWindow", u"Help", None))
#endif // QT_CONFIG(tooltip)
        self.btn_help.setText("")
#if QT_CONFIG(tooltip)
        self.btn_exit.setToolTip(QCoreApplication.translate("MainWindow", u"Close window", None))
#endif // QT_CONFIG(tooltip)
        self.btn_exit.setText("")
    # retranslateUi

