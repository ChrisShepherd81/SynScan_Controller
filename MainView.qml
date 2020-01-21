import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.14

ApplicationWindow {
    title: qsTr("SynScan Controller")
    visible: true
    width: 640
    height: 480

    ColumnLayout {
        RowLayout {
            ComboBox {
                id: comPortSelectId
                textRole: "display"
                model: comPortsModel
            }

            CustomButton {
                button_height: comPortSelectId.height
                text: qsTr("Connect")
                onClicked: {
                    viewModel.connect(comPortSelectId.currentText)
                }
            }

            ComboBox {
                implicitWidth: 100
                width: 50
                id: speed
                currentIndex: 4
                model: ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
            }
        }

        GridLayout {
            property int speed: 9
            rows: 3
            columns: 3

            SpacerItem {}

            SlewButton {
                id: upArrowButton
                text: "↑"
                onPressed: {console.log("SlewButton.upArrowButton.onPressed")
                    viewModel.on_slewUpButton(speed.currentIndex+1) }
            }

            SpacerItem {}

            SlewButton {
                id: leftArrowButton
                text: "←"
                onPressed: { viewModel.on_slewLeftButton(speed.currentIndex+1) }
            }

            SpacerItem {}

            SlewButton {
                id: rightArrowButton
                text: "→"
                onPressed: { viewModel.on_slewRightButton(speed.currentIndex+1) }
            }

            SpacerItem {}

            SlewButton {
                id: downArrowButton
                text: "↓"
                onPressed: { viewModel.on_slewDownButton(speed.currentIndex+1) }
            }

            SpacerItem {}
        }

        RowLayout {
            Label { text: "Location:" }
            Text  { text: viewModel.location }
        }

        RowLayout {
            Label { text: "Current pointing Position:" }
            Text  { text: viewModel.position }
        }
    }
}
