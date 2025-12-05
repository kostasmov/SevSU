import QtQuick

import "core"
import QtQuick.Layouts

Window {
    id: window
    width: 370
    height: 500
    visible: true
    title: qsTr("КПП: ЛР 4")

    property int redButtonIndex: 0  // индекс красной кнопки

    // генерация случайного индекса
    function getRandomIndex(currentIndex) {
        var newIndex;
        do {
            newIndex = Math.floor(Math.random() * 12);
        } while (newIndex === currentIndex);
        return newIndex;
    }

    GridLayout {
        id: gridLayout
        columns: 3
        rows: 4

        anchors.centerIn: parent
        rowSpacing: 10
        columnSpacing: 10

        Repeater {
            id: repeater
            model: 12

            Button {
                buttonColor: modelData === redButtonIndex ? "red" : "lightblue"

                onButtonClick: {
                    if (modelData === redButtonIndex) {
                        var newIndex = getRandomIndex(redButtonIndex);
                        redButtonIndex = newIndex;
                        repeater.itemAt(newIndex).changeColor("red");
                        changeColor("lightblue");
                    }
                }
            }
        }
    }
}
