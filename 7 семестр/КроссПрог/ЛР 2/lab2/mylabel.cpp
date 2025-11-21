#include "mylabel.h"

MyLabel::MyLabel(QWidget *parent) : QLabel(parent)
{

}

void MyLabel::setValue(int value)
{
    if (value > max)
    {
        emit ownDisableSignal(true);
    }
    this->setText(QString::number(value));
}
