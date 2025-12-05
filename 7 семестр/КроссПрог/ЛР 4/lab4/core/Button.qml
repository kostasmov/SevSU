import QtQuick

Rectangle {
    // идентификатор элемента
    id: button

    // свойства отображения
    height: 100
    width: 100
    radius: 15

    // цвет кнопки (меняется при нажатии)
    property color buttonColor: "lightblue"
    color: buttonMouseArea.pressed ? Qt.darker(buttonColor, 1.5) : buttonColor

    // анимация смены цвета кнопки
    Behavior on color { ColorAnimation{ duration: 55 } }

    // цвет обводки
    property color borderColor: "transparent"
    property color onHoverColor: "lightsteelblue"   // для MouseArea
    border { width: 2; color: borderColor }

    // увеличить кнопку при нажатии
    scale: buttonMouseArea.pressed ? 1.1 : 1.00

    // анимация при увеличении кнопки
    Behavior on scale { NumberAnimation{ duration: 55 }}

    // сигнал, который будет вызываться при нажатии
    signal buttonClick()

    // определение "кликабельной" зоны (поверхность всей кнопки)
    MouseArea {
        id: buttonMouseArea
        anchors.fill: parent    // размер равен размеру "родителя"
        onClicked: buttonClick()

        // отобразить рамку если навели курсор
        hoverEnabled: true
        onEntered: parent.border.color = onHoverColor
        onExited: parent.border.color = borderColor
    }

    // сменить цвет кнопки
    function changeColor(newColor) {
        button.buttonColor = newColor;
    }
}
