import datetime
import json
import os
import subprocess
import sys
import re
from typing import List, Tuple
import dateutil.parser as parser
import pandas as pd
import xlrd
import qdarkstyle
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QPersistentModelIndex
from count_form import gen_form

import models

from PyQt5.QtWinExtras import QtWin

myappid = 'eb.forge-fell.helsing.alpha'
QtWin.setCurrentProcessExplicitAppUserModelID(myappid)


def set_defaults():
    default = {
        "CDB_Folder": r"\\aubrsisfile01\public\Aaron Penny\Data\CDB",
        "Short_Folder": r"\\aubrsisfile01\public\DCOperations\Restock\SHORT REPORT 1",
        "Dracula_Folder": r"\\aubrsisfile01\public\AusDCAdmin\Assigned Cycle Counts",
        "C_Form_Folder": r"\\aubrsisfile01\public\Aaron Penny\Restock\Helsing",
        "Style": "dark"
    }
    with open("Data\\Settings.json", 'w') as s:
        json.dump(default, s)


def update_settings(setting_name, new_setting):
    d = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(d, 'Data', 'Settings.json'), 'r') as s:
        settings = json.load(s)
    settings[setting_name] = new_setting
    with open(os.path.join(d, 'Data', 'Settings.json'), 'w') as s:
        json.dump(settings, s)


def get_setting(setting: str) -> str:
    d = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(d, 'Data', 'Settings.json'), 'r') as s:
        settings = json.load(s)
    return settings[setting]


def get_folder_dir(folder_name):
    d = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(d, 'Data', 'Settings.json'), 'r') as s:
        settings = json.load(s)
    if folder_name in settings:
        return settings[folder_name]
    else:
        return


def check_columns(df: pd.DataFrame(), columns: List[str]) -> Tuple[bool, list]:
    """
    Given a dataframe derived from Bin Contents, returns True if
    all the required columns are present, else; False.
    Also returns list of missing columns.
    :param df: Pandas Dataframe
    :param columns: List[str]
    :return: Tuple[bool, list]
    """
    missing = [c for c in columns if c not in df.columns]
    return len(missing) == 0, missing


def trim_columns(df: pd.DataFrame(), columns: List[str]) -> pd.DataFrame():
    """
    Takes a dataframe and removes columns not listed in the given columns list.
    :param df: Pandas Dataframe
    :param columns: List[Str]
    :return: None
    """
    superfluous = [c for c in df.columns if c not in columns]
    df = df.drop(columns=superfluous)
    return df


def set_style(style: str):
    d = os.path.dirname(os.path.abspath(__file__))
    app = QtCore.QCoreApplication.instance()
    app.setStyleSheet("")
    if style == 'dark':
        dark = qdarkstyle.load_stylesheet()
        app.setStyleSheet(dark)
    elif style in ['Fusion', 'Windows', 'WindowsVista']:
        app.setStyle(style)
    else:
        app.setStyleSheet(open(os.path.join(d, 'stylesheets', style)).read())

    update_settings("Style", style)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Get current settings
        d = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(d, 'ui', 'MainWindow.ui'), self)
        with open(os.path.join(d, 'Data', 'Settings.json'), 'r') as s:
            settings = json.load(s)

        self.setWindowTitle("Helsing")

        # Set column headers for different data types
        self.bc_cols = ['Zone Code', 'Bin Code', 'Item No.', 'Item Description', 'Quantity', 'Unit of Measure Code',
                        'Qty. (Base)', 'Pick Qty.', 'Available Qty.', 'Available Qty. (Base)', 'Put-away Qty.']
        self.shrep_cols = ['TimeStamp', 'Location', 'Req', 'Pic', 'Wave ID', 'Zone ID', 'SKU ID']
        self.drac_cols = ['Registering Date', 'Item No.', 'Zone Code', 'Bin Code']
        self.count_cols = ['Zone', 'Bin', 'Item', 'Qty Shorted', 'Qty Expected']

        # Keep a record of old short report files for deletion at an appropriate time
        self.old_shrep_files = []

        # Set folder string locations
        self.cdb_folder = settings["CDB_Folder"]
        self.shrep_folder = settings["Short_Folder"]
        self.drac_folder = settings["Dracula_Folder"]
        self.c_form_folder = settings["C_Form_Folder"]
        self.cdb_loc_lbl.setText("Central Database Location: " + self.cdb_folder)
        self.shrep_loc_lbl.setText("Short Report Folder Location: " + self.shrep_folder)
        self.drac_loc_lbl.setText("Dracula Location: " + self.drac_folder)
        self.rep_loc_lbl.setText("Count Report Location: " + self.c_form_folder)

        # Load button signals and slots
        self.update_shrep_btn.pressed.connect(lambda x="Short Report": self.update_folder(x))
        self.update_cdb_btn.pressed.connect(lambda x="CDB": self.update_folder(x))
        self.update_drac_btn.pressed.connect(lambda x="Dracula": self.update_folder(x))
        self.update_rep_btn.pressed.connect(lambda x="Report": self.update_folder(x))
        self.load_bc_btn.pressed.connect(self.get_bin_contents)
        self.load_shrep_btn.pressed.connect(self.get_short_reports)
        self.load_drac_btn.pressed.connect(self.get_drac_data)
        self.get_rep_btn.pressed.connect(self.gen_report)
        self.gen_form_btn.pressed.connect(self.get_printable_form)
        self.del_counts_btn.pressed.connect(self.remove_counts_from_shrep)
        self.del_counts_btn.setVisible(False)
        self.bind_styles()

        # Set Dataframes, Models, and Tables
        self.bc_df = pd.DataFrame()
        self.shrep_df = pd.DataFrame()
        self.drac_df = pd.DataFrame()
        self.count_df = pd.DataFrame()
        self.bc_model = models.PandasModel(pd.DataFrame())
        self.bc_table.setModel(self.bc_model)
        self.drac_model = models.PandasModel(pd.DataFrame())
        self.drac_table.setModel(self.drac_model)
        self.shrep_model = models.PandasModel(pd.DataFrame())
        self.shrep_table.setModel(self.shrep_model)
        self.count_model = models.PandasModel(pd.DataFrame())
        self.count_table.setModel(self.count_model)

        # Set all data automatically on open, if it is available.
        self.get_bin_contents(open_run=True)
        self.get_short_reports()
        self.get_drac_data()
        if not (self.bc_df.empty or self.shrep_df.empty or self.drac_df.empty):
            self.gen_report()

    def update_folder(self, setting):
        f_name = {"CDB": "CDB_Folder",
                  "Short Report": "Short_Folder",
                  "Dracula": "Dracula_Folder",
                  "Report": "C_Form_Folder"}[setting]
        open_folder = get_folder_dir(f_name)
        folder = QFileDialog.getExistingDirectory(self, "Select Folder for {}.".format(setting), directory=open_folder)
        if folder == "":
            return
        if setting == "Short Report":
            update_settings("Short_Folder", folder)
            self.shrep_folder = folder
        elif setting == "CDB":
            update_settings("CDB_Folder", folder)
            self.cdb_folder = folder
        elif setting == "Dracula":
            update_settings("Dracula_Folder", folder)
            self.drac_folder = folder
        elif setting == "Report":
            update_settings("C_Form_Folder", folder)
            self.c_form_folder = folder

        self.update_labels()

    def update_labels(self):
        self.cdb_loc_lbl.setText("Central Database Location: " + self.cdb_folder)
        self.shrep_loc_lbl.setText("Short Report Folder Location: " + self.shrep_folder)
        self.drac_loc_lbl.setText("Dracula Location: " + self.drac_folder)

    def get_bin_contents(self, open_run=False):
        try:
            self.bc_df = pd.read_clipboard()
            """ In case of data corruption, drop rows with nan values, 
            and cast Item and Pick columns to int data types."""
            self.bc_df.dropna(inplace=True)
            self.bc_df = self.bc_df.astype({'Item No.': int})
            self.bc_df = self.bc_df.astype({'Pick Qty.': int})
        except pd.errors.EmptyDataError:
            if not open_run:
                self.msg_box("Clipboard Data unreadable.")
            return

        has_columns, missing_cols = check_columns(self.bc_df, self.bc_cols)
        if has_columns:
            self.table_tabs.setCurrentIndex(0)
        else:
            if not open_run:
                msg = QMessageBox()
                msg.setText("There {col} missing from the given Bin Contents:\n".format(
                    col='are columns' if len(missing_cols) > 1 else 'is a column'))
                msg.setWindowTitle("Missing Column{s}".format(s='s' if len(missing_cols) > 1 else ''))
                msg.setDetailedText(str(missing_cols).strip('[]').replace("'", '').replace(", ", " | "))
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()
            self.bc_df = pd.DataFrame
            return

        self.bc_df = trim_columns(self.bc_df, self.bc_cols)
        self.bc_model = models.PandasModel(self.bc_df)
        self.bc_table.setModel(self.bc_model)

    def get_short_reports(self):
        fldr = self.shrep_folder
        self.shrep_df = pd.DataFrame()
        self.old_shrep_files = []
        for entry in os.scandir(fldr):
            if entry.path.endswith('.xls') and entry.is_file():
                wb = xlrd.open_workbook(os.path.abspath(entry.path), logfile=open(os.devnull, 'w'))
                df = pd.read_excel(wb)

            elif entry.path.endswith('.csv') and entry.is_file():
                df = pd.read_csv(os.path.abspath(entry.path))
            else:
                df = pd.DataFrame()

            if check_columns(df, self.shrep_cols)[0]:
                if entry.name != 'helsing_short_lines.csv':
                    self.old_shrep_files.append(entry.path)
                self.shrep_df = pd.concat([self.shrep_df, df])

        self.shrep_df = trim_columns(self.shrep_df, self.shrep_cols)
        self.shrep_df.drop_duplicates(inplace=True, ignore_index=True)
        self.shrep_df = self.shrep_df.sort_values(by=['SKU ID'])
        self.shrep_df.reset_index(drop=True, inplace=True)
        self.shrep_df['TimeStamp'] = [sanitize_date_type(d) for d in self.shrep_df['TimeStamp']]
        self.shrep_model = models.PandasModel(self.shrep_df)
        self.shrep_table.setModel(self.shrep_model)
        if not self.shrep_df.empty:
            self.table_tabs.setCurrentIndex(1)

    def get_drac_data(self):
        fldr = self.drac_folder
        self.drac_df = pd.DataFrame()
        for entry in os.scandir(fldr):
            if re.match(".*(Dracula).*(.xlsm)", entry.name) and entry.is_file() and entry.name[:2] != '~$':
                df = pd.read_excel(os.path.abspath(entry.path), 'Approved Variances')
                if check_columns(df, self.drac_cols)[0]:
                    frames = [self.drac_df, df]
                    self.drac_df = pd.concat(frames)

        self.drac_df = self.drac_df.dropna(subset=['Item No.'])
        self.drac_df = trim_columns(self.drac_df, self.drac_cols)
        self.drac_df.reset_index(drop=True, inplace=True)
        self.drac_df['Registering Date'] = [sanitize_date_type(d) for d in self.drac_df['Registering Date']]
        self.drac_df['Item No.'] = [int(s) for s in self.drac_df['Item No.']]
        self.drac_df = self.drac_df[
            [x in ['PK', 'SP PK', 'BLK PK', 'PO PK', 'BLK PO', 'SUP PK'] for x in self.drac_df['Zone Code']]]

        self.drac_model = models.PandasModel(self.drac_df)
        self.drac_table.setModel(self.drac_model)
        if not self.drac_df.empty:
            self.table_tabs.setCurrentIndex(2)

    def gen_report(self):
        if self.bc_df.empty or self.shrep_df.empty or self.drac_df.empty:
            self.msg_box("Missing Data: Cannot continue.")
            return

        self.shrep_df['Short'] = self.shrep_df['Req'] - self.shrep_df['Pic']
        self.drop_shrep_lines()
        df = trim_columns(self.bc_df, ['Zone Code', 'Bin Code', 'Item No.',
                                       'Item Description', 'Pick Qty.', 'Available Qty.'])
        # Convert pick qty to numeric to ensure conditional evaluates accurately.
        df['Pick Qty.'] = pd.to_numeric(df['Pick Qty.'].astype(str).str.replace(',', ''), errors='coerce')
        df = df[df['Pick Qty.'] == 0]  # Get only lines that aren't currently picking.
        # Remove anything not on the short list.
        if not df.empty:
            df = df[[sku in self.shrep_df['SKU ID'].values for sku in df['Item No.']]]
        if not df.empty:
            df['Qty Shorted'] = [self.get_short_qty(sku) for sku in df['Item No.']]  # Get the shorted qty column.

        df.reset_index(drop=True, inplace=True)
        self.del_counts_btn.setVisible(False)
        self.count_df = df
        self.count_model = models.PandasModel(self.count_df)
        self.count_table.setModel(self.count_model)
        self.table_tabs.setCurrentIndex(3)

    def get_printable_form(self):
        if self.count_df.empty:
            self.msg_box("Nothing to print.")
            return
        file = gen_form(get_folder_dir("C_Form_Folder"), self.count_df)
        subprocess.Popen([file], shell=True)
        self.del_counts_btn.setVisible(True)

    def drop_shrep_lines(self):
        self.shrep_df = self.shrep_df[[self.short_after_count(sku, timestamp) for sku, timestamp in
                                       zip(self.shrep_df['SKU ID'], self.shrep_df['TimeStamp'])]]
        self.shrep_df.reset_index(drop=True, inplace=True)
        self.shrep_model = models.PandasModel(self.shrep_df)
        self.shrep_table.setModel(self.shrep_model)
        self.replace_old_shrep_files()

    def replace_old_shrep_files(self):
        self.shrep_df.to_csv(os.path.join(get_folder_dir('Short_Folder'), 'helsing_short_lines.csv'), index=False)
        perr = []
        fnfe = []
        for file in self.old_shrep_files:
            try:
                os.remove(file)
            except PermissionError:
                perr.append(file)
            except FileNotFoundError:
                fnfe.append(file)
        self.old_shrep_files = []
        if len(perr) > 0:
            self.msg_box("Permission Error - Couldn't delete: \n" + '\n'.join(perr))
        if len(fnfe) > 0:
            self.msg_box("File Not Found: \n" + '\n'.join(fnfe))

    def remove_counts_from_shrep(self):
        self.shrep_df = self.shrep_df[
            [sku not in self.count_df['Item No.'].values for sku in self.shrep_df['SKU ID']]]
        self.shrep_df.reset_index(drop=True, inplace=True)
        self.shrep_df.to_csv(os.path.join(get_folder_dir('Short_Folder'), 'helsing_short_lines.csv'), index=False)
        self.shrep_model = models.PandasModel(self.shrep_df)
        self.shrep_table.setModel(self.shrep_model)
        self.gen_report()

    def short_after_count(self, sku: int, timestamp: datetime.datetime) -> bool:
        """
        Given the values for the sku and time from the short reports, returns true
        if the last count date in dracula comes before this short pick timestamp.
        :param timestamp: Time of short pick.
        :param sku: sku id for ite,
        :return:
        """
        dr_df = self.drac_df
        if sku not in dr_df['Item No.'].values:
            last_count = datetime.datetime(1970, 1, 1)
        else:
            last_count = dr_df[dr_df['Item No.'] == sku]['Registering Date'].max()
        return timestamp >= last_count

    def get_short_qty(self, sku: int) -> int:
        """
        Gets the total shorted quantity for the given sku.
        :param sku: Item Number
        :return: Total quantity shorted for the given sku.
        """
        df = self.shrep_df
        return df[df['SKU ID'] == sku]['Short'].sum()

    def delete(self):
        if self.count_table.selectionModel().hasSelection():
            indexes = [QPersistentModelIndex(index) for index in self.count_table.selectionModel().selectedRows()]
            ind = [i.row() for i in indexes]
            self.count_df = self.count_df.drop(ind, axis=0)
            self.count_df.reset_index(drop=True, inplace=True)
            self.count_model = models.PandasEditableModel(self.count_df)
            self.count_table.setModel(self.count_model)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Backspace, Qt.Key_Delete):
            self.delete()
        QMainWindow.keyPressEvent(self, event)

    @staticmethod
    def success_box():
        scs = QMessageBox()
        scs.setText("Success!")
        scs.setStyleSheet("QLabel{min-width: 100px;}")
        scs.setStandardButtons(QMessageBox.Ok)
        scs.exec()

    @staticmethod
    def msg_box(msg: str):
        box = QMessageBox()
        box.setWindowTitle("Helsing")
        box.setText(msg)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec()

    def bind_styles(self):
        self.actionTrue_Green.triggered.connect(lambda: set_style("green_stuff.css"))
        self.actionGreen_Y.triggered.connect(lambda: set_style("green_stuff_y.css"))
        self.actionGreen_C.triggered.connect(lambda: set_style("green_stuff_c.css"))
        self.actionTrue_Red.triggered.connect(lambda: set_style("red_things.css"))
        self.actionRed_Y.triggered.connect(lambda: set_style("red_things_y.css"))
        self.actionRed_M.triggered.connect(lambda: set_style("red_things_m.css"))
        self.actionTrue_Blue.triggered.connect(lambda: set_style("blue_misc.css"))
        self.actionBlue_C.triggered.connect(lambda: set_style("blue_misc_c.css"))
        self.actionBlue_M.triggered.connect(lambda: set_style("blue_misc_m.css"))
        self.actionCstartpage.triggered.connect(lambda: set_style("Cstartpage.qss"))
        self.actionDiffnes.triggered.connect(lambda: set_style("Diffnes.qss"))
        self.actionFibers.triggered.connect(lambda: set_style("Fibers.qss"))
        self.actionFibrary.triggered.connect(lambda: set_style("Fibrary.qss"))
        self.actionGenetive.triggered.connect(lambda: set_style("Genetive.qss"))
        self.actionIncrypt.triggered.connect(lambda: set_style("Incrypt.qss"))
        self.actionIrrorater.triggered.connect(lambda: set_style("Irrorater.qss"))
        self.actionObit.triggered.connect(lambda: set_style("Obit.qss"))
        self.actionRemover.triggered.connect(lambda: set_style("Remover.qss"))
        self.actionSyNet.triggered.connect(lambda: set_style("SyNet.qss"))
        self.actionVisualScript.triggered.connect(lambda: set_style("VisualScript.qss"))
        self.actionDark_blue.triggered.connect(lambda: set_style("dark_blue.css"))
        self.actionDark_teal.triggered.connect(lambda: set_style("dark_teal.css"))
        self.actionDark_magenta.triggered.connect(lambda: set_style("dark_magenta.css"))
        self.actionDark_purple.triggered.connect(lambda: set_style("dark_purple.css"))
        self.actionDark_yellowGreen.triggered.connect(lambda: set_style("dark_yellowGreen.css"))
        self.actionDark_orange.triggered.connect(lambda: set_style("dark_orange.css"))
        self.actionDark_darkBlue.triggered.connect(lambda: set_style("dark_darkBlue.css"))
        self.actionDark_strongBlue.triggered.connect(lambda: set_style("dark_strongBlue.css"))
        self.actionDark_lilac.triggered.connect(lambda: set_style("dark_lilac.css"))
        self.actionDark_yellow.triggered.connect(lambda: set_style("dark_yellow.css"))
        self.actionDark_cornsilk.triggered.connect(lambda: set_style("dark_cornsilk.css"))
        self.actionDark_darkRed.triggered.connect(lambda: set_style("dark_darkRed.css"))
        self.actionDark_red.triggered.connect(lambda: set_style("dark_red.css"))
        self.actionDark_pink.triggered.connect(lambda: set_style("dark_pink.css"))
        self.actionDark_turquoise.triggered.connect(lambda: set_style("dark_turquoise.css"))
        self.actionDark_cyan.triggered.connect(lambda: set_style("dark_cyan.css"))
        self.actionDark_powderBlue.triggered.connect(lambda: set_style("dark_powderBlue.css"))
        self.actionDark_green.triggered.connect(lambda: set_style("dark_green.css"))
        self.actionDark_limeGreen.triggered.connect(lambda: set_style("dark_limeGreen.css"))
        self.actionDark_paleGreen.triggered.connect(lambda: set_style("dark_paleGreen.css"))
        self.actionDark_darkViolet.triggered.connect(lambda: set_style("dark_darkViolet.css"))
        self.actionDark_fuchsia.triggered.connect(lambda: set_style("dark_fuchsia.css"))
        self.actionDark_plum.triggered.connect(lambda: set_style("dark_plum.css"))
        self.actionDark_goldenrod.triggered.connect(lambda: set_style("dark_goldenrod.css"))
        self.actionFusion.triggered.connect(lambda: set_style("Fusion"))
        self.actionWindows.triggered.connect(lambda: set_style("Windows"))
        self.actionWindowsVista.triggered.connect(lambda: set_style("WindowsVista"))


def sanitize_date_type(d: any) -> datetime.datetime:
    """
    converts to datetime where possible.
    :param d:
    :return: datetime object
    """
    if type(d) is int:
        return datetime.datetime(1899, 12, 31) + datetime.timedelta(days=d)
    elif isinstance(d, datetime.datetime):
        return d
    elif type(d) is str:
        return parser.parse(d)
    elif type(d) is datetime.datetime.timestamp:
        return datetime.datetime.fromtimestamp(d)


def main():
    app = QApplication(sys.argv)
    d = os.path.dirname(os.path.abspath(__file__))
    app.setWindowIcon(QtGui.QIcon(os.path.join(d, 'ico', 'hellsing.ico')))
    app.setStyle('Fusion')
    set_style(get_setting("Style"))
    w = MainWindow()
    w.showMaximized()
    app.exec()


if __name__ == '__main__':
    main()
