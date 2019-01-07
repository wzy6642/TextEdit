import platform
import os
import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *
# 以下模块可以模拟键盘以及鼠标操作
import pymouse, pykeyboard
from pymouse import *
from pykeyboard import *
import webbrowser
from PyQt5 import QtCore, QtGui, QtWidgets

# 搜索对话框
class FindDialog(QDialog):
    def __init__(self, parent=None):
        super(FindDialog, self).__init__(parent)
        self.setWindowTitle('查找')
        self.setWindowIcon(QIcon('./image/Find.ico'))
        # 应用程序模态，阻止和任何其他窗口进行交互
        self.setWindowModality(Qt.ApplicationModal)
        # 禁止最大化按钮
        #self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.resize(500, 173)
        # 禁止拉伸窗口大小
        self.setFixedSize(self.width(), self.height())
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 451, 141))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 2, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy)
        self.checkBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 3, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 2, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.groupBox.setObjectName("groupBox")
        self.QRadioButton_1 = QtWidgets.QRadioButton(self.groupBox)
        self.QRadioButton_1.setGeometry(QtCore.QRect(10, 40, 71, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.QRadioButton_1.sizePolicy().hasHeightForWidth())
        self.QRadioButton_1.setSizePolicy(sizePolicy)
        self.QRadioButton_1.setObjectName("QRadioButton_1")
        self.QRadioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.QRadioButton_2.setGeometry(QtCore.QRect(120, 40, 71, 22))
        self.QRadioButton_2.setObjectName("QRadioButton_2")
        # 默认为选中状态
        self.QRadioButton_2.setChecked(True)
        self.gridLayout.addWidget(self.groupBox, 3, 1, 1, 1)
        self.label.setBuddy(self.lineEdit)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Form", "查找内容(&N):"))
        self.pushButton_2.setText(_translate("Form", "查找下一个(&F)"))
        self.pushButton_2.setShortcut(_translate("Form", "Alt+F"))
        self.checkBox.setText(_translate("Form", "区分大小写(&C)"))
        self.checkBox.setShortcut(_translate("Form", "Alt+C"))
        self.pushButton.setText(_translate("Form", "取消"))
        self.groupBox.setTitle(_translate("Form", "方向"))
        self.QRadioButton_1.setText(_translate("Form", "向上(&U)"))
        self.QRadioButton_1.setShortcut(_translate("Form", "Alt+U"))
        self.QRadioButton_2.setText(_translate("Form", "向下(&D)"))
        self.QRadioButton_2.setShortcut(_translate("Form", "Alt+D"))
                    
# 弹出日历对话框类
class DateDialog(QDialog):
    # 自定义信号
    Signal_OneParameter = pyqtSignal(str)

    def __init__(self, parent=None):
        super(DateDialog, self).__init__(parent)
        self.setWindowTitle('calender')
        self.setWindowIcon(QIcon('./image/calendar.ico'))
        # 应用程序模态，阻止和任何其他窗口进行交互
        self.setWindowModality(Qt.ApplicationModal)
        # 在垂直布局中添加部件
        layout = QVBoxLayout(self)

        self.datetime_inner = QDateTimeEdit(self)
        # 日历采用可以弹出式的
        self.datetime_inner.setCalendarPopup(True)
        # 日历时间为当前时间
        self.datetime_inner.setDateTime(QDateTime.currentDateTime())
        # 布局
        layout.addWidget(self.datetime_inner)

        # 使用两个button(ok和cancel)分别连接accept()和reject()槽函数
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.datetime_inner.dateTimeChanged.connect(self.emit_signal)

    def emit_signal(self):
        date_str = self.datetime_inner.dateTime().toString()
        self.Signal_OneParameter.emit(date_str)

class RichTextEdit(QTextEdit):
    # 自定义信号returnPressed
    #returnPressed = pyqtSignal()
    # 自定义一个元组用来存储模式
    # 粗体字，斜体字，下划线，删除线，等宽字体，没有，衬线字体，没有上下标，下标，上标
    (Bold, Italic, Underline, StrikeOut, Monospaced, Sans, Serif,
     NoSuperOrSubscript, Subscript, Superscript) = range(10)
    # 构造函数

    def __init__(self, parent=None):
        super(RichTextEdit, self).__init__(parent)
        # 检查是否有按键按下
        self.key_modifiers = False
        key_modifiers = self.key_modifiers
        self.zoomsize = 2
        self.ctrlPressed = False
        self.initUI()

    # 界面初始化函数
    def initUI(self):
        self.monofamily = "courier"
        self.sansfamily = "helvetica"
        self.seriffamily = "times"
        """
        QTextEdit::NoWrap - 不自动换行。
        QTextEdit::WidgetWidth - 在窗口部件的当前宽度自动换行（这是默认的）。默认在空白符号处自动换行，这可以使用setWrapPolicy()
        来改变。
        QTextEdit::FixedPixelWidth - 从窗口部件的左侧开始的固定数量的象素数自动换行。象素的数量可以通过wrapColumnOrWidth()
        来设置。
        QTextEdit::FixedColumnWidth - 从窗口部件左侧开始的固定数量的列数自动换行。列数可以通过wrapColumnOrWidth()
        设置。如果你需要使用等宽文本在设备上显示很好的格式
        """
        # 每一行没有输入的限制
        self.setLineWrapMode(QTextEdit.NoWrap)
        # 自动换行
        #self.setLineWrapMode(QTextEdit.WidgetWidth)
        # If b is true, the Tab key will cause the widget to change focus;
        # otherwise, the tab key will insert a tab into the document.
        self.setTabChangesFocus(True)
        # 显示竖直方向的滚动条
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # 显示水平方向的滚动条
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # 获取字体宽度
        fm = QFontMetrics(self.font())
        # 设置气泡提示内容
        self.setToolTip("Press <b>Ctrl+M</b> for the text effects "
                "menu and <b>Ctrl+K</b> for the color menu")


    def toggleItalic(self):
        # 斜体（如果原来不是斜体则改为斜体）
        self.setFontItalic(not self.fontItalic())

    def toggleUnderline(self):
        # 下划线（如果原来没有下划线则添加下划线）
        self.setFontUnderline(not self.fontUnderline())

    def toggleBold(self):
        # 加粗（若字体未加粗则加粗，反之亦然）
        self.setFontWeight(QFont.Normal
                if self.fontWeight() > QFont.Normal else QFont.Bold)

    def sizeHint(self):
        # 提示
        return QSize(self.document().idealWidth() + 5,
                     self.maximumHeight())

    def minimumSizeHint(self):
        fm = QFontMetrics(self.font())
        return QSize(fm.width("WWWW"), self.minimumHeight())

    def contextMenuEvent(self, event):
    	# 右键快捷菜单（弹出对字体等的设定），这里采用的是对原函数的重载
        self.textEffectMenu()
      
    def keyPressEvent(self, event):
    	# 键盘事件的重载
    	# Qt::ControlModifier -- A Ctrl key on the keyboard is pressed.
    	# Returns the keyboard modifier flags that existed immediately before the event occurred.
        # 只要有键盘按下就为True
        self.key_modifiers = True
        key_modifiers = self.key_modifiers
        #if key_modifiers:
        #    print("key_modifiers = True")
        if event.modifiers():
            if Qt.ControlModifier:
                # ctrl按下的标志位
                self.ctrlPressed = True
                #ctrlPressed = self.ctrlPressed
        	# 操作位置为False，除非按下以下按键
                handled = False
            # Ctrl+B 加粗
                if event.key() == Qt.Key_B:
                    self.toggleBold()
                    handled = True
            # Ctrl+I 倾斜
                elif event.key() == Qt.Key_I:
                    self.toggleItalic()
                    handled = True
            # Ctrl+K 弹出colorMenu
                elif event.key() == Qt.Key_K:
                    self.colorMenu()
                    handled = True
            # Ctrl+M 弹出操作对话框
                elif event.key() == Qt.Key_M:
                    self.textEffectMenu()
                    handled = True
            # Ctrl+U 下划线
                elif event.key() == Qt.Key_U:
                    self.toggleUnderline()
                    handled = True  
                # 处理滚轮放大缩小事件
                return super().keyPressEvent(event)
            # 处理事件
            if handled:
                event.accept()
                return 
       	QTextEdit.keyPressEvent(self, event)
    
    # 键盘释放事件
    def keyReleaseEvent(self, event):
        if event.key()==QtCore.Qt.Key_Control:
            self.ctrlPressed=False
        return super().keyReleaseEvent(event)
    
    # 滚轮向上+Ctrl就放大
    def wheelEvent(self, event):
       if self.ctrlPressed:    
          delta = event.angleDelta()
          oriention = delta.y()/8
          self.zoomsize = 0
          if oriention > 0:
              self.zoomsize += 1
          else:
              self.zoomsize -= 1
          self.zoomIn(self.zoomsize)
       else:   
          return super().wheelEvent(event)
      
    # 颜色菜单
    def colorMenu(self):
    	# 颜色图例大小未22*22(像素)
        pixmap = QPixmap(22, 22)
        # 创建菜单
        menu = QMenu("Colour")
        for text, color in (
                ("&Black", Qt.black),
                ("B&lue", Qt.blue),
                ("Dark Bl&ue", Qt.darkBlue),
                ("&Cyan", Qt.cyan),
                ("Dar&k Cyan", Qt.darkCyan),
                ("&Green", Qt.green),
                ("Dark Gr&een", Qt.darkGreen),
                ("M&agenta", Qt.magenta),
                ("Dark Mage&nta", Qt.darkMagenta),
                ("&Red", Qt.red),
                ("&Dark Red", Qt.darkRed)):
        	# 制作颜色图例
            color = QColor(color)
            pixmap.fill(color)
            # 添加图例到菜单栏
            action = menu.addAction(QIcon(pixmap), text, self.setColor)
            action.setData(color)
        self.ensureCursorVisible()
        menu.exec_(self.viewport().mapToGlobal(self.cursorRect().center()))
    # 设置颜色
    def setColor(self):
        action = self.sender()
        if action is not None and isinstance(action, QAction):
            color = QColor(action.data())
            if color.isValid():
                self.setTextColor(color)

    def textEffectMenu(self):
    	# 字体为当前字体
        format = self.currentCharFormat()
        menu = QMenu("Text Effect")
        for text, shortcut, data, checked in (
                ("&Bold", "Ctrl+B", RichTextEdit.Bold,
                 self.fontWeight() > QFont.Normal),
                ("&Italic", "Ctrl+I", RichTextEdit.Italic,
                 self.fontItalic()),
                ("Strike &out", None, RichTextEdit.StrikeOut,
                 format.fontStrikeOut()),
                ("&Underline", "Ctrl+U", RichTextEdit.Underline,
                 self.fontUnderline()),
                ("&Monospaced", None, RichTextEdit.Monospaced,
                 format.fontFamily() == self.monofamily),
                ("&Serifed", None, RichTextEdit.Serif,
                 format.fontFamily() == self.seriffamily),
                ("S&ans Serif", None, RichTextEdit.Sans,
                 format.fontFamily() == self.sansfamily),
                ("&No super or subscript", None,
                 RichTextEdit.NoSuperOrSubscript,
                 format.verticalAlignment() ==
                 QTextCharFormat.AlignNormal),
                ("Su&perscript", None, RichTextEdit.Superscript,
                 format.verticalAlignment() ==
                 QTextCharFormat.AlignSuperScript),
                ("Subs&cript", None, RichTextEdit.Subscript,
                 format.verticalAlignment() ==
                 QTextCharFormat.AlignSubScript)):
            action = menu.addAction(text, self.setTextEffect)
            if shortcut is not None:
                action.setShortcut(QKeySequence(shortcut))
            action.setData(data)
            action.setCheckable(True)
            action.setChecked(checked)
        self.ensureCursorVisible()
        menu.exec_(self.viewport().mapToGlobal(
                   self.cursorRect().center()))

    def setTextEffect(self):
        action = self.sender()
        if action is not None and isinstance(action, QAction):
            what = action.data()
            if what == RichTextEdit.Bold:
                self.toggleBold()
                return
            if what == RichTextEdit.Italic:
                self.toggleItalic()
                return
            if what == RichTextEdit.Underline:
                self.toggleUnderline()
                return
            format = self.currentCharFormat()
            if what == RichTextEdit.Monospaced:
                format.setFontFamily(self.monofamily)
            elif what == RichTextEdit.Serif:
                format.setFontFamily(self.seriffamily)
            elif what == RichTextEdit.Sans:
                format.setFontFamily(self.sansfamily)
            if what == RichTextEdit.StrikeOut:
                format.setFontStrikeOut(not format.fontStrikeOut())
            if what == RichTextEdit.NoSuperOrSubscript:
                format.setVerticalAlignment(
                        QTextCharFormat.AlignNormal)
            elif what == RichTextEdit.Superscript:
                format.setVerticalAlignment(
                        QTextCharFormat.AlignSuperScript)
            elif what == RichTextEdit.Subscript:
                format.setVerticalAlignment(
                        QTextCharFormat.AlignSubScript)
            self.mergeCurrentCharFormat(format)
    

class MenuDemo(QMainWindow):
    def __init__(self, parent=None, filename=None):
        super(MenuDemo, self).__init__(parent)
        # 设置窗口大小1:0.618
        self.resize(1000, 618)
        location = os.path.abspath('QLabel.py')
        self.setWindowTitle(location + "--QMenuDemo")
        self.setWindowIcon(QIcon('./image/text.ico'))
        self.filename = filename
        self.textedit = RichTextEdit()
        self.setCentralWidget(self.textedit)
        self.initMenu()
        self.createToolbar()
        # 初始化状态下撤消、剪切、复制、删除为不可选状态
        self.initial()   
        # 定时器
        self.timer = QTimer()
        self.findDialog = FindDialog()
        # 100毫秒后启动
        self.timer.setInterval(100)    
        self.timer.start()
        self.timer.timeout.connect(self.onTimerOut)
        
        
    # 工具栏
    def createToolbar(self):
        toolbar = self.addToolBar('文件')
        toolbar.addAction(QAction(QIcon("./image/new.ico"), "新建", self, triggered=self.new))
        toolbar.addAction(QAction(QIcon("./image/open.ico"), "打开", self, triggered=self.open_file))
        toolbar.addAction(QAction(QIcon("./image/save.ico"), "保存", self, triggered=self.save_file))
        toolbar.addSeparator()
        toolbar = self.addToolBar("编辑")
        toolbar.addAction(QAction(QIcon("./image/size.ico"), "字体", self, triggered=self.font))
        toolbar.addAction(QAction(QIcon("./image/calendar.ico"), "日期", self, triggered=self.setCalendar))
        self.zoomin_key = toolbar.addAction(QAction(QIcon("./image/zoomIn.ico"), "放大", self, triggered=self.zoomIn))
        self.zoomout_key = toolbar.addAction(QAction(QIcon("./image/zoomOff.ico"), "缩小", self, triggered=self.zoomOff))  
        toolbar = self.addToolBar("浏览")
        self.network = toolbar.addAction(QAction(QIcon("./image/net.ico"), "搜索", self, triggered=self.network))  

    def initMenu(self):
        bar = self.menuBar()
        # 设定Menu并设定快捷键
        file = bar.addMenu("文件(&F)")
        edit = bar.addMenu("编辑(&E)")
        format = bar.addMenu("格式(&O)")
        view = bar.addMenu("查看(&V)")
        help = bar.addMenu("帮助(&H)")
        
        # 底部的状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        self.initFile(file)
        self.initEdit(edit)
        self.initFormat(format)
        self.initView(view)
        self.initHelp(help)
    

    def initFile(self, file):
        # 向file小控件中添加一个操作按钮，其中包含文本或图标
        new = file.addAction("新建(&N)")
        new.setShortcut("Ctrl+N")
        # 连接到槽函数new
        new.triggered.connect(self.new)

        open_file = QAction("打开(&O)...", self)
        open_file.setShortcut("Ctrl+O")
        file.addAction(open_file)
        # 连接到槽函数open_file
        open_file.triggered.connect(self.open_file)

        save_file = QAction("保存(&S)", self)
        save_file.setShortcut("Ctrl+S")
        file.addAction(save_file)
        # 连接到槽函数save_file
        save_file.triggered.connect(self.save_file)

        
        save_as_file = file.addAction("另存为(&A)...")
        # 连接到槽函数save_as_file
        save_as_file.triggered.connect(self.save_as_file)

        file.addSeparator()

        page_setting = file.addAction("页面设置(&U)...")

        printer = QAction("打印(&P)...", self)
        printer.setShortcut("Ctrl+P")
        file.addAction(printer)
        printer.triggered.connect(self.printer)

        file.addSeparator()

        exit_file = file.addAction("退出(&X)")
        exit_file.triggered.connect(self.exit_file)

    def initEdit(self, edit):
        self.revoke = edit.addAction("撤销(&U)")
        revoke = self.revoke
        revoke.setShortcut("Ctrl+Z")
        # 连接到槽函数revoke
        revoke.triggered.connect(self.Revoke)
        
        self.re_do = edit.addAction("恢复(&R)")
        re_do = self.re_do
        re_do.setShortcut("Ctrl+R")
        # 连接到槽函数re_do
        re_do.triggered.connect(self.Re_do)

        edit.addSeparator()

        self.cut = QAction("剪切(&T)", self)
        cut = self.cut
        cut.setShortcut("Ctrl+X")
        edit.addAction(cut)
        # 连接到槽函数Cut
        cut.triggered.connect(self.Cut)

        self.copy = QAction("复制(&C)", self)   
        copy = self.copy
        copy.setShortcut("Ctrl+C")
        edit.addAction(copy)
        # 连接到槽函数Copy
        copy.triggered.connect(self.Copy)

        self.paste = QAction("粘贴(&V)", self)
        paste = self.paste
        paste.setShortcut("Ctrl+V")
        edit.addAction(paste)
        # 连接到槽函数paste
        paste.triggered.connect(self.Paste)

        self.delete = QAction("删除(&L)", self)     
        delete = self.delete
        delete.setShortcut("Del")
        edit.addAction(delete)

        edit.addSeparator()

        self.find = QAction("查找(&F)...", self)
        find = self.find
        find.setShortcut("Ctrl+F")
        edit.addAction(find)
        # 连接到槽函数Find
        find.triggered.connect(self.Find)

        self.findNext = QAction("查找下一个(&N)", self)
        findNext = self.findNext
        findNext.setShortcut("F3")
        edit.addAction(findNext)

        replace = QAction("替换(&R)...", self)
        replace.setShortcut("Ctrl+H")
        edit.addAction(replace)

        goto = QAction("转到(&G)...", self)
        goto.setShortcut("Ctrl+G")
        edit.addAction(goto)

        edit.addSeparator()

        self.selectAll = QAction("全选(&A)", self)
        selectAll = self.selectAll
        selectAll.setShortcut("Ctrl+A")
        edit.addAction(selectAll)
        # 连接到槽函数SelectAll
        selectAll.triggered.connect(self.SelectAll)

        timedate = QAction("时间/日期(&D)", self)
        timedate.setShortcut("F5")
        edit.addAction(timedate)
        # 连接到槽函数timedate
        timedate.triggered.connect(self.timedate)

    def initFormat(self, format):
        autoNewline = format.addAction("自动换行(&W)")
        
        self.ZoomIn = QAction("放大", self)
        ZoomIn = self.ZoomIn
        ZoomIn.setShortcut("Ctrl+=")
        format.addAction(ZoomIn)
        ZoomIn.triggered.connect(self.zoomIn)

        self.ZoomOff = QAction("缩小", self)
        ZoomOff = self.ZoomOff
        ZoomOff.setShortcut("Ctrl+-")
        format.addAction(ZoomOff)
        ZoomOff.triggered.connect(self.zoomOff)

        font = format.addAction("字体(&F)...")
        # 连接到槽函数font
        font.triggered.connect(self.font)

    def initView(self, view):
        status = view.addAction("状态栏(&S)")

    def initHelp(self, help):
        aboutSoftware = help.addAction("关于软件(&A)")

        about = help.addMenu("查看(&H)")
        self.author = about.addAction("开发人员")
        author = self.author
        # 连接到槽函数Author
        author.triggered.connect(self.Author)
        
        self.version = about.addAction("版本")
        version = self.version
        # 连接到槽函数Version
        version.triggered.connect(self.Version)
        
    # 定义所有的需要另存为的情况
    def okToContinue(self):
        # 文件内容发生改变
        if self.textedit.document().isModified():
            reply = QMessageBox.question(self,
                            "Text Editor - Unsaved Changes",
                            "Save unsaved changes?",
                            QMessageBox.Yes|QMessageBox.No|
                            QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.No:
                return False
            elif reply == QMessageBox.Yes:
                return self.save_file()
        return True
        
    # 槽函数   
    def new(self):
        self.copy.setEnabled(True)
        if self.okToContinue():
            return
        else:
            document = self.textedit.document()
            document.clear()
            document.setModified(False)
            self.filename = None
            self.setWindowTitle("Text Editor - Unnamed")
        
    # 文件打开
    def open_file(self):
        self.copy.setEnabled(True)
        if not self.okToContinue():
            return
        dir = (os.path.dirname(self.filename)
               if self.filename is not None else ".")
        fname = str(QFileDialog.getOpenFileName(self,
                "text Editor - Choose File", dir,
                "text files (*.txt)")[0])
        if fname:
            self.filename = fname
            self.loadFile()
            
    # 重载关闭事件        
    def closeEvent(self, event):
        if not self.okToContinue():
            qApp = QCoreApplication.instance()
            qApp.quit()
            
    # 装载文件
    def loadFile(self):
        self.copy.setEnabled(True)
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            self.textedit.setPlainText(stream.readAll())
            self.textedit.document().setModified(False)
        except EnvironmentError as e:
            QMessageBox.warning(self, "Text Editor -- Load Error",
                    "Failed to load {0}: {1}".format(self.filename, e))
        finally:
            if fh is not None:
                fh.close()
        self.setWindowTitle("Text Editor - {0}".format(
                QFileInfo(self.filename).fileName()))
            
    # 设置字体
    def font(self, Font):
        fontSet, ok = QFontDialog.getFont()
        if ok:
            self.textedit.setFont(fontSet)
            
    # 打印当前日期以及时间到文本框
    def timedate(self, Timedate):
        self.copy.setEnabled(True)
        now = QDate.currentDate()#获取当前日期
        datetime = QDateTime.currentDateTime() #获取当前日期与时间
        time = QTime.currentTime() #获取当前时间
        #time_date = time.strftime("%Y-%m-%d %H:%M:%S")
        # Convenience slot that inserts text at the current cursor position.
        #ISO日期格式打印
        self.textedit.insertPlainText(now.toString(Qt.ISODate) + "\n")
        #本地化长格式日期打印
        self.textedit.insertPlainText(now.toString(Qt.DefaultLocaleLongDate) + "\n")
        #当前日期与时间打印
        self.textedit.insertPlainText(datetime.toString() + "\n")
        #本地化长格式时间打印
        self.textedit.insertPlainText(time.toString(Qt.DefaultLocaleLongDate) + "\n")
    
    # 日历label所能触发的槽函数
    def setCalendar(self):
        # 实例化
        dialog = DateDialog(self)
        '''连接子窗口的内置信号与主窗口的槽函数'''
        dialog.datetime_inner.dateTimeChanged.connect(self.deal_inner_slot)
        dialog.show()
    
    def deal_inner_slot(self, date):
        self.dateSplit = date.toString().split(' ')
        self.datePerfict = "\n您所选定的日期是：" + self.dateSplit[4] + "年" \
                            + self.dateSplit[1] + self.dateSplit[2] + "日" \
                            + "\n当前时间为：" + self.dateSplit[3] \
                            + "\n现在是" + self.dateSplit[0] + "哦"  
        # 输入到文本对话框内
        self.textedit.insertPlainText(self.datePerfict)
        
    # 保存文档
    def save_file(self):
        self.copy.setEnabled(True)
        if self.filename is None:
            return self.save_as_file()
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            stream << self.textedit.toPlainText()
            self.textedit.document().setModified(False)
        except EnvironmentError as e:
            QMessageBox.warning(self, "text Editor -- Save Error",
                    "Failed to save {0}: {1}".format(self.filename, e))
            return False
        finally:
            if fh is not None:
                fh.close()
        return True
    
    # 文件另存为
    def save_as_file(self):
        self.copy.setEnabled(True)
        filename = self.filename if self.filename is not None else "."
        filename,filetype = QFileDialog.getSaveFileName(self,
                "text Editor -- Save File As", filename,
                "text files (*.txt)")
        if filename:
            self.filename = filename
            self.setWindowTitle("text Editor - {0}".format(
                    QFileInfo(self.filename).fileName()))
            return self.save_file()
        return False
    
    # 连接到打印机
    def printer(self):
        printer = QPrinter()
        printDialog = QPrintDialog(printer, self)
        if printDialog.exec_():
            painter = QPainter(printer)
            rect = painter.viewport()
            size = self.textedit.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.textedit.rect())
            painter.drawText(0, 0, self.textedit)
            
    # 退出功能实现
    def exit_file(self):
        if self.textedit.document().isModified():
            reply = QMessageBox.question(self,
                            "Text Editor - Unsaved Changes",
                            "Save unsaved changes?",
                            QMessageBox.Yes|QMessageBox.No|
                            QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.No:
                return False
            elif reply == QMessageBox.Yes:
                return self.save_file()
        else:
            qApp = QCoreApplication.instance()
            qApp.quit()
    
    # 全选
    def SelectAll(self):
        self.textedit.selectAll()
        self.cut.setEnabled(True)          # 剪切
        self.copy.setEnabled(True)         # 复制
        self.delete.setEnabled(True)       # 删除
        self.find.setEnabled(True)         # 查找
        self.findNext.setEnabled(True)     # 查找下一个     
    
    # 复制
    def Copy(self):
        self.textedit.copy()
    
    # 粘贴
    def Paste(self):
        if self.copy.isEnabled() == True:
            self.textedit.paste()
            
    # 剪切    
    def Cut(self):
        self.textedit.cut()
    
    # 撤消
    def Revoke(self):
        self.textedit.undo()
    
    # 恢复
    def Re_do(self):
        self.textedit.redo()
    
    def Find(self):
        Find_Dialog = self.findDialog
        # 单行文本控件水平方向左对齐
        Find_Dialog.lineEdit.setAlignment(Qt.AlignLeft)
        # 当按下回车键时，发射这个信号
        #Find_Dialog.lineEdit.returnPressed.connect(self.button2)
        Find_Dialog.pushButton_2.clicked.connect(self.button2)
        Find_Dialog.show()
        #print(self.textedit.find("abc"))
        
    def button2(self):
        # 判断QLineEdit是否为空，若为空则弹出对话框
        if self.findDialog.lineEdit.text() == "":
            QMessageBox.information(self, "Empty search field", "The search field is empty.")
        # 不为空则进行查找
        else:
            if self.findDialog.checkBox.isChecked():
                # 选中向下查找
                if self.findDialog.QRadioButton_2.isChecked():
                    # 获取单行文本控件内容
                    self.ledit_text = self.findDialog.lineEdit.text()
                    Ledit_Text = self.ledit_text
                    if self.textedit.find(Ledit_Text):
                        # 查找到的文本高亮显示
                        print("True")
                        # 否则弹出消息对话框
                    else:
                        QMessageBox.information(self, "textEdit", "找不到"+"\""+Ledit_Text+"\"", QMessageBox.Yes)
                # 选中向下查找
                if self.findDialog.QRadioButton_1.isChecked():
                    pass
            else:
                pass

                
    # 按键变大字体
    def zoomIn(self):
        self.textedit.zoomsize += 1
        self.textedit.zoomIn(self.textedit.zoomsize)
    
    # 按键缩小字体
    def zoomOff(self):
        self.textedit.zoomsize -= 1
        self.textedit.zoomOut(self.textedit.zoomsize)
    
    # 打开百度网页
    def network(self):
        webbrowser.open("http://www.baidu.com")
    
    # 作者相关
    def Author(self):
        QMessageBox.about(self, "Author", "\n振宇工作室")
    
    # 版本相关
    def Version(self):
        QMessageBox.about(self, "Version", "Version:\nV1.0.0\nTime:\n2018-5-14")
    
    # 初始化状态下撤消、剪切、复制、删除为不可选状态
    def initial(self):
        # 如果文档内容为空，则以下按键为不可选状态
        if self.textedit.document().isEmpty():
            self.revoke.setEnabled(False)       # 撤销
            self.re_do.setEnabled(False)        # 恢复
            self.cut.setEnabled(False)          # 剪切
            self.copy.setEnabled(False)         # 复制
            self.delete.setEnabled(False)       # 删除
            self.find.setEnabled(False)         # 查找
            self.findNext.setEnabled(False)     # 查找下一个     
    
    # 定时器控制事件发生        
    def onTimerOut(self):     
        # 在定时器中检查键盘按下置位符
        if self.textedit.key_modifiers:
            self.revoke.setEnabled(True)
            self.re_do.setEnabled(True)
        #if self.textedit.textCursor.selectedText():


if __name__ == "__main__":           
    app = QApplication(sys.argv)
    demo = MenuDemo()
    demo.show()
    sys.exit(app.exec_())
