class Signal:
    """
    Fake Signal class to which provides the same method as the QSignal class.
    Used if QT5 is not used in case only the terminal function is used.
    Use those weird name because of https://bugreports.qt.io/browse/PYSIDE-1264.
    """
    def s_connect(self, callback):
        pass

    def s_disconnect(self):
        pass

    def s_emit(self, idx: int):
        pass
