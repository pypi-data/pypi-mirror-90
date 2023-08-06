import os.path as osp
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class ViewWidget(QDockWidget):

    ITEM_COLOR_OK = QBrush(QColor(255, 255, 255))
    ITEM_COLOR_NG = QBrush(QColor(255, 255, 0))

    def __init__(self, parent=None, title=''):
        super(ViewWidget, self).__init__(title, parent)

        self.viewListWidget = QListWidget()
        self.viewlistLayout = QVBoxLayout()
        self.viewlistLayout.setContentsMargins(0, 0, 0, 0)
        self.viewlistLayout.addWidget(self.viewListWidget)
        self.viewWidgetContainer = QWidget()
        self.viewWidgetContainer.setLayout(self.viewlistLayout)
        self.setObjectName('View')
        self.setWidget(self.viewWidgetContainer)
        self.setFeatures(QDockWidget.DockWidgetFloatable)

    def itemClicked_connect(self, f):
        self.viewListWidget.itemClicked.connect(f)

    def initialize_item(self, matching):
        views = matching.get_views()
        self.viewListWidget.clear()
        for view in views:
            self.viewListWidget.addItem(self.item_text(view))

    def count(self):
        return self.viewListWidget.count()

    def get_current_idx(self):
        return self.viewListWidget.currentIndex().row()

    def set_current_idx(self, idx):
        self.viewListWidget.setCurrentRow(idx)

    def update_item_by_idx(self, matching, idx):
        views = matching.get_views()
        if type(idx) in (list, tuple):
            for i in idx:
                self.viewListWidget.item(i).setText(self.item_text(views[i]))
        else:
            self.viewListWidget.item(idx).setText(self.item_text(views[idx]))

    def apply_bad_keypoints(self, bad_keypoints):
        bad_view_idxs = [x[0] for x in bad_keypoints]
        for idx in range(self.count()):
            if idx in bad_view_idxs:
                self.viewListWidget.item(idx).setBackground(self.ITEM_COLOR_NG)
            else:
                self.viewListWidget.item(idx).setBackground(self.ITEM_COLOR_OK)

    @staticmethod
    def item_text(view):
        return '(ID={}, K={}) {}'.format(
            view['id_view'],
            len(view['keypoints']),
            osp.join(*view['filename']))
