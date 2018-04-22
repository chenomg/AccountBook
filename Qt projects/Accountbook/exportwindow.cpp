#include "exportwindow.h"
#include "ui_exportwindow.h"

exportwindow::exportwindow(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::exportwindow)
{
    ui->setupUi(this);
}

exportwindow::~exportwindow()
{
    delete ui;
}
