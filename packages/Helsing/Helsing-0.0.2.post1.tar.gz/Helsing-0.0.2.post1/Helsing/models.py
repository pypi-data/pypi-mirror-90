from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
import typing
import pandas as pd


class PandasModel(QAbstractTableModel):
    """
    Model for Bin Contents Data
    _data: DataFrame
    """

    def __init__(self, data: pd.DataFrame()):
        """Bin Contents Model Initializer"""
        super(PandasModel, self).__init__()
        self._data = data

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self._data.shape[0]

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return self._data.shape[1]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class PandasEditableModel(QAbstractTableModel):
    """
    Model for Bin Contents Data
    _data: DataFrame
    """

    def __init__(self, data: pd.DataFrame()):
        """Bin Contents Model Initializer"""
        super(PandasEditableModel, self).__init__()
        self._data = data

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self._data.shape[0]

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return self._data.shape[1]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if role == Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            return True

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
