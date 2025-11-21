#include "mainwindow.h"
#include "./ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    connect(ui->pushButton, &QPushButton::clicked,
            this, &MainWindow::setTitle);           // изменение заголовка
    connect(ui->plainTextEdit, &QPlainTextEdit::textChanged,
            this, &MainWindow::copyWithReplace);    // копирование с заменой а на *
    connect(ui->plainTextEdit_2, &QPlainTextEdit::textChanged,
            this, &MainWindow::countSigns);         // подсчёт символов '*'
    connect(ui->label, &MyLabel::ownDisableSignal,
            ui->plainTextEdit, &QWidget::setDisabled);   // проверка на превышение символов 'а'
}

void MainWindow::setTitle()
{
    this->setWindowTitle(ui->lineEdit->text());
}

void MainWindow::copyWithReplace()
{
    QString text = ui->plainTextEdit->toPlainText();
    text.replace("а", "*");
    ui->plainTextEdit_2->setPlainText(text);
}

void MainWindow::countSigns()
{
    QString text = ui->plainTextEdit_2->toPlainText();
    int value = text.count("*");
    ui->label->setValue(value);
}

MainWindow::~MainWindow()
{
    delete ui;
}
