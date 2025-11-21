#ifndef MYLABEL_H
#define MYLABEL_H

#include <QLabel>

class MyLabel : public QLabel
{
    Q_OBJECT
private:
    const int max = 10;
    int value();
public:
    MyLabel(QWidget *parent = nullptr);
public slots:
    void setValue(int value);
signals:
    void ownDisableSignal(bool disable);
};

#endif // MYLABEL_H
