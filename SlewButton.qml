import QtQuick 2.0
import QtQuick.Controls 2.12

Button {

    onReleased: {
        viewModel.on_slewStop()
    }

    MouseArea {
       id: buttonMouseId
       anchors.fill: parent
    }

    background: Rectangle {
           implicitWidth: 50
           implicitHeight: 50
           color: buttonMouseId.pressed ? "lightgray" : "gray"
           border.color: "darkgray"
           border.width: 1
           radius: 4
    }

    font {
        pixelSize: 22
        bold: true
    }
}
