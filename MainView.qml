import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.14

ApplicationWindow {

    //title of the application
    title: qsTr("SynScan Controller")
    visible: true
    width: 640
    height: 480

    GridLayout
    {
        property int speed: 9
        rows: 3
        columns: 3

        SpacerItem {}

        SlewButton {
            id: upArrowButton
            text: "↑"
            onPressed: { viewModel.on_slewUpButton(parent.speed) }
        }

        SpacerItem {}

        SlewButton {
            id: leftArrowButton
            text: "←"
            onPressed: { viewModel.on_slewLeftButton(parent.speed) }
        }

        SpacerItem {}

        SlewButton {
            id: rightArrowButton
            text: "→"
            onPressed: { viewModel.on_slewRightButton(parent.speed) }
        }

        SpacerItem {}

        SlewButton {
            id: downArrowButton
            text: "↓"
            onPressed: { viewModel.on_slewDownButton(parent.speed) }
        }

        SpacerItem {}
    }
}
