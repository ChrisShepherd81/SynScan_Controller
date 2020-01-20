import QtQuick 2.0
import QtQuick.Controls 2.12

Button {
    id: root
    property int button_height: 40
    property int button_width: 150

    MouseArea {
       id: buttonMouseId
       anchors.fill: parent
       onClicked:
       {
           root.clicked()
       }
    }

    background: Rectangle {
        implicitHeight: button_height
        implicitWidth: button_width
        color: buttonMouseId.pressed ? "gray" : "lightgray"
        border.color: "darkgray"
        border.width: 1
        radius: 4
    }
}
