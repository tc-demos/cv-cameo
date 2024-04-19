import cv2

import filters
from managers import WindowManager, CaptureManager


class Cameo(object):
    def __init__(self):
        self._windowManager = WindowManager('Cameo', self.onKeyPress)
        self._captureManager = CaptureManager(cv2.VideoCapture(0), self._windowManager, True)

        self._LFilters = [{"title": "No filtering", "filter": None}]

        self._sharpenFilter = filters.SharpenFilter()
        self._LFilters.append({"title": "Sharpen", "filter": self._sharpenFilter})

        self._findEdgesFilter = filters.FindEdgesFilter()
        self._LFilters.append({"title": "Find edges", "filter": self._findEdgesFilter})

        self._blurFilter = filters.BlurFilter()
        self._LFilters.append({"title": "Blur", "filter": self._blurFilter})

        self._embossFilter = filters.EmbossFilter()
        self._LFilters.append({"title": "Emboss", "filter": self._embossFilter})



    def run(self, choice):
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            if frame is not None:
                if choice == 0:
                    pass
                elif 0 < choice <= len(self._LFilters):
                    self._LFilters[choice]["filter"].apply(frame, frame)
                elif choice == len(self._LFilters):
                    filters.enhanceEdges(frame, frame)
                else:
                    pass

            self._captureManager.exitFrame()
            self._windowManager.processEvents()

    def onKeyPress(self, keycode):
        if keycode == 32:
            self._captureManager.writeImage('screenshot_{index}.png')
        elif keycode == 9:
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo('screencast.avi')
            else:
                self._captureManager.stopWritingVideo()
        elif keycode == 27:
            self._windowManager.destroyWindow()


def main():
    cam = Cameo()
    while True:
        print("Space: screenshot\nTab: start-stop screencast\nEscape: exit")

        for i, f in enumerate(cam._LFilters):
            print(f"{i}: {f['title']}")

        idx = input(len(cam._LFilters))
        print(idx, "Enhance edges")

        print()

        choice = -2
        while choice < -1 or choice > len(cam._LFilters):
            choice = int(input("Choose a filter: "))
        print()

        if choice > -1:
            cam.run(choice)
            ans = input("Another? (y/n): ")
        else:
            break



if __name__ == '__main__':
    main()