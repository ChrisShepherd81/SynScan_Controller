import QtQuick 2.0
import QtQuick.Controls 2.12

Button {
    id: root
    property int button_height: 40
    property int button_width: 150

    background: Rectangle {
        id: buttonBackground
        implicitHeight: button_height
        implicitWidth: button_width
        color: root.down ? "gray": "lightgray"
        border.color: "darkgray"
        border.width: 1
        radius: 4
    }
}
