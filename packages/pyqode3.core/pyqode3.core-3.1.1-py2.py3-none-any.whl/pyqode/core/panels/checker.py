"""
Checker panels:

    - CheckerPanel: draw checker messages in front of each line
    - GlobalCheckerPanel: draw all checker markers as colored rectangle to
      offer a global view of all errors
"""
from pyqode.core.api import DelayJobRunner, TextHelper
from pyqode.core.api.panel import Panel
from pyqode.qt import QtCore, QtGui, QtWidgets


class CheckerPanel(Panel):
    """ Shows messages collected by one or more checker modes """

    _use_syntax_theme = True

    def __init__(self):
        super(CheckerPanel, self).__init__()
        self._previous_line = -1
        self.scrollable = True
        self._job_runner = DelayJobRunner(delay=100)
        self.setMouseTracking(True)
    
    def marker_for_line(self, line):
        """
        Returns the marker that is displayed at the specified line number if
        any.

        :param line: The marker line.

        :return: Marker of None
        :rtype: pyqode.core.Marker
        """
        block = self.editor.document().findBlockByNumber(line)
        try:
            messages = block.userData().messages
        except AttributeError:
            return []
        return [msg for msg in messages if msg.show_on_panel(self)]

    def sizeHint(self):
        """
        Returns the panel size hint. (fixed with of 16px)
        """
        metrics = QtGui.QFontMetricsF(self.editor.font())
        size_hint = QtCore.QSize(metrics.height(), metrics.height())
        if size_hint.width() > 16:
            size_hint.setWidth(16)
        return size_hint

    def on_uninstall(self):
        self._job_runner.cancel_requests()
        super(CheckerPanel, self).on_uninstall()

    def paintEvent(self, event):
        super(CheckerPanel, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        message_count = 0
        for top, block_nbr, block in self.editor.visible_blocks:
            user_data = block.userData()
            if not user_data or not user_data.messages:
                continue
            for msg in user_data.messages:
                if not msg.show_on_panel(self):
                    continue
                icon = msg.icon()
                if not icon:
                    continue
                rect = QtCore.QRect()
                rect.setX(0)
                rect.setY(top)
                rect.setSize(icon.actualSize(self.sizeHint()))
                icon.paint(painter, rect)
                message_count += 1
        self._message_count(message_count)

    def mouseMoveEvent(self, event):
        # Requests a tooltip if the cursor is currently over a marker.
        line = TextHelper(self.editor).line_nbr_from_position(event.pos().y())
        if line < 0:
            return
        markers = self.marker_for_line(line)
        if markers:
            tooltips = [marker.tooltip() for marker in markers]
            if self._previous_line != line:
                ypos = TextHelper(self.editor).line_pos_from_number(
                    markers[0].line
                )
                self._job_runner.request_job(
                    self._display_tooltip,
                    '<br />\n'.join(tooltips),
                    ypos
                )
        else:
            self._job_runner.cancel_requests()
        self._previous_line = line
        
    def mousePressEvent(self, event):
        line = TextHelper(self.editor).line_nbr_from_position(event.pos().y())
        if line < 0:
            return
        for marker in self.marker_for_line(line):
            marker.clicked(event) 

    def leaveEvent(self, *args):
        """
        Hide tooltip when leaving the panel region.
        """
        QtWidgets.QToolTip.hideText()
        self._previous_line = -1

    def _display_tooltip(self, tooltip, top):
        """
        Display tooltip at the specified top position.
        """
        QtWidgets.QToolTip.showText(self.mapToGlobal(QtCore.QPoint(
            self.sizeHint().width(), top)), tooltip, self)

    def _message_count(self, n):
        pass
