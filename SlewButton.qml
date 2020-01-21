import QtQuick 2.0
import QtQuick.Controls 2.12

CustomButton {

   button_height: 50
   button_width: 50

    onReleased: {
        console.log("SlewButton.onReleased")
        viewModel.on_slewStop()
    }

    font {
        pixelSize: 22
        bold: true
    }
}
