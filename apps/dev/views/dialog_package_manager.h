/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        dialog_package_manager.h
 * @brief
 *
 *****************************************************************************
 * @attention
 * Licensed under the GNU General Public License v. 3 (the "License");
 * You may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.gnu.org/licenses/gpl-3.0.html
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Copyright (C) 2024-2024 xqyjlj<xqyjlj@126.com>
 *
 *****************************************************************************
 * Change Logs:
 * Date           Author       Notes
 * ------------   ----------   -----------------------------------------------
 * 2024-02-27     xqyjlj       initial version
 */

#ifndef PACKAGE_MANAGER_DIALOG_H
#define PACKAGE_MANAGER_DIALOG_H

#include <QDialog>
#include <QSortFilterProxyModel>
#include <QStandardItem>

#include "xmake.h"

namespace Ui
{
class dialog_package_manager;
}

class dialog_package_manager final : public QDialog
{
    Q_OBJECT

  public:
    explicit dialog_package_manager(QWidget *parent = nullptr);

    ~dialog_package_manager();

  private:
    Ui::dialog_package_manager *_ui;
    QSortFilterProxyModel *_tableview_proxy_model = nullptr;
    typedef struct
    {
        QString version;
        bool installed;
    } package_info_t;
    QMap<QString, package_info_t> _selected_package_infos;
    int _install_count = 0, _uninstall_count = 0, _update_count = 0;
    xmake *_xmake_instance = nullptr;

    void init_treeview();
    Qt::CheckState treeview_item_sibling_check_state(const QStandardItem *item) const;
    void update_pushbutton_install_update_uninstall_status();

  private slots:
    void treeview_model_item_changed_callback(QStandardItem *item);
    void toolbutton_collapse_pressed_callback() const;
    void toolbutton_expand_pressed_callback() const;

    void pushbutton_close_pressed_callback();
    void pushbutton_install_pressed_callback() const;
    void pushbutton_update_pressed_callback() const;
    void pushbutton_uninstall_pressed_callback() const;
};

#endif // PACKAGE_MANAGER_DIALOG_H
