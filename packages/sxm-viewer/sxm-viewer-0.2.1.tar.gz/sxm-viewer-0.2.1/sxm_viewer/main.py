# test.py by Cocca Guo at 2020/12/22 14:25:58
# main.py by Cocca Guo at 2021/01/07 11:47:21 version 0.2, add options and warnings.


import os
import sys
import configparser

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

import pySPM


class Main_window(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(Main_window,self).__init__(parent)
        self.initialize()
        

    def initialize(self):
        self.setWindowTitle("SXM File Viewer")
        # self.setWindowState(Qt.WindowMaximized)
        self.resize(900, 900)
        self.setWindowIcon(QIcon("icon.png"))
        self.setup_config()
        self.setup_menu()
        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.setCentralWidget(QtWidgets.QWidget())


    # this func only loads once when program starts
    def setup_config(self):
        self.cfg_file_setup()
        self.current_file = None
        self.current_dir = None
        self.current_index = None
        self.cfg = configparser.ConfigParser()
        self.cfg.read(os.path.join(self.root_path, "config.ini"))
        if int(self.cfg.get("sys", "help_info")): self.help()


    def refresh_config(self):
        with open(os.path.join(self.root_path, "config.ini"), "w+") as f:
            self.cfg.write(f)  


    def setup_menu(self):
        self.m_file = QtWidgets.QMenu("File")
        self.m_tool = QtWidgets.QMenu("Tool")
        self.m_help = QtWidgets.QMenu("Help")

        self.m_file_open = QtWidgets.QAction("Open", self.m_file)
        self.m_file_open.triggered.connect(self.open_file)
        self.m_file.addAction(self.m_file_open)

        self.m_file_opendir = QtWidgets.QAction("Open Folder", self.m_file)
        self.m_file_opendir.triggered.connect(self.open_folder)
        self.m_file.addAction(self.m_file_opendir)

        self.m_tool_save_pic = QtWidgets.QAction("Save Figure", self.m_tool)
        self.m_tool_save_pic.triggered.connect(self.save_pic)
        self.m_tool.addAction(self.m_tool_save_pic)

        self.m_help_options = QtWidgets.QAction("Options", self.m_help)
        self.m_help_options.triggered.connect(self.options)
        self.m_help.addAction(self.m_help_options)
        
        self.m_help_help = QtWidgets.QAction("Help", self.m_help)
        self.m_help_help.triggered.connect(self.help)
        self.m_help.addAction(self.m_help_help)

        self.m_help_about = QtWidgets.QAction("About", self.m_help)
        self.m_help_about.triggered.connect(self.about)
        self.m_help.addAction(self.m_help_about)

        self.menuBar().addMenu(self.m_file)
        self.menuBar().addMenu(self.m_tool)
        self.menuBar().addMenu(self.m_help)


    def open_file(self):
        self.current_dir = None
        self.current_index = None
        fileName_choose, _ = QtWidgets.QFileDialog.getOpenFileName(self,  "Choose file",  self.cfg.get("file", "last_file"),  "SXM Files (*.sxm)")
        if fileName_choose == "": return
        self.cfg.set("file", "last_file", fileName_choose)
        self.refresh_config()
        self.current_file = fileName_choose
        self.statusBar.showMessage("file loaded: "+self.current_file)
        self.sxm_show()


    def render_dirpath(self): # 从打开文件也可以打开文件夹下其他文件
        self.current_dir = os.path.dirname(self.current_file)
        self.dir_list = os.listdir(self.current_dir)
        self.total_num = len(self.dir_list)
        self.current_index = self.dir_list.index(os.path.basename(self.current_file))


    def open_folder(self):
        folder_choose = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose Folder", self.cfg.get("file", "last_dir"))
        if folder_choose == "": return
        self.cfg.set("file", "last_dir", folder_choose)
        self.refresh_config()
        self.current_dir = folder_choose
        self.statusBar.showMessage("folder loaded: "+self.current_dir)
        self.dir_list = os.listdir(self.current_dir)
        self.total_num = len(self.dir_list)
        self.statusBar.showMessage(str(self.total_num)+" file loaded.")
        self.current_index = 0
        self.sxm_folder_show()


    def save_pic(self):
        if self.current_file is None: 
            QtWidgets.QMessageBox.information(self, "Infomation", "please open a file first.", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
            return
        fname = QtWidgets.QFileDialog.getSaveFileName(self, "Save Figure", self.cfg.get("file", "output_dir"), "Image Files (*.png)")     
        if fname[0]:
            self.save(self.current_file, fname[0])

    
    def save(self, sxmpath: str, savepath: str):
        if not sxmpath.endswith(".sxm"): return
        sxm = pySPM.SXM(sxmpath)
        channel=self.cfg.get("plot", "channel")
        sxm.get_channel(channel).show(cmap=self.cfg.get("save", "cmap"))
        if int(self.cfg.get("save", "show_title")) == 0:
            plt.title(None)
        try:
            if int(self.cfg.get("save", "show_axis")) == 0:
                plt.savefig(savepath, dpi=int(self.cfg.get("save", "fig_dpi")), bbox_inches = 'tight',pad_inches = 0)
            else:
                plt.savefig(savepath, dpi=int(self.cfg.get("save", "fig_dpi")))
        except PermissionError as e:
            QtWidgets.QMessageBox.warning(self, "unable to save", "Unable to save due to a PermissionError. Have you changed the the default path in Help-Options?", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)


    def options(self):
        self.opt_win = Options(os.path.join(self.root_path, "config.ini"))


    def help(self):
        help_txt = self.cfg.get("about", "help")
        QtWidgets.QMessageBox.information(self, "Help", help_txt, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)


    def about(self):
        infor = self.cfg.get("about", "info")
        QtWidgets.QMessageBox.information(self, "About", infor, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)


    def sxm_show(self):
        plt.close()
        plt.cla()
        fig = plt.figure()
        ax =fig.add_subplot()
        try:
            sxm = pySPM.SXM(self.current_file)
        except KeyError as err:
            QtWidgets.QMessageBox.warning(self, "Unable to read the file", "Unable to read the file: "+self.current_file+", is it an available sxm file?", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
            return
        channel = self.cfg.get("plot", "channel")
        cmap = self.cfg.get("plot", "cmap")
        if int(self.cfg.get("plot", "show_axis")) == 0:
            plt.axis('off') 
        title = os.path.basename(self.current_file)
        if int(self.cfg.get("plot", "show_title")) == 0:
            title = ""
        sxm.get_channel(channel).show(cmap=cmap, ax=ax, title=title)
        canvas = FigureCanvas(fig)
        self.setCentralWidget(canvas)

    
    def sxm_folder_show(self):
        self.statusBar.showMessage("current index "+str(self.current_index+1)+" / "+str(self.total_num))
        self.current_file = os.path.join(self.current_dir, self.dir_list[self.current_index])
        self.sxm_show()
        

    # step = +1/-1
    def sxm_folder_change(self, step):
        if self.current_file is not None and self.current_index is None:
            self.render_dirpath()
        if self.current_index is not None and (self.current_index+step)>-1 and (self.current_index+step)<self.total_num:
            self.current_index += step
            if self.dir_list[self.current_index].endswith(".sxm"):
                    self.sxm_folder_show()


    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key()== Qt.Key_S:
            if self.current_file is not None:
                path = os.path.join(self.cfg.get("file", "output_dir"), os.path.basename(self.current_file))+".png"
                self.save(self.current_file, path)
                self.statusBar.showMessage("figure saved: "+path)
        if QKeyEvent.key()== Qt.Key_Up or QKeyEvent.key()== Qt.Key_Left:
            self.sxm_folder_change(-1)
        if QKeyEvent.key()== Qt.Key_Down or QKeyEvent.key()== Qt.Key_Right:
            self.sxm_folder_change(1)

    
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.sxm_folder_change(-1)
        if event.angleDelta().y() < 0:
            self.sxm_folder_change(1)

    
    def cfg_file_setup(self):
        cfg_txt = """
[file]
output_dir = /
last_file = /
last_dir = /

[sys]
help_info = 1

[plot]
show_title = 1
show_axis = 1
channel = Current
cmap = viridis

[save]
show_title = 0
show_axis = 0
cmap = viridis
fig_dpi = 100

[about]
help = This tool aims to inspect and save figures fast. Load a folder, and use up/down to switch the files swiftly. Press key S to save the .png file directly(configure the save_dir in help-option first). Suppress this help_info in options.
info = Ver 0.2 by Cocca on 2021.1.7
"""
        self.root_path = os.path.join(os.getcwd(), '.sxm_viewer')
        if not os.path.exists(self.root_path):
            os.mkdir(self.root_path)
        if not os.path.exists(os.path.join(self.root_path, "ver0.2")):
            with open(os.path.join(self.root_path, "ver0.2"), 'w') as f:
                f.write("version 0.2")
            with open(os.path.join(self.root_path, "config.ini"), 'w') as f:
                f.write(cfg_txt)
            # QtWidgets.QMessageBox.warning(self, "config file not found", "config file not found, program will exit.", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
            


class Options(QtWidgets.QWidget):
    def __init__(self, cfg_path):
        super().__init__()
        self.cfg = cfg_path
        self.initialize()

    def initialize(self):
        self.setWindowTitle('Options: apply when restarts')
        self.resize(700, 700)

        self.readOptions()

        okButton = QtWidgets.QPushButton("OK")
        okButton.clicked.connect(self.refresh)
        cancelButton = QtWidgets.QPushButton("Cancel")
        cancelButton.clicked.connect(self.close)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)


        vbox = QtWidgets.QVBoxLayout()
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self.textEdit)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)   

        self.show()

    def readOptions(self):
        self.textEdit = QtWidgets.QTextEdit() 
        with open(self.cfg,'r+') as f:
            self.textEdit.setText(f.read())
    
    def refresh(self):
        with open(self.cfg,'w') as f:
            f.write(self.textEdit.toPlainText())
        self.close()
            

    
def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()
    main_window.show()
    app.exec()


# main.py by Cocca Guo at 2020/12/22 20:05:39
# completed programming on this special day.
if __name__ == '__main__':
    main()