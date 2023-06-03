/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        choose_chip_dialog.h
 *  @brief
 *
 * ****************************************************************************
 *  @attention
 *  Licensed under the GNU General Public License v. 3 (the "License");
 *  You may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      https://www.gnu.org/licenses/gpl-3.0.html
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *  Copyright (C) 2023-2023 xqyjlj<xqyjlj@126.com>
 *
 * ****************************************************************************
 *  Change Logs:
 *  Date           Author       Notes
 *  ------------   ----------   -----------------------------------------------
 *  2023-05-13     xqyjlj       initial version
 */

#ifndef CHOOSE_MCU_DIALOG_H
#define CHOOSE_MCU_DIALOG_H

#include <QAbstractButton>
#include <QDialog>
#include <QModelIndexList>
#include <QSortFilterProxyModel>
#include <QStandardItemModel>

#include "repo.h"
#include "project.h"

namespace Ui {
class choose_chip_dialog;
}

class choose_chip_dialog : public QDialog {
    Q_OBJECT

public:
    explicit choose_chip_dialog(QWidget *parent = nullptr);
    ~choose_chip_dialog() override;

private slots:
    void treeview_chip_filter_model_item_changed_callback(QStandardItem *item);
    void tableview_chip_infos_selection_model_selection_changed_callback(const QItemSelection &selected,
                                                                         const QItemSelection &deselected);
    void on_dialogbuttonbox_clicked(QAbstractButton *button);
    void on_pushbutton_name_pressed();
    void on_pushbutton_company_pressed();

private:
    Ui::choose_chip_dialog *ui;
    csp::repo              *_repo_instance;
    csp::project           *_project_instance = nullptr;

    QString _chip_name;
    QString _hal_name;
    QString _package_name;

    QStringList _company_keys;
    QStringList _series_keys;
    QStringList _line_keys;
    QStringList _core_keys;
    QStringList _package_keys;

    QStandardItem *_company_root = nullptr;
    QStandardItem *_series_root  = nullptr;
    QStandardItem *_line_root    = nullptr;
    QStandardItem *_core_root    = nullptr;
    QStandardItem *_package_root = nullptr;

    QList<QStandardItem *> _company_items;
    QList<QStandardItem *> _series_items;
    QList<QStandardItem *> _line_items;
    QList<QStandardItem *> _core_items;
    QList<QStandardItem *> _package_items;

    QList<QList<QStandardItem *> *>             _chips_items;
    QSortFilterProxyModel                      *_tableview_chip_infos_proxy_model = nullptr;
    QList<csp::repository_table::chip_info_t *> _chips;

private:
    void find_all_keys();
    void init_treeview_chip_filter();
    void init_tableview_chip_infos();
    void set_chips_info_ui(const QModelIndexList &selected_indexes);
};

#endif  // CHOOSE_MCU_DIALOG_H
