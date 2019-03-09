import sys
import os
import json
import glob
import sqlite3
import shutil
from datetime import datetime
import time

from about import Ui_About
from report_info import Ui_ReportInfo
from UsageStatsMain import Ui_UsageStats
from UsageStatsNew import Ui_Form
from usagestats_conv import parsefile
from recenttasks_conv import datatoparse
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


from PyQt5 import QtCore, QtGui, QtWidgets

class RunThread(QtCore.QThread):

    processedfile = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()

    def __init__(self,parent = None):
        super(RunThread, self).__init__(parent)

        self.folder_name = ""
        self.file_type = ""
        self.parsedatapath = ""
        self.currentstate = {}
        self.imagefolder = ''


    def run(self):
        self.is_running = True
        while self.is_running:
            if self.file_type == "usagestats":
                db = sqlite3.connect(f"{self.parsedatapath}/usagestats.db")
                cursor = db.cursor()
                cursor.execute('''
                    CREATE TABLE data(usage_type TEXT, lastime TEXT, timeactive TEXT, package TEXT, types TEXT, classs TEXT,source TEXT, fullatt TEXT)
                    ''')
                db.commit()
            elif self.file_type == "Recenttask":
                db = sqlite3.connect(f"{self.parsedatapath}/RecentAct.db")
                cursor = db.cursor()
                cursor.execute('''
					CREATE TABLE data(task_id TEXT, effective_uid TEXT, affinity TEXT, real_activity TEXT, first_active_time TEXT, last_active_time TEXT,
								  last_time_moved TEXT, calling_package TEXT, user_id TEXT, action TEXT, component TEXT, snap TEXT,
								  recimg TXT, fullat1 TEXT, fullat2 TEXT)
					''')
                db.commit()

            for filename in glob.iglob(self.folder_name+r'\**', recursive=True):
                if os.path.isfile(filename):
                    self.processedfile.emit(filename)
                    if self.file_type == "usagestats":
                        usagestatsdata = parsefile(filename,db)
                        usagestatsdata.parse_usagestats_file()
                    elif self.file_type == "Recenttask":
                        recenttaskdata = datatoparse(filename,db,self.parsedatapath,self.imagefolder)
                        recenttaskdata.parse_recenttask_file()
            self.is_running = False
        self.finished.emit()

class RunThread2(QtCore.QThread):

    finished = QtCore.pyqtSignal(str)

    def __init__(self,parent = None):
        super(RunThread2, self).__init__(parent)
        self.checkvalue = None
        self.evidence_number = None
        self.device_owner = None
        self.case_number = None
        self.Investigator = None
        self.crime_code = None
        self.table = None
        self.type = None
        self.picturepath = None
        self.path = os.getcwd()


    def run(self):
        self.is_running = True
        while self.is_running:
            all_rows = self.table.rowCount()
            if self.type == "Recenttask":
                Save_Location = os.path.expanduser('~')
                with open(f'{Save_Location}\\Documents\\US_RT Reports\\{self.case_number}_{self.evidence_number}_Recent_Activity.html', 'w') as f1:
                    f1.write('<html><body>')
                    f1.write('<h2> Android Recent Tasks Report </h2>')
                    f1.write(f'<h3> Case Number: {self.case_number} </h3>')
                    f1.write(f'<h3> Item Number: {self.evidence_number} </h3>')
                    f1.write(f'<h3> Crime Code: {self.crime_code} </h3>')
                    f1.write(f'<h3> Report Created By: {self.Investigator} </h3>')

                    f1.write ('<style> table, th, td {border: 1px solid black; border-collapse: collapse;} img {width: 180px; height: 370px; object-fit: cover;}</style>')
                    for row in range(0,all_rows):
                        checked = self.table.item(row, 0).checkState()
                        if checked in self.checkvalue:
                            affinity = self.table.item(row,3).text()
                            if affinity == '':
                                f1.write(f'<h3> Application: No Data<h3>')
                            else:
                                f1.write(f'<h3> Application: {affinity}<h3>')


                            f1.write('<table> <tr><th>Key</th><th>Values</th></tr>')
                            for col in range(1,11):
                                f1.write('<tr>')
                                f1.write('<td align="left">')
                                f1.write(self.table.horizontalHeaderItem(col).text())
                                f1.write('</td>')
                                f1.write('<td align="left">')
                                f1.write(self.table.item(row,col).text())
                                f1.write('</td>')
                                f1.write('</tr>')


                            f1.write('<tr>')
                            f1.write('<td align="left">')
                            f1.write('Snapshot_Image')
                            f1.write('</td>')
                            f1.write('<td align="left">')
                            rname = self.picturepath[f'{row}_12']
                            if rname != 'No Image' or rname != 'NO Image':
                                try:
                                    rname = rname.rsplit('\\',1)[1]
                                except:
                                    pass
                            f1.write(rname)
                            f1.write('</td>')
                            f1.write('</tr>')

                            f1.write('<tr>')
                            f1.write('<td align="left">')
                            f1.write('Recent_Image')
                            f1.write('</td>')
                            f1.write('<td align="left">')
                            rname = (self.picturepath[f'{row}_13'])
                            if rname != 'No Image':
                                try:
                                    rname = rname.rsplit('\\',1)[1]
                                except:
                                    pass
                            f1.write(rname)
                            f1.write('</td>')
                            f1.write('</tr>')

                            f1.write('</table></p>')
                            f1.write('<table> <tr><th>Snapshot_Images</th><th>Recent_Image</th></tr>')
                            f1.write('<tr>')
                            if self.picturepath[f'{row}_12'].lower() == 'no image':
                                f1.write('<td align="left">')
                                f1.write(f'<img src="{self.path}/icons/noimg.jpg" alt="no image">')
                                f1.write('</td>')
                            else:
                                f1.write('<td align="left">')
                                f1.write('<a href="')
                                f1.write(self.picturepath[f'{row}_12'])
                                f1.write('"><img src="')
                                f1.write(self.picturepath[f'{row}_12'])
                                f1.write('" alt="Smiley face">')
                                f1.write('</a>')
                                f1.write('</td>')

                            if self.picturepath[f'{row}_13'].lower() == 'no image':
                                f1.write('<td align="left">')
                                f1.write(f'<img src="{self.path}/icons/noimg.jpg" alt="no image">')
                                f1.write('</td>')
                            else:
                                f1.write('<td align="left">')
                                f1.write('<a href="')
                                f1.write(self.picturepath[f'{row}_13'])
                                f1.write('"><img src="')
                                f1.write(self.picturepath[f'{row}_13'])
                                f1.write('" alt="Smiley face">')
                                f1.write('</a>')
                                f1.write('</td>')
                        f1.write('</tr>')
                        f1.write('</table></p>')
            if self.type == "usagestats":
                Save_Location = os.path.expanduser('~')
                with open(f'{Save_Location}\\Documents\\US_RT Reports\\{self.case_number}_{self.evidence_number}_UsageStats.html', 'w') as h:
                    h.write('<html><body>')
                    h.write('<h2>Android Usagestats report</h2>')
                    h.write(f'<h3> Case Number: {self.case_number} </h3>')
                    h.write(f'<h3> Item Number: {self.evidence_number} </h3>')
                    h.write(f'<h3> Crime Code: {self.crime_code} </h3>')
                    h.write(f'<h3> Report Created By: {self.Investigator} </h3>')
                    h.write ('<style> table, th, td {border: 1px solid black; border-collapse: collapse;}</style>')
                    h.write('<br />')
                    h.write('<table>')
                    h.write('<tr>')
                    h.write('<th>Usage Type</th>')
                    h.write('<th>Last Time Active</th>')
                    h.write('<th>Time Active in Msecs</th>')
                    h.write('<th>Package</th>')
                    h.write('<th>Types</th>')
                    h.write('<th>Class</th>')
                    h.write('<th>Source</th>')
                    h.write('</tr>')
                    for row in range(all_rows):
                        checked = self.table.item(row, 0).checkState()
                        if checked in self.checkvalue:
                            usage_type = self.table.item(row,1).text()
                            lasttimeactive = self.table.item(row,2).text()
                            time_Active_in_msecs = self.table.item(row,3).text()
                            package = self.table.item(row,4).text()
                            types = self.table.item(row,5).text()
                            classs = self.table.item(row,6).text()
                            source = self.table.item(row,7).text()

                            h.write('<tr>')
                            h.write(f'<td>  {usage_type}    </td>')
                            h.write(f'<td>  {lasttimeactive}  </td>')
                            h.write(f'<td>  {time_Active_in_msecs}  </td>')
                            h.write(f'<td>  {package}   </td>')
                            h.write(f'<td>  {types} </td>')
                            h.write(f'<td>  {classs}    </td>')
                            h.write(f'<td>  {source}    </td>')
                            h.write('</tr>')
                    h.write('<table>')
                    h.write('<br />')

            self.is_running = False
            if self.type == 'Recenttask':
                self.finished.emit(f'{Save_Location}\\Documents\\US_RT Reports\\{self.case_number}_{self.evidence_number}_Recent_Activity.html')
            if self.type == "usagestats":
                self.finished.emit(f'{Save_Location}\\Documents\\US_RT Reports\\{self.case_number}_{self.evidence_number}_UsageStats.html')

class MainWindow_EXEC():

    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_UsageStats()
        self.ui.setupUi(MainWindow)
        self.tableicon = None
        self.headerItem = None
        self.chkBoxItem = None
        self.currentstate = {}
        self.type = None
        self.model = None
        self.evidence_number = None
        self.device_owner = None
        self.case_number = None
        self.Investigator = None
        self.crime_code = None
        self.picturepath = {}

        self.ui.actionNew_Case_2.triggered.connect(self.newcasewindow)
        self.current_dir = None
        self.ui.actionOpen_Case.triggered.connect(self.openusagestatscasewindow)
        self.ui.actionRemove_Case_Folder.triggered.connect(self.deletefolderwindow)
        self.ui.radioButton_4.toggled.connect(lambda:self.btnstate(self.ui.radioButton_4))
        self.ui.radioButton_2.toggled.connect(lambda:self.btnstate(self.ui.radioButton_2))
        self.ui.radioButton_3.toggled.connect(lambda:self.btnstate(self.ui.radioButton_3))
        self.ui.pushButton.clicked.connect(self.create_html_report)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionRead_Me.triggered.connect(self.readme)


        MainWindow.show()
        sys.exit(app.exec_())

    def readme(self):
        os.startfile(os.getcwd()+'/icons/Help.pdf')

    def about(self):
        self.aboutWindow = QtWidgets.QWidget()
        self.about = Ui_About()
        self.about.setupUi(self.aboutWindow)
        self.aboutWindow.show()

    def btnstate(self,button):
        for k,v in self.currentstate.items():
            if button.text() == "Show All":
                self.ui.tableWidget.setRowHidden(k, False)
            elif button.text() == "Show Checked":
                if v == 2:
                    self.ui.tableWidget.setRowHidden(k, False)
                elif v == 0:
                    self.ui.tableWidget.setRowHidden(k, True)
            elif button.text() == "Show Unchecked":
                if v == 2:
                    self.ui.tableWidget.setRowHidden(k, True)
                elif v == 0:
                    self.ui.tableWidget.setRowHidden(k, False)

    def newcasewindow(self):
        self.newCaseWindow = QtWidgets.QWidget()
        self.newui = Ui_Form()
        self.newui.setupUi(self.newCaseWindow)
        self.newui.buttonBox.accepted.connect(self.getfile)
        self.newCaseWindow.show()


    def getfile(self):
        case_Number = self.newui.lineEdit.text()
        evidence_item_number = self.newui.lineEdit_3.text()
        investigator = self.newui.lineEdit_4.text()
        crime_code = self.newui.lineEdit_2.text()
        device_owner = self.newui.lineEdit_6.text()

        blank = [case_Number,evidence_item_number,investigator,crime_code]

        if "" in blank:
                error_dialog = QtWidgets.QMessageBox()
                error_dialog.setIcon(QtWidgets.QMessageBox.Warning)
                error_dialog.setWindowTitle('Error')
                error_dialog.setText('All Fields Are Required!')
                error_dialog.setStandardButtons(QtWidgets.QMessageBox.Close)
                error_dialog.exec()
        elif self.newui.radioButton.isChecked() == False and self.newui.radioButton_2.isChecked() == False:
                error_dialog = QtWidgets.QMessageBox()
                error_dialog.setIcon(QtWidgets.QMessageBox.Warning)
                error_dialog.setWindowTitle('Error')
                error_dialog.setText('Please select a file type!')
                error_dialog.setStandardButtons(QtWidgets.QMessageBox.Close)
                error_dialog.exec()
        else:
            if self.newui.radioButton.isChecked():
                self.filetype = "usagestats"
            if self.newui.radioButton_2.isChecked():
                self.filetype = "Recenttask"

            filename = QtWidgets.QFileDialog.getExistingDirectory()

            if filename != "":
                self.newCaseWindow.close()
                self.current_dir = os.getcwd()+f"/CaseFolders/{case_Number}/{evidence_item_number}"
                if os.path.isdir(self.current_dir):
                    pass
                else:
                    os.makedirs(self.current_dir)
                if self.filetype == "usagestats":
                    datapath = f"{self.current_dir}/usagestats.db"
                elif self.filetype == "Recenttask":
                    os.makedirs(f'{self.current_dir}/images')
                    datapath = f"{self.current_dir}/RecentAct.db"
                f = f"{self.current_dir}/{evidence_item_number}_{self.filetype}.json"
                if os.path.isfile(f):
                    error_dialog = QtWidgets.QMessageBox()
                    error_dialog.setIcon(QtWidgets.QMessageBox.Warning)
                    error_dialog.setWindowTitle('Error')
                    error_dialog.setText(f'{self.filetype} for this item alread exists!')
                    error_dialog.setStandardButtons(QtWidgets.QMessageBox.Close)
                    error_dialog.exec()

                else:
                    with open(f,"w") as casefile:
                        json.dump({"Case Number": case_Number,"Item Number": evidence_item_number,"Investigator": investigator,"Crime Code": crime_code,"Device Owner": device_owner,"File Type": self.filetype,"Data Path": datapath},casefile)
                        self.createdb(filename,self.filetype,self.current_dir)


    def createdb(self,filename, filetype, current_dir):
        self.run_thread = RunThread()
        self.run_thread.folder_name = filename
        self.run_thread.file_type = filetype
        self.run_thread.parsedatapath = current_dir
        self.run_thread.imagefolder = f'{self.current_dir}/images'
        self.run_thread.start()
        self.run_thread.processedfile.connect(self.printprocessedfile)
        self.run_thread.finished.connect(self.finishedfile)

    def printprocessedfile(self,filename):
        self.ui.statusbar.showMessage(f"Processing {filename}")

    def finishedfile(self):
        self.run_thread.quit()
        self.ui.statusbar.showMessage(f"Processing Finished")
        finished_dialog = QtWidgets.QMessageBox()
        finished_dialog.setIcon(QtWidgets.QMessageBox.Information)
        finished_dialog.setWindowTitle('Processing Finished')
        finished_dialog.setText('Processing Files is Finished')
        finished_dialog.setStandardButtons(QtWidgets.QMessageBox.Close)
        finished = finished_dialog.exec()
        if finished == QtWidgets.QMessageBox.Close:
            self.getusagestatsjson(self.current_dir)

    def openusagestatscasewindow(self):
        qfd = QtWidgets.QFileDialog()
        path = os.getcwd()
        title = "Open"
        filter = "json(*.json)"
        filename = QtWidgets.QFileDialog.getOpenFileName(qfd,title,path,filter)[0]
        if filename != "":
            self.loadusagestatstale(filename)

    def getusagestatsjson(self, casedir):
        if self.filetype == "usagestats":
            filename = glob.glob(casedir+'/*_usagestats.json')[0]
        elif self.filetype == "Recenttask":
            filename = glob.glob(casedir+'/*_Recenttask.json')[0]
        self.loadusagestatstale(filename)

    def deletefolderwindow(self):
        qfd = QtWidgets.QFileDialog()
        path = os.getcwd()
        title = "Delete Case/Evidence Item Folder"
        foldername = QtWidgets.QFileDialog.getExistingDirectory(qfd,title,path)
        self.areyousurefolder(foldername)

    def areyousurefolder(self,foldername):
        folder = foldername.split("/")[-1]
        type = "folder"
        areyousure_dialog = QtWidgets.QMessageBox()
        areyousure_dialog.setIcon(QtWidgets.QMessageBox.Warning)
        areyousure_dialog.setWindowTitle('Delete Case/Evidence Folder')
        if folder == "CaseFolders":
            areyousure_dialog.setText(f'\nCannot Delete All Case Folders at one time!               ')
            areyousure_dialog.setStandardButtons(QtWidgets.QMessageBox.Cancel)
        elif 'CaseFolders' not in foldername:
            areyousure_dialog.setText(f'\nCannot Delete Folders not         \n            associate to this program!')
            areyousure_dialog.setStandardButtons(QtWidgets.QMessageBox.Cancel)
        else:
            areyousure_dialog.setText(f'Are you sure you want to remove           \n              {folder}!')
            areyousure_dialog.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.Cancel)
        answer = areyousure_dialog.exec()
        if answer == QtWidgets.QMessageBox.Cancel:
            areyousure_dialog.close()
        elif answer == QtWidgets.QMessageBox.Yes:
            self.removefile(foldername,type)


    def removefile(self,filename,type):
        try:
            shutil.rmtree(filename)
        except:
            print("can't remove")

    def loadusagestatstale(self,usagejson):
        self.ui.tableWidget.setRowCount(0)
        self.ui.radioButton_4.setEnabled(True)
        self.ui.radioButton_2.setEnabled(True)
        self.ui.radioButton_3.setEnabled(True)
        self.ui.radioButton_4.setChecked(True)
        self.ui.groupBox_2.setEnabled(True)
        rowPosition = 0
        self.ui.statusbar.showMessage("")
        with open(usagejson) as f:
            casedata = json.load(f)
        self.evidence_number = casedata["Item Number"]
        self.ui.label_4.setText(casedata["Item Number"])
        self.device_owner = casedata["Device Owner"]
        self.ui.label_5.setText(casedata["Device Owner"])
        self.case_number = casedata["Case Number"]
        self.ui.label_6.setText(casedata["Case Number"])
        self.Investigator = casedata["Investigator"]
        self.crime_code = casedata['Crime Code']
        db = casedata["Data Path"]
        self.filetype = casedata["File Type"]
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute("Select * From data")
        data = cur.fetchall()
        self.tableicon = os.getcwd()+'/icons/checked.png'
        self.headerItem = QtWidgets.QTableWidgetItem()
        self.headerItem.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
        self.headerItem.setIcon(QtGui.QIcon(QtGui.QPixmap(self.tableicon)))

        if self.filetype == "usagestats":
            self.ui.tableWidget.setColumnCount(8)
            labels = ["","Usage Type","Last Time UTC","Time Active (milliseconds)","Package","Types","Classs","Source"]
            combolabels = labels[1:]
            self.ui.tableWidget.setHorizontalHeaderLabels(labels)
            self.ui.tableWidget.setHorizontalHeaderItem(0,self.headerItem)

            self.model = QtGui.QStandardItemModel(len(combolabels), 1)
            firstItem = QtGui.QStandardItem("---- Show/Hide Columns ----")
            firstItem.setBackground(QtGui.QBrush(QtGui.QColor(200, 200, 200)))
            firstItem.setSelectable(False)
            self.model.setItem(0, 0, firstItem)

            for i,label in enumerate(combolabels):
                item = QtGui.QStandardItem(label)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setData(QtCore.Qt.Checked, QtCore.Qt.CheckStateRole)
                self.model.setItem(i+1, 0, item)

            self.ui.comboBox.setModel(self.model)

            for record in data:
                if record[4] == '1':
                    type = 'Moved to Foreground'
                elif record[4] == '2':
                    type = 'Moved to Background'
                elif record[4] == '5':
                    type = 'Configuration Change'
                elif record[4] == '7':
                    type = 'User Interaction'
                elif record[4] == '8':
                    type = 'Shortcut Invocation'
                else:
                    type = record[4]


                unixtime = int(record[1])/1000
                timestamp = self.gettime((int(record[1])/1000)) #datetime.utcfromtimestamp(unixtime).strftime('%m-%d-%Y %H:%M:%S')
                self.chkBoxItem = QtWidgets.QTableWidgetItem()
                self.chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                self.chkBoxItem.setCheckState(QtCore.Qt.Checked)
                self.ui.tableWidget.insertRow(rowPosition)
                self.ui.tableWidget.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(self.chkBoxItem))
                self.ui.tableWidget.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(record[0]))
                self.ui.tableWidget.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(timestamp))
                self.ui.tableWidget.setItem(rowPosition , 3, QtWidgets.QTableWidgetItem(record[2]))
                self.ui.tableWidget.setItem(rowPosition , 4, QtWidgets.QTableWidgetItem(record[3]))
                self.ui.tableWidget.setItem(rowPosition , 5, QtWidgets.QTableWidgetItem(type))
                self.ui.tableWidget.setItem(rowPosition , 6, QtWidgets.QTableWidgetItem(record[5]))
                self.ui.tableWidget.setItem(rowPosition , 7, QtWidgets.QTableWidgetItem(record[6]))
                item = self.ui.tableWidget.item(rowPosition,0)
                currentState = item.checkState()
                self.currentstate.update({rowPosition:currentState})
                rowPosition += 1

            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(4,QtWidgets.QHeaderView.ResizeToContents)
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(5,QtWidgets.QHeaderView.ResizeToContents)



        elif self.filetype == "Recenttask":
            self.ui.tableWidget.setColumnCount(14)
            labels = ["","Task ID","Effective_uid","Affinity","Real Activity","First Active Time (UTC)","Last Active Time (UTC)","Last Time Moved (UTC)","Calling PAckage","User ID","Action","Component","Snap","Thumbnail Image"]
            combolabels = labels[1:]
            self.ui.tableWidget.setHorizontalHeaderLabels(labels)
            self.ui.tableWidget.setHorizontalHeaderItem(0,self.headerItem)
            self.model = QtGui.QStandardItemModel(len(combolabels), 1)
            firstItem = QtGui.QStandardItem("---- Show/Hide Columns ----")
            firstItem.setBackground(QtGui.QBrush(QtGui.QColor(200, 200, 200)))
            firstItem.setSelectable(False)
            self.model.setItem(0, 0, firstItem)

            for i,label in enumerate(combolabels):
                item = QtGui.QStandardItem(label)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setData(QtCore.Qt.Checked, QtCore.Qt.CheckStateRole)
                self.model.setItem(i+1, 0, item)

            self.ui.comboBox.setModel(self.model)

            for record in data:
                if record[11] == 'No Image':
                    image1 = "No Image"
                else:
                    image1 = QtWidgets.QLabel()
                    image1.setPixmap(QPixmap(record[11]).scaled(300,300,Qt.KeepAspectRatio))

                self.picturepath.update({f'{rowPosition}_12':record[11]})
                if record[12] == "No Image":
                    image = "No Image"
                else:
                    image = QtWidgets.QLabel()
                    image.setPixmap(QPixmap(record[12]).scaled(300,300,Qt.KeepAspectRatio))
                self.picturepath.update({f'{rowPosition}_13':record[12]})
                timestamp = self.gettime((int(record[4])/1000))
                timestamp1 = self.gettime((int(record[5])/1000))
                try:
                    timestamp2 = self.gettime((int(record[6])/1000))
                except:
                    timestamp2 = record[6]
                self.chkBoxItem = QtWidgets.QTableWidgetItem()
                self.chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                self.chkBoxItem.setCheckState(QtCore.Qt.Checked)
                self.ui.tableWidget.insertRow(rowPosition)
                self.ui.tableWidget.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(self.chkBoxItem))
                self.ui.tableWidget.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(record[0]))
                self.ui.tableWidget.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(record[1]))
                self.ui.tableWidget.setItem(rowPosition , 3, QtWidgets.QTableWidgetItem(record[2]))
                self.ui.tableWidget.setItem(rowPosition , 4, QtWidgets.QTableWidgetItem(record[3]))
                self.ui.tableWidget.setItem(rowPosition , 5, QtWidgets.QTableWidgetItem(timestamp))
                self.ui.tableWidget.setItem(rowPosition , 6, QtWidgets.QTableWidgetItem(timestamp1))
                self.ui.tableWidget.setItem(rowPosition , 7, QtWidgets.QTableWidgetItem(timestamp2))
                self.ui.tableWidget.setItem(rowPosition , 8, QtWidgets.QTableWidgetItem(record[7]))
                self.ui.tableWidget.setItem(rowPosition , 9, QtWidgets.QTableWidgetItem(record[8]))
                self.ui.tableWidget.setItem(rowPosition , 10, QtWidgets.QTableWidgetItem(record[9]))
                self.ui.tableWidget.setItem(rowPosition , 11, QtWidgets.QTableWidgetItem(record[10]))

                if record[11] == "No Image":
                    self.ui.tableWidget.setItem(rowPosition , 12, QtWidgets.QTableWidgetItem(record[11]))
                else:
                    self.ui.tableWidget.setCellWidget(rowPosition , 12, image1)

                if record[12] == "No Image":
                    self.ui.tableWidget.setItem(rowPosition , 13, QtWidgets.QTableWidgetItem(record[12]))
                else:
                    self.ui.tableWidget.setCellWidget(rowPosition , 13, image)

                item = self.ui.tableWidget.item(rowPosition,0)
                currentState = item.checkState()
                self.currentstate.update({rowPosition:currentState})
                rowPosition += 1

        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeToContents)
        self.ui.tableWidget.resizeRowsToContents()
        self.ui.tableWidget.cellChanged.connect(self.onCellChanged)
        self.ui.tableWidget.horizontalHeader().sectionClicked.connect(self.toggleCheckState)
        self.ui.comboBox.view().pressed.connect(self.handleItemPressed)
        self.ui.comboBox.view().clicked.connect(self.combocheckbox)
        self.ui.tableWidget.cellClicked.connect(self.bringupimage)
        self.changeicon()

    def bringupimage(self,row,column):
        if column == 12 or column == 13:
            try:
                os.startfile(self.picturepath[f'{row}_{column}'])
            except:
                pass

    def combocheckbox(self,index):
        item = self.model.itemFromIndex(index)
        if item.row() == 0:
            pass
        else:
            if item.checkState() == 0:
                self.ui.tableWidget.setColumnHidden(item.row(), True)
            elif item.checkState() == 2:
                self.ui.tableWidget.setColumnHidden(item.row(), False)


    def handleItemPressed(self,index):
        item = self.model.itemFromIndex(index)
        if item.row() == 0:
            pass
        else:
            if item.checkState() == 0:
                item.setData(QtCore.Qt.Checked, QtCore.Qt.CheckStateRole)
                self.ui.tableWidget.setColumnHidden(item.row(), False)
            elif item.checkState() == 2:
                item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
                self.ui.tableWidget.setColumnHidden(item.row(), True)


    def gettime(self,unixtime):
        return datetime.utcfromtimestamp(unixtime).strftime('%m-%d-%Y %H:%M:%S')

    def onCellChanged(self,row,column):
        item = self.ui.tableWidget.item(row, column)
        current = item.checkState()
        self.currentstate.update({row:current})
        self.changeicon()

    def changeicon(self):
        item1 = self.ui.tableWidget.item(0, 0).checkState()
        checked = set(list(self.currentstate.values()))
        if checked == {0}:
            self.tableicon = os.getcwd()+'/icons/unchecked.png'
            self.headerItem.setIcon(QtGui.QIcon(QtGui.QPixmap(self.tableicon)))
            self.ui.tableWidget.setHorizontalHeaderItem(0,self.headerItem)
        elif checked == {2}:
            self.tableicon = os.getcwd()+'/icons/checked.png'
            self.headerItem.setIcon(QtGui.QIcon(QtGui.QPixmap(self.tableicon)))
            self.ui.tableWidget.setHorizontalHeaderItem(0,self.headerItem)
        elif checked == {0,2}:
            self.tableicon = os.getcwd()+'/icons/intermediate.png'
            self.headerItem.setIcon(QtGui.QIcon(QtGui.QPixmap(self.tableicon)))
            self.ui.tableWidget.setHorizontalHeaderItem(0,self.headerItem)


    def toggleCheckState(self,index):
        if index == 0:
            if self.tableicon == os.getcwd()+'/icons/checked.png':
                for row in range(0,self.ui.tableWidget.rowCount()):
                    self.chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
                    self.ui.tableWidget.setItem(row , 0, QtWidgets.QTableWidgetItem(self.chkBoxItem))
                    self.currentstate.update({row:0})

            elif self.tableicon == os.getcwd()+'/icons/unchecked.png' or self.tableicon == os.getcwd()+'/icons/intermediate.png':
                for row in range(0,self.ui.tableWidget.rowCount()):
                    self.chkBoxItem.setCheckState(QtCore.Qt.Checked)
                    self.ui.tableWidget.setItem(row , 0, QtWidgets.QTableWidgetItem(self.chkBoxItem))
                    self.currentstate.update({row:2})


            self.changeicon()
        if index == 1:
            pass

    def create_html_report(self):
        self.report_info_window = QtWidgets.QWidget()
        self.reportwindow = Ui_ReportInfo()
        self.reportwindow.setupUi(self.report_info_window)
        self.report_info_window.show()
        self.reportwindow.lineEdit.setText(self.case_number)
        self.reportwindow.lineEdit_4.setText(self.evidence_number)
        self.reportwindow.lineEdit_3.setText(self.Investigator)
        self.reportwindow.lineEdit_2.setText(self.crime_code)
        self.reportwindow.lineEdit_6.setText(self.device_owner)
        self.reportwindow.buttonBox.accepted.connect(self.begin_report)

    def begin_report(self):

        try:
            Save_Location = os.path.expanduser('~')
            os.makedirs(f'{Save_Location}\\Documents\\US_RT Reports')
        except:
            pass

        if self.reportwindow.radioButton.isChecked() == True:
            self.checkvalue = [0,2]
        elif self.reportwindow.radioButton_2.isChecked() == True:
            self.checkvalue = [2]
        elif self.reportwindow.radioButton_3.isChecked() == True:
            self.checkvalue = [0]

        self.report_info_window.close()
        self.ui.statusbar.showMessage(f"Creating Report")
        self.run_thread2 = RunThread2()
        self.run_thread2.picturepath = self.picturepath
        self.run_thread2.checkvalue = self.checkvalue
        self.run_thread2.evidence_number = self.evidence_number
        self.run_thread2.device_owner = self.device_owner
        self.run_thread2.case_number = self.case_number
        self.run_thread2.Investigator = self.Investigator
        self.run_thread2.crime_code = self.crime_code
        self.run_thread2.table = self.ui.tableWidget
        self.run_thread2.type = self.filetype
        self.run_thread2.start()
        self.run_thread2.finished.connect(self.report_finished)

    def report_finished(self, finish_message):
        self.run_thread2.quit()
        self.ui.statusbar.showMessage(f"Report Finised")
        finished_dialog = QtWidgets.QMessageBox()
        finished_dialog.setIcon(QtWidgets.QMessageBox.Information)
        finished_dialog.setWindowTitle('Report Finished')
        finished_dialog.setText(f'Your report is located at \n {finish_message}')
        finished_dialog.setStandardButtons(QtWidgets.QMessageBox.Close)
        finished = finished_dialog.exec()
        if finished == QtWidgets.QMessageBox.Close:
            self.clear_statusbar(finish_message)

    def clear_statusbar(self,finish_message):
        self.ui.statusbar.showMessage(f"")
        os.startfile(finish_message)

if __name__ == "__main__":
    MainWindow_EXEC()
