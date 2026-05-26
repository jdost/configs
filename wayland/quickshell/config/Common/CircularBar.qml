import QtQml
import QtQuick
import QtQuick.Shapes
import qs

Shape {
    id: base

    enum Direction {
        CW = 1,
        ClockWise = 1,
        CCW = -1,
        CounterClockWise = -1
    }

    property bool background: true
    property string backgroundColor: "#333333"
    property string color: "lightgreen"
    property int direction: CircularBar.Direction.CW
    property real max: 1.0
    required property real size
    property real startPosition: 90
    property real thickness: 10
    required property real value

    height: size
    preferredRendererType: Shape.CurveRenderer
    width: size

    ShapePath {
        capStyle: ShapePath.RoundCap
        fillColor: "transparent"
        strokeColor: base.background ? base.backgroundColor : "transparent"
        strokeStyle: ShapePath.SolidLine
        strokeWidth: base.thickness

        PathAngleArc {
            centerX: base.size / 2
            centerY: base.size / 2
            radiusX: base.size / 2
            radiusY: base.size / 2
            startAngle: 0
            sweepAngle: 360
        }
    }

    ShapePath {
        capStyle: ShapePath.RoundCap
        fillColor: "transparent"
        strokeColor: base.color
        strokeStyle: ShapePath.SolidLine
        strokeWidth: base.thickness

        Behavior on strokeColor {
            enabled: Config.animations
            ColorAnimation {
                duration: 250;
            }
        }

        PathAngleArc {
            centerX: base.size / 2
            centerY: base.size / 2
            radiusX: base.size / 2
            radiusY: base.size / 2
            startAngle: base.startPosition
            sweepAngle: base.value / base.max * 360 * base.direction

            Behavior on sweepAngle {
                enabled: Config.animations
                NumberAnimation {
                    duration: 250;
                }
            }
        }
    }
}
