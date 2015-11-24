import re
from PyQt4.QtGui import QTextEdit, QColor, QTextCharFormat, QSyntaxHighlighter, QFont, QFontMetrics

def format(color, style=''):
    """Converts simple color/style pair int QTextCharFormat
    """
    color_ = QColor()
    color_.setNamedColor(color)

    format_ = QTextCharFormat()
    format_.setForeground(color_)
    if 'bold' in style:
        format_.setFontWeight(QFont.Bold)
    if 'italic' in style:
        format_.setFontItalic(True)

    return format_

STYLES = {
    'tag': format('blue'),
    'comment': format('green', 'italic'),
    'quote': format('brown'),
}

class XmlHighlighter(QSyntaxHighlighter):
    """Implements text edit widget with XML highlighting. Only simplified
       syntax is distinguished. No multiline support.
    """

    def __init__(self, document):
        """Defines rules for highliting
        """
        super().__init__(document)

        rules = [
            (STYLES['tag'], '<.*?>'),
            (STYLES['comment'], '<!--.*?-->'),
            (STYLES['quote'], '\\".*?\\"'),
        ]

        self.rules = [(fmt, re.compile(pat)) for (fmt, pat) in rules]

    def highlightBlock(self, text):
        """Called for each line that has been changed.
        """
        for format_, expression in self.rules:
            match = expression.search(text, 0)
            while match:
                start, stop = match.span()
                self.setFormat(start, stop-start, format_)
                match = expression.search(text, stop)

        self.setCurrentBlockState(0)
        
class XmlEditor(QTextEdit):
    def __init__(self):
        """Configures all the properties.
        """
        super().__init__()
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        metrics = QFontMetrics(font)
        self.setFont(font)
        self.setTabStopWidth(2 * metrics.width(' '))       
        self.highlighter = XmlHighlighter(self.document())
