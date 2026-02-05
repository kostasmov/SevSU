#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    /*// формируем путь к файлу БД
    //QString DBpath = QDir::toNativeSeparators(qApp->applicationDirPath() + "/student.db");
    QString DBpath = "C:/QtProjects/lab6/student.db";

    // добавляем нашу БД
    sdb = QSqlDatabase::addDatabase("QSQLITE");
    sdb.setDatabaseName(DBpath);*/

    QString DBpath = QStandardPaths::writableLocation(QStandardPaths::AppDataLocation) + "/student.db";
    QDir().mkpath(QFileInfo(DBpath).absolutePath());

    if (!QFile::exists(DBpath)) {
        QFile::copy(":/db/student.db", DBpath);
        QFile::setPermissions(DBpath, QFileDevice::ReadOwner | QFileDevice::WriteOwner);
    }

    QSqlDatabase sdb = QSqlDatabase::addDatabase("QSQLITE");
    sdb.setDatabaseName(DBpath);

    // пытаемся подключиться
    if(!sdb.open())
    {
        QMessageBox::critical(this, tr("SQLite connection"), tr("Unable connect to DB, check file permission."));
        exit(1);
    }

    // создаем модель
    QSqlTableModel *model = new QSqlTableModel(ui->studentView);
    model->setTable("Student");

    // задаем режим редактирования при изменении поля
    model->setEditStrategy(QSqlTableModel::OnFieldChange);
    model->select();

    // привязываем QTableView к модели
    ui->studentView->setModel(model);

    // соединяем сигнал нажатия кнопки со слотом удаления записей
    connect(ui->deleteButton, SIGNAL(clicked()), SLOT(deleteSelected()));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::deleteSelected()
{
    // получаем индексы выделенных ячеек
    QModelIndexList indexes = ui->studentView->selectionModel()->selection().indexes();
    QSet<int> *rowsToDelete = new QSet<int>();

    // формируем список строк на удаление
    for (int i = 0; i < indexes.count(); ++i)
    {
        QModelIndex index = indexes.at(i);
        rowsToDelete->insert(index.row());
    }

    // удаляем
    QAbstractItemModel *model = ui->studentView->model();
    QSet<int>::iterator i;
    for (i = rowsToDelete->begin(); i != rowsToDelete->end(); ++i)
    {
        model->removeRow(*i);
    }
}
