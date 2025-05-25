# This Python file uses the following encoding: utf-8
from colorsys import rgb_to_hls, hls_to_rgb
from PySide6.QtWidgets import QWidget, QStyleOption
from PySide6.QtGui import QPainter
from PySide6.QtCore import QSize, QByteArray, QRectF, Property
from PySide6.QtCore import Signal
from PySide6.QtSvg import QSvgRenderer


class QLed(QWidget):
    Circle = 1

    Red = 1
    Green = 2
    Yellow = 3
    Grey = 4
    Orange = 5
    Purple = 6
    Blue = 7

    shapes = {
        Circle: """
            <svg height="50.000000px" id="svg9493" width="50.000000px" xmlns="http://www.w3.org/2000/svg">
              <defs id="defs9495">
                <linearGradient gradientUnits="userSpaceOnUse" id="linearGradient6650" x1="23.402565" x2="23.389874" xlink:href="#linearGradient6506" y1="44.066776" y2="42.883698"/>
                <linearGradient id="linearGradient6494">
                  <stop id="stop6496" offset="0.0000000" style="stop-color:%s;stop-opacity:1.0000000;"/>
                  <stop id="stop6498" offset="1.0000000" style="stop-color:%s;stop-opacity:1.0000000;"/>
                </linearGradient>
                <linearGradient gradientUnits="userSpaceOnUse" id="linearGradient6648" x1="23.213980" x2="23.201290" xlink:href="#linearGradient6494" y1="42.754631" y2="43.892632"/>
                <linearGradient gradientUnits="userSpaceOnUse" id="linearGradient6646" x1="23.349695" x2="23.440580" xlink:href="#linearGradient5756" y1="42.767944" y2="43.710873"/>
                <linearGradient gradientUnits="userSpaceOnUse" id="linearGradient6644" x1="23.193102" x2="23.200001" xlink:href="#linearGradient5742" y1="42.429230" y2="44.000000"/>
                <linearGradient id="linearGradient6506">
                  <stop id="stop6508" offset="0.0000000" style="stop-color:#ffffff;stop-opacity:0.0000000;"/>
                  <stop id="stop6510" offset="1.0000000" style="stop-color:#ffffff;stop-opacity:0.87450981;"/>
                </linearGradient>
                <linearGradient gradientUnits="userSpaceOnUse" id="linearGradient7498" x1="23.402565" x2="23.389874" xlink:href="#linearGradient6506" y1="44.066776" y2="42.883698"/>
                <linearGradient id="linearGradient7464">
                  <stop id="stop7466" offset="0.0000000" style="stop-color:#00039a;stop-opacity:1.0000000;"/>
                  <stop id="stop7468" offset="1.0000000" style="stop-color:#afa5ff;stop-opacity:1.0000000;"/>
                </linearGradient>
                <linearGradient gradientUnits="userSpaceOnUse" id="linearGradient7496" x1="23.213980" x2="23.201290" xlink:href="#linearGradient7464" y1="42.754631" y2="43.892632"/>
                <linearGradient id="linearGradient5756">
                  <stop id="stop5758" offset="0.0000000" style="stop-color:#828282;stop-opacity:1.0000000;"/>
                  <stop id="stop5760" offset="1.0000000" style="stop-color:#929292;stop-opacity:0.35294119;"/>
                </linearGradient>
                <linearGradient gradientUnits="userSpaceOnUse" id="linearGradient9321" x1="22.935030" x2="23.662106" xlink:href="#linearGradient5756" y1="42.699776" y2="43.892632"/>
                <linearGradient id="linearGradient5742">
                  <stop id="stop5744" offset="0.0000000" style="stop-color:#adadad;stop-opacity:1.0000000;"/>
                  <stop id="stop5746" offset="1.0000000" style="stop-color:#f0f0f0;stop-opacity:1.0000000;"/>
                </linearGradient>
                <linearGradient gradientUnits="userSpaceOnUse" id="linearGradient7492" x1="23.193102" x2="23.200001" xlink:href="#linearGradient5742" y1="42.429230" y2="44.000000"/>
                <linearGradient gradientUnits="userSpaceOnUse" id="linearGradient9527" x1="23.193102" x2="23.200001" xlink:href="#linearGradient5742" y1="42.429230" y2="44.000000"/>
                <linearGradient gradientUnits="userSpaceOnUse" id="linearGradient9529" x1="22.935030" x2="23.662106" xlink:href="#linearGradient5756" y1="42.699776" y2="43.892632"/>
                <linearGradient gradientUnits="userSpaceOnUse" id="linearGradient9531" x1="23.213980" x2="23.201290" xlink:href="#linearGradient7464" y1="42.754631" y2="43.892632"/>
                <linearGradient gradientUnits="userSpaceOnUse" id="linearGradient9533" x1="23.402565" x2="23.389874" xlink:href="#linearGradient6506" y1="44.066776" y2="42.883698"/>
              </defs>
              <g id="layer1">
                <g id="g9447" style="overflow:visible" transform="matrix(31.25000,0.000000,0.000000,31.25000,-625.0232,-1325.000)">
                  <path d="M 24.000001,43.200001 C 24.000001,43.641601 23.641601,44.000001 23.200001,44.000001 C 22.758401,44.000001 22.400001,43.641601 22.400001,43.200001 C 22.400001,42.758401 22.758401,42.400001 23.200001,42.400001 C 23.641601,42.400001 24.000001,42.758401 24.000001,43.200001 z " id="path6596" style="fill:url(#linearGradient6644);fill-opacity:1.0000000;stroke:none;stroke-width:0.80000001;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4.0000000;stroke-opacity:1.0000000;overflow:visible" transform="translate(-2.399258,-1.000000e-6)"/>
                  <path d="M 23.906358,43.296204 C 23.906358,43.625433 23.639158,43.892633 23.309929,43.892633 C 22.980700,43.892633 22.713500,43.625433 22.713500,43.296204 C 22.713500,42.966975 22.980700,42.699774 23.309929,42.699774 C 23.639158,42.699774 23.906358,42.966975 23.906358,43.296204 z " id="path6598" style="fill:url(#linearGradient6646);fill-opacity:1.0000000;stroke:none;stroke-width:0.80000001;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4.0000000;stroke-opacity:1.0000000;overflow:visible" transform="matrix(1.082474,0.000000,0.000000,1.082474,-4.431649,-3.667015)"/>
                  <path d="M 23.906358,43.296204 C 23.906358,43.625433 23.639158,43.892633 23.309929,43.892633 C 22.980700,43.892633 22.713500,43.625433 22.713500,43.296204 C 22.713500,42.966975 22.980700,42.699774 23.309929,42.699774 C 23.639158,42.699774 23.906358,42.966975 23.906358,43.296204 z " id="path6600" style="fill:url(#linearGradient6648);fill-opacity:1.0000000;stroke:none;stroke-width:0.80000001;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4.0000000;stroke-opacity:1.0000000;overflow:visible" transform="matrix(0.969072,0.000000,0.000000,0.969072,-1.788256,1.242861)"/>
                  <path d="M 23.906358,43.296204 C 23.906358,43.625433 23.639158,43.892633 23.309929,43.892633 C 22.980700,43.892633 22.713500,43.625433 22.713500,43.296204 C 22.713500,42.966975 22.980700,42.699774 23.309929,42.699774 C 23.639158,42.699774 23.906358,42.966975 23.906358,43.296204 z " id="path6602" style="fill:url(#linearGradient6650);fill-opacity:1.0000000;stroke:none;stroke-width:0.80000001;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4.0000000;stroke-opacity:1.0000000;overflow:visible" transform="matrix(0.773196,0.000000,0.000000,0.597938,2.776856,17.11876)"/>
                </g>
              </g>
            </svg>
        """
    }

    colours = {Red: (0xCF, 0x00, 0x00),
            Green: (0x0f, 0x69, 0x00),
            Yellow: (0xd2, 0xcd, 0x00),
            Grey: (0x5a, 0x5a, 0x5a),
            Orange: (0xda, 0x46, 0x15),
            Purple: (0x87, 0x00, 0x83),
            Blue: (0x00, 0x03, 0x9a)}

    clicked = Signal()
    pressed = Signal(bool)

    def __init__(self, parent=None, **kwargs):
        self.m_value = False
        self.m_onColour = QLed.Red
        self.m_offColour = QLed.Grey
        self.m_shape = QLed.Circle
        self.m_clickable = False

        QWidget.__init__(self, parent, **kwargs)

        self._pressed = False
        self.renderer = QSvgRenderer()

    def value(self): return self.m_value

    def setValue(self, value):
        self.m_value = value
        self.update()
    value = Property(bool, value, setValue)

    def onColour(self): return self.m_onColour

    def setOnColour(self, newColour):
        self.m_onColour = newColour
        self.update()
    onColour = Property(int, onColour, setOnColour)

    def offColour(self): return self.m_offColour

    def setOffColour(self, newColour):
        self.m_offColour = newColour
        self.update()
    offColour = Property(int, offColour, setOffColour)

    def shape(self): return self.m_shape

    def setShape(self, newShape):
        self.m_shape = newShape
        self.update()
    shape = Property(int, shape, setShape)

    def clickable(self): return self.m_clickable

    def setClickable(self, newClickability):
        self.m_clickable = newClickability
    clickable = Property(bool, clickable, setClickable)

    def sizeHint(self):
        return QSize(48, 48)

    def adjust(self, r, g, b):
        def normalise(x): return x/255.0
        def denormalise(x): return int(x*255.0)

        (h, l, s) = rgb_to_hls(normalise(r), normalise(g), normalise(b))
        (nr, ng, nb) = hls_to_rgb(h, l*1.5, s)

        return (denormalise(nr), denormalise(ng), denormalise(nb))

    def paintEvent(self, event):
        option = QStyleOption()
        option.initFrom(self)

        h = option.rect.height()
        w = option.rect.width()

        size = min(w, h)
        x = abs(size-w)/2.0
        y = abs(size-h)/2.0
        bounds = QRectF(x, y, size, size)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        (dark_r, dark_g, dark_b) = self.colours[self.m_onColour if self.m_value else self.m_offColour]

        dark_str = "rgb(%d,%d,%d)" % (dark_r, dark_g, dark_b)
        light_str = "rgb(%d,%d,%d)" % self.adjust(dark_r, dark_g, dark_b)

        __xml = (self.shapes[self.m_shape] % (dark_str, light_str)).encode('utf8')
        self.renderer.load(QByteArray(__xml))
        self.renderer.render(painter, bounds)

    def mousePressEvent(self, event):
        self._pressed = True
        QWidget.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self._pressed:
            self._pressed = False
            if self.m_clickable:
                self.toggleValue()
                self.pressed.emit(self.m_value)
            else:
                self.pressed.emit(True)
            self.clicked.emit()

        QWidget.mouseReleaseEvent(self, event)

    def toggleValue(self):
        self.m_value = not self.m_value
        self.update()