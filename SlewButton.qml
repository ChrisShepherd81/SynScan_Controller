import QtQuick 2.0
import QtQuick.Controls 2.12

Button {

    onReleased: {
        viewModel.on_slewStop()
    }

    background: Rectangle {
           implicitWidth: 50
           implicitHeight: 50
           color: "#00ffff"
    }
}
