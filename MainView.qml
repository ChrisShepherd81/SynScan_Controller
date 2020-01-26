import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.14

ApplicationWindow {
    id: root
    title: qsTr("SynScan Controller")
    visible: true

    height: contentItem.childrenRect.height
    width: contentItem.childrenRect.width

    ColumnLayout {
        RowLayout {
            ComboBox {
                id: comPortSelectId
                textRole: "display"
                model: comPortsModel
            }

            CustomButton {
                button_height: comPortSelectId.height
                text: viewModel.connected ? qsTr("Disconnect") : qsTr("Connect")
                onClicked: {
                    if(!viewModel.connected)
                        viewModel.connect(comPortSelectId.currentText);
                    else
                        viewModel.disconnect();
                }
            }
        }

        GridLayout {
            rows: 3
            columns: 3

            SpacerItem {}

            SlewButton {
                id: upArrowButton
                text: "↑"
                onPressed: {viewModel.on_slewUpButton(speed.currentIndex+1) }
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
            Label { text: "Speed:" }
            ComboBox {
                implicitWidth: 100
                width: 50
                id: speed
                currentIndex: 4
                model: ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
            }
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
