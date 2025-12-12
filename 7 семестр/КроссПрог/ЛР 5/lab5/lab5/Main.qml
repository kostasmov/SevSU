import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "."

ApplicationWindow {
    width: 370
    height: 500
    visible: true

    property int redButtonIndex: gameController.redButtonIndex

    function getRandomIndex(excludeIndex) {
        var newIndex;
        do {
            newIndex = Math.floor(Math.random() * 12);
        } while (newIndex === excludeIndex);
        return newIndex;
    }

    GridLayout {
        columns: 3
        rows: 4
        anchors.fill: parent
        anchors.margins: 20

        Repeater {
            id: repeater
            model: 12

            delegate: CustomButton {
                index: modelData
                buttonColor: modelData === redButtonIndex ? "red" : "lightblue"
            }

        }
    }

    Row {
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        spacing: 50

        Button {
            text: "Сохранить"
            onClicked: {
                gameController.saveState()
            }
        }

        Button {
            text: "Загрузить"
            onClicked: {
                gameController.loadState();

                for (var i = 0; i < repeater.count; i++) {
                    repeater.itemAt(i).buttonColor = i === gameController.redButtonIndex ? "red" : "lightblue";
                }
            }
        }

    }

    Connections {
        target: gameController
        onRedButtonIndexChanged: {
            redButtonIndex = gameController.redButtonIndex;
            for (var i = 0; i < repeater.count; i++) {
                repeater.itemAt(i).buttonColor = i === redButtonIndex ? "red" : "lightblue";
            }
        }
    }
}

