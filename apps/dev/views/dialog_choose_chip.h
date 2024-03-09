/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        dialog_choose_chip.h
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

#ifndef DIALOG_CHOOSE_CHIP_H
#define DIALOG_CHOOSE_CHIP_H

#include <QAbstractButton>
#include <QDialog>
#include <QSortFilterProxyModel>
#include <QStandardItemModel>

#include "project.h"
#include "repo.h"

namespace Ui
{
class dialog_choose_chip;
}

class dialog_choose_chip final : public QDialog
{
    Q_OBJECT

  public:
    explicit dialog_choose_chip(QWidget *parent = nullptr);
    ~dialog_choose_chip() override;

  signals:
    void signals_create_project();

  private slots:
    void treeview_chip_filter_model_item_changed_callback(const QStandardItem *item) const;
    void tableview_chip_infos_selection_model_selection_changed_callback(const QItemSelection &selected,
                                                                         const QItemSelection &deselected);
    void dialogbuttonbox_clicked_callback(const QAbstractButton *button);
    void pushbutton_name_pressed_callback() const;
    void pushbutton_company_pressed_callback() const;

  private:
    Ui::dialog_choose_chip *_ui;
    repo *_repo_instance;
    project *_project_instance = nullptr;

    QString _chip_name;
    QString _hal_name;
    QString _package_name;
    QString _company_name;

    QStringList _company_keys;
    QStringList _series_keys;
    QStringList _line_keys;
    QStringList _core_keys;
    QStringList _package_keys;

    QStandardItem *_company_root = nullptr;
    QStandardItem *_series_root = nullptr;
    QStandardItem *_line_root = nullptr;
    QStandardItem *_core_root = nullptr;
    QStandardItem *_package_root = nullptr;

    QList<QStandardItem *> _company_items;
    QList<QStandardItem *> _series_items;
    QList<QStandardItem *> _line_items;
    QList<QStandardItem *> _core_items;
    QList<QStandardItem *> _package_items;

    QList<QList<QStandardItem *> *> _chips_items;
    QSortFilterProxyModel *_tableview_chip_infos_proxy_model = nullptr;
    QList<repository_table::chip_info_t *> _chips;

  private:
    void find_all_keys();
    void init_treeview_chip_filter();
    void init_tableview_chip_infos();
    void set_chips_info_ui(const QModelIndexList &selected_indexes);
};

#endif // DIALOG_CHOOSE_CHIP_H
