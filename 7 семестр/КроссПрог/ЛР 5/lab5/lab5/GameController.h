#ifndef GAMECONTROLLER_H
#define GAMECONTROLLER_H

#include <QObject>
#include <QFile>
#include <QTextStream>
#include <QDebug>

class GameController : public QObject
{
    Q_OBJECT
    Q_PROPERTY(int redButtonIndex READ redButtonIndex WRITE setRedButtonIndex NOTIFY redButtonIndexChanged)

public:
    explicit GameController(QObject *parent = nullptr) : QObject(parent), m_redButtonIndex(0) {}

    int redButtonIndex() const { return m_redButtonIndex; }

    Q_INVOKABLE void setRedButtonIndex(int index) {
        if (m_redButtonIndex != index) {
            m_redButtonIndex = index;
            emit redButtonIndexChanged();
        }
    }

    Q_INVOKABLE void saveState() {
        QFile file("game_state.txt");
        if (file.open(QIODevice::WriteOnly)) {
            QTextStream out(&file);
            out << m_redButtonIndex;
            qDebug() << "Состояние игры сохранено с redButtonIndex:" << m_redButtonIndex;
        } else {
            qDebug() << "Ошибка: Не удалось сохранить состояние игры.";
        }
    }

    Q_INVOKABLE void loadState() {
        QFile file("game_state.txt");
        if (file.open(QIODevice::ReadOnly)) {
            int index;
            QTextStream in(&file);
            in >> index;
            setRedButtonIndex(index);
            qDebug() << "Состояние игры загружено с redButtonIndex:" << m_redButtonIndex;
        } else {
            qDebug() << "Ошибка: Не удалось загрузить состояние игры.";
        }
    }

signals:
    void redButtonIndexChanged();

private:
    int m_redButtonIndex;
};

#endif // GAMECONTROLLER_H
