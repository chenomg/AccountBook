#ifndef EXPORTWINDOW_H
#define EXPORTWINDOW_H

#include <QDialog>

namespace Ui {
class exportwindow;
}

class exportwindow : public QDialog
{
    Q_OBJECT

public:
    explicit exportwindow(QWidget *parent = 0);
    ~exportwindow();

private:
    Ui::exportwindow *ui;
};

#endif // EXPORTWINDOW_H
