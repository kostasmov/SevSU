// РЕАЛИЗАЦИЯ КЛАССА MainWindow

#include "mainwindow.h"
//#include "ui_mainwindow.h"

#include <QLabel>       // надпись
#include <QVBoxLayout>  // вертикальная схема размещения
#include <QHBoxLayout>  // горизонтальная схема размещения
#include <QCheckBox>    // флажок включить/выключить
#include <QRadioButton> // радиокнопка
#include <QComboBox>    // выпадающий список
#include <QPushButton>  // кнопка действия
#include <QSpacerItem>  // растяжка

// Конструктор MainWindow
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    //, ui(new Ui::MainWindow)
{
    // Основная вертикальная схема размещения
    QVBoxLayout *centralLayout = new QVBoxLayout();

    // Растяжка
    QSpacerItem *spacer = new QSpacerItem(0, 0,
                                         QSizePolicy::Minimum,      // минимум по горизонтали
                                         QSizePolicy::Expanding);   // растягивание по вертикали


    // ----- Вопрос 1: CheckBox -----
    QLabel *question1Label = new QLabel("Вопрос 1: Какие файлы НЕ определяют "
                                        "конфигурацию сборки проекта в Qt?");

    centralLayout->addWidget(question1Label);

    centralLayout->addWidget(new QCheckBox(".cpp"));    // верно
    centralLayout->addWidget(new QCheckBox(".txt"));
    centralLayout->addWidget(new QCheckBox(".ui"));     // верно

    centralLayout->addSpacerItem(spacer);


    // ----- Вопрос 2: RadioButton -----
    QLabel *question2Label = new QLabel("Вопрос 2: Какой макрос используется для "
                                        "объявления класса с поддержкой сигналов и слотов?");

    centralLayout->addWidget(question2Label);

    centralLayout->addWidget(new QRadioButton("Q_SIGNAL"));
    centralLayout->addWidget(new QRadioButton("Q_SLOT"));
    centralLayout->addWidget(new QRadioButton("Q_OBJECT")); // верно

    centralLayout->addSpacerItem(spacer);


    // ----- Вопрос 3: ComboBox -----
    QLabel *question3Label = new QLabel("Вопрос 3: Выберите тип файла, который хранит "
                                        "описание интерфейса, созданного в Qt Designer:");

    QComboBox *question3ComboBox = new QComboBox;
    question3ComboBox->addItem(".h");
    question3ComboBox->addItem(".ui");     // верно
    question3ComboBox->addItem(".txt");

    //question3ComboBox->setSizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
    //question3ComboBox->setFixedWidth(120);

    centralLayout->addWidget(question3Label);
    centralLayout->addWidget(question3ComboBox);
    centralLayout->addSpacerItem(spacer);


    // Кнопка завершения теста
    QPushButton *loadButton = new QPushButton("Загрузка данных в форму из внешнего файла");
    centralLayout->addWidget(loadButton);

    connect(loadButton, &QPushButton::clicked,
            this, &MainWindow::loadDataFromFile);


    // Центральный виджет
    QWidget *centralWidget = new QWidget();
    centralWidget->setLayout(centralLayout);
    this->setCentralWidget(centralWidget);

    setWindowTitle("Форма тестирования знаний");

    //ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    //delete ui;
}

#include <QFile>        // работа с файлами
#include <QTextStream>  // поток передачи текста
#include <QMessageBox>  // диалоговое окно

// Загрузка данных в форму из внешнего файла;
void MainWindow::loadDataFromFile()
{
    QFile file("C:/QtProjects/lab3/data.txt");
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {        // передача текста в режиме для чтения
        QMessageBox::warning(this, "Ошибка", "Не удалось открыть файл");
        return;
    }

    QTextStream in(&file);  // поток ввода

    // ----- Вопрос 1: CheckBox -----
    QString line1 = in.readLine();
    //QStringList cbStates = line1.split('.');

    QList<QCheckBox*> checkBoxes = this->findChildren<QCheckBox*>();
    for (int i = 0; i < line1.length() && i < checkBoxes.size(); i++) {
        checkBoxes[i]->setChecked(line1[i] == '1');
    }

    // ----- Вопрос 2: RadioButton -----
    QString line2 = in.readLine();
    int radioIndex = line2.toInt();

    QList<QRadioButton*> radioButtons = this->findChildren<QRadioButton*>();
    if (radioIndex >= 0 && radioIndex < radioButtons.size()) {
        radioButtons[radioIndex]->setChecked(true);
    }

    // ----- Вопрос 3: ComboBox -----
    QString line3 = in.readLine();
    int comboIndex = line3.toInt();

    QComboBox *combo = this->findChild<QComboBox*>();
    if (comboIndex >= 0 && comboIndex < combo->count()) {
        combo->setCurrentIndex(comboIndex);
    }

    file.close();
}
