import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: customButton
    width: 100
    height: 100

    property string buttonColor: "lightblue"
    property int index: 0

    Button {
        id: button
        anchors.fill: parent
        text: (index + 1)
        hoverEnabled: false
        background: Rectangle {
            radius: 15
            color: customButton.buttonColor
            border.color: "black"
        }

        onClicked: {
            if (customButton.buttonColor === "red") {
                customButton.buttonColor = "lightblue";
                var newRedIndex = getRandomIndex(redButtonIndex);
                repeater.itemAt(newRedIndex).buttonColor = "red";
                gameController.setRedButtonIndex(newRedIndex);
            }
        }
    }
}
