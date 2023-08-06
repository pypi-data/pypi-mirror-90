import sys
import os
import random
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


# 修复Qt环境
def analyse_code(contents: str) -> tuple:
    """
    Return list of lines, pyside2 path line number, indentation.

        :param str contents: code in __init__.py
    """
    lines = contents.splitlines(keepends=True)
    # locate pyside_package_dir line index
    pkg_dir = 'os.path.abspath(os.path.dirname(__file__))'
    for index, line in enumerate(lines):
        if pkg_dir in line:
            break

    # return lines, line index, indentation
    return lines, index, ' ' * (len(line.rstrip()) - len(line.strip()))


def insert_lines(contents: str) -> list:
    """
    Insert lines adding platforms plugin to PATH,
    return replaced list of lines of code.

        :param str contents: code in __init__.py
        :return: replaced list of lines of code
    """
    lines, position, indentation = analyse_code(contents)
    new_lines = (
            lines[position] + '\n' +
            indentation + '# add platforms plugin to PATH\n' +
            indentation + 'platforms_dir = ' +
            'os.path.join(pyside_package_dir, "plugins", "platforms")\n' +
            indentation +
            'os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = platforms_dir\n')

    # insert lines
    lines[position] = new_lines
    return lines


def add_plugins_to_PATH(file_path):
    """
    Add platforms plugin to PATH to avoid load error.

        :param str file_path: __init__.py path in PySide2 toplevel package
    """
    # open __init__.py
    with open(file_path, encoding='utf-8') as f:
        contents = f.read()

    # insert lines
    lines = insert_lines(contents)

    # save changes to __init__.py
    code = ''.join(lines)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)


def start_fix():
    """Glitch fixing entry."""
    import PySide2
    pyside2_init_module = PySide2.__file__
    add_plugins_to_PATH(pyside2_init_module)


start_fix()


class Ui_Cards(object):
    def setupUi(self, Cards):
        if not Cards.objectName():
            Cards.setObjectName(u"Cards")
        Cards.resize(800, 600)
        self.centralwidget = QWidget(Cards)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 110, 771, 481))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pbtn05 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img = QButtonGroup(Cards)
        self.pbtn_img.setObjectName(u"pbtn_img")
        self.pbtn_img.addButton(self.pbtn05)
        self.pbtn05.setObjectName(u"pbtn05")

        self.gridLayout.addWidget(self.pbtn05, 1, 0, 1, 1)

        self.pbtn02 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn02)
        self.pbtn02.setObjectName(u"pbtn02")

        self.gridLayout.addWidget(self.pbtn02, 0, 1, 1, 1)

        self.pbtn06 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn06)
        self.pbtn06.setObjectName(u"pbtn06")

        self.gridLayout.addWidget(self.pbtn06, 1, 1, 1, 1)

        self.pbtn07 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn07)
        self.pbtn07.setObjectName(u"pbtn07")

        self.gridLayout.addWidget(self.pbtn07, 1, 2, 1, 1)

        self.pbtn01 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn01)
        self.pbtn01.setObjectName(u"pbtn01")

        self.gridLayout.addWidget(self.pbtn01, 0, 0, 1, 1)

        self.pbtn04 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn04)
        self.pbtn04.setObjectName(u"pbtn04")

        self.gridLayout.addWidget(self.pbtn04, 0, 3, 1, 1)

        self.pbtn08 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn08)
        self.pbtn08.setObjectName(u"pbtn08")

        self.gridLayout.addWidget(self.pbtn08, 1, 3, 1, 1)

        self.pbtn03 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn03)
        self.pbtn03.setObjectName(u"pbtn03")

        self.gridLayout.addWidget(self.pbtn03, 0, 2, 1, 1)

        self.pbtn09 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn09)
        self.pbtn09.setObjectName(u"pbtn09")

        self.gridLayout.addWidget(self.pbtn09, 2, 0, 1, 1)

        self.pbtn10 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn10)
        self.pbtn10.setObjectName(u"pbtn10")

        self.gridLayout.addWidget(self.pbtn10, 2, 1, 1, 1)

        self.pbtn11 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn11)
        self.pbtn11.setObjectName(u"pbtn11")

        self.gridLayout.addWidget(self.pbtn11, 2, 2, 1, 1)

        self.pbtn12 = QPushButton(self.gridLayoutWidget)
        self.pbtn_img.addButton(self.pbtn12)
        self.pbtn12.setObjectName(u"pbtn12")

        self.gridLayout.addWidget(self.pbtn12, 2, 3, 1, 1)

        self.lcd_time = QLCDNumber(self.centralwidget)
        self.lcd_time.setObjectName(u"lcd_time")
        self.lcd_time.setGeometry(QRect(290, 10, 221, 91))
        Cards.setCentralWidget(self.centralwidget)

        self.retranslateUi(Cards)

        QMetaObject.connectSlotsByName(Cards)

    # setupUi

    def retranslateUi(self, Cards):
        Cards.setWindowTitle(QCoreApplication.translate("Cards", u"\u8bb0\u5fc6\u7ffb\u724c", None))
        self.pbtn05.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn02.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn06.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn07.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn01.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn04.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn08.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn03.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn09.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn10.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn11.setText(QCoreApplication.translate("Cards", u"PushButton", None))
        self.pbtn12.setText(QCoreApplication.translate("Cards", u"PushButton", None))
    # retranslateUi


class Cards(QMainWindow, Ui_Cards):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_button()
        self.init_img()
        self.show()
        self.clicked_num = 0
        self.match_img = {
            1: {
                "pbtn": None,
                "pbtn_img": None
            },
            2: {
                "pbtn": None,
                "pbtn_img": None
            },
        }
        self.first_clicked = True
        self.time = 0
        self.right_count = 0
        self.pbtn_img.buttonClicked.connect(self.pbtn_func)

    def init_button(self):
        pbtn_list = self.pbtn_img.buttons()
        for btn in pbtn_list:
            btn.setText("")
            btn.setIcon(QIcon("images_cards/bg.png"))
            btn.setIconSize(QSize(150, 150))
            btn.setCheckable(True)

    def init_img(self):
        image_type = ['.png', '.jpg', '.bmp', '.jpeg']
        files = os.listdir("images_cards")
        all_imgs = []
        for file in files:
            ext = os.path.splitext(file)[-1]
            if ext in image_type:
                all_imgs.append("images_cards" + os.sep + file)

        random_imgs = random.sample(all_imgs, 6)
        grid_imgs = random_imgs + random_imgs
        random.shuffle(grid_imgs)
        pbtn_list = self.pbtn_img.buttons()
        self.grids = dict(zip(pbtn_list, grid_imgs))

    def pbtn_func(self):
        if self.first_clicked:
            self.first_clicked = False
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_time)
            self.timer.start(1000)

        if self.clicked_num < 2:
            QApplication.processEvents()
            pbtn = self.pbtn_img.checkedButton()
            if pbtn != self.match_img[1]["pbtn"] and pbtn in self.pbtn_img.buttons():
                self.clicked_num += 1
                pbtn.setIcon(QIcon(self.grids[pbtn]))
                self.match_img[self.clicked_num]["pbtn"] = pbtn
                self.match_img[self.clicked_num]["pbtn_img"] = self.grids[pbtn]
                timer = QTimer()
                timer.singleShot(300, self.judge)

    def judge(self):
        if self.clicked_num == 2:
            self.clicked_num = 0
            if self.match_img[1]["pbtn_img"] != self.match_img[2]["pbtn_img"]:
                self.match_img[1]["pbtn"].setIcon(QIcon("images_cards/bg.png"))
                self.match_img[2]["pbtn"].setIcon(QIcon("images)cards/bg.png"))
            else:
                self.pbtn_img.removeButton(self.match_img[1]["pbtn"])
                self.pbtn_img.removeButton(self.match_img[2]["pbtn"])
                self.right_count += 1
                if self.right_count == 6:
                    self.timer.stop()
            self.match_img[1]["pbtn"] = self.match_img[2]["pbtn"] = None

    def update_time(self):
        self.time += 1
        self.lcd_time.display(self.time)


def main():
    app = QApplication(sys.argv)
    window = Cards()
    sys.exit(app.exec_())

# main()
