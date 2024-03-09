/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        dialog_package_manager.cpp
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

#include <QDebug>
#include <QStack>
#include <QStandardItemModel>
#include <QStyle>

#include "dialog_package_manager.h"
#include "ui_dialog_package_manager.h"
#include "xmake.h"

#include <qtjson.h>

dialog_package_manager::dialog_package_manager(QWidget *parent)
    : QDialog(parent),
      _ui(new Ui::dialog_package_manager)
{
    _ui->setupUi(this);

    _xmake_instance = xmake::get_instance();

    setWindowFlags(Qt::Dialog | Qt::WindowCloseButtonHint | Qt::WindowMinimizeButtonHint |
                   Qt::WindowMaximizeButtonHint);

    connect(_ui->toolbutton_collapse, &QPushButton::pressed, this, &dialog_package_manager::toolbutton_collapse_pressed_callback,
            Qt::UniqueConnection);
    connect(_ui->toolbutton_expand, &QPushButton::pressed, this, &dialog_package_manager::toolbutton_expand_pressed_callback,
            Qt::UniqueConnection);
    connect(_ui->pushbutton_close, &QPushButton::pressed, this, &dialog_package_manager::pushbutton_close_pressed_callback,
            Qt::UniqueConnection);
    connect(_ui->pushbutton_install, &QPushButton::pressed, this, &dialog_package_manager::pushbutton_install_pressed_callback,
            Qt::UniqueConnection);
    connect(_ui->pushbutton_update, &QPushButton::pressed, this, &dialog_package_manager::pushbutton_update_pressed_callback,
            Qt::UniqueConnection);
    connect(_ui->pushbutton_uninstall, &QPushButton::pressed, this, &dialog_package_manager::pushbutton_uninstall_pressed_callback,
            Qt::UniqueConnection);

    init_treeview();
}

dialog_package_manager::~dialog_package_manager()
{
    delete _ui;
}

void dialog_package_manager::init_treeview()
{
    _tableview_proxy_model = new QSortFilterProxyModel(this);
    QStandardItemModel *model = new QStandardItemModel(_ui->treeview);
    model->setColumnCount(7);
    model->setHeaderData(0, Qt::Horizontal, tr("Name"));
    model->setHeaderData(1, Qt::Horizontal, tr("Size"));
    model->setHeaderData(2, Qt::Horizontal, tr("Home Page"));
    model->setHeaderData(3, Qt::Horizontal, tr("Status"));
    model->setHeaderData(4, Qt::Horizontal, tr("Description"));
    model->setHeaderData(5, Qt::Horizontal, tr("License"));
    model->setHeaderData(6, Qt::Horizontal, tr("Sha"));

    xmake::packages_t packages;
    xmake::load_packages(&packages);

    const QMap<QString, xmake::info_t> *library = &packages.library;
    QMap<QString, xmake::info_t>::const_iterator library_i = library->constBegin();
    while (library_i != library->constEnd())
    {
        QList<QStandardItem *> *items = new QList<QStandardItem *>;

        QStandardItem *const item = new QStandardItem(library_i.key()); /** Name */
        item->setCheckable(true);
        item->setAutoTristate(true);
        items->append(item);
        /** Size */
        items->append(new QStandardItem());
        /** Home Page */
        items->append(new QStandardItem(library_i.value().homepage));
        /** Status */
        items->append(new QStandardItem());
        /** Description */
        items->append(new QStandardItem(library_i.value().description));
        /** License */
        items->append(new QStandardItem(library_i.value().license));

        const QMap<QString, xmake::version_t> *versions = &library_i.value().versions;
        QMap<QString, xmake::version_t>::const_iterator versions_i = versions->constBegin();
        while (versions_i != versions->constEnd())
        {
            QList<QStandardItem *> *child_items = new QList<QStandardItem *>;
            /** Name */
            QStandardItem *const child_item = new QStandardItem(versions_i.key());
            child_item->setCheckable(true);
            child_item->setAutoTristate(true);
            child_items->append(child_item);
            /** Size */
            child_items->append(new QStandardItem(QString::number(versions_i.value().size, 'f', 2)));
            /** Home Page */
            child_items->append(new QStandardItem());
            /** Status */
            child_items->append(new QStandardItem(QApplication::style()->standardIcon(versions_i.value().installed ? QStyle::SP_DialogYesButton : QStyle::SP_DialogNoButton),
                                                  versions_i.value().installed ? tr("Installed") : tr("Not Installed")));
            /** Description */
            child_items->append(new QStandardItem());
            /** License */
            child_items->append(new QStandardItem());
            /** Sha */
            child_items->append(new QStandardItem(versions_i.value().sha256));

            for (const auto &i : *child_items)
            {
                i->setEditable(false);
            }

            item->appendRow(*child_items);
            ++versions_i;
        }

        model->appendRow(*items);

        for (const auto &i : *items)
        {
            i->setEditable(false);
        }

        ++library_i;
    }
    connect(model, &QStandardItemModel::itemChanged, this, &dialog_package_manager::treeview_model_item_changed_callback, Qt::UniqueConnection);
    _tableview_proxy_model->setSourceModel(model);

    delete _ui->treeview->model();
    _ui->treeview->setModel(_tableview_proxy_model);
    _ui->treeview->expandAll();
    _ui->treeview->setSortingEnabled(true);
    _ui->treeview->sortByColumn(0, Qt::AscendingOrder);
    _ui->treeview->header()->setMinimumSectionSize(10);
    _ui->treeview->header()->setSectionResizeMode(QHeaderView::Interactive);
}

void dialog_package_manager::treeview_model_item_changed_callback(QStandardItem *item)
{
    disconnect(dynamic_cast<QStandardItemModel *>(_tableview_proxy_model->sourceModel()), &QStandardItemModel::itemChanged, this, &dialog_package_manager::treeview_model_item_changed_callback);
    if (item != nullptr)
    {
        if (item->isCheckable())
        {
            /** 获取当前的选择状态 */
            const Qt::CheckState state = item->checkState();
            /** 如果条目不是三态的，说明可以对子节点进行处理 */
            if (state != Qt ::PartiallyChecked)
            {
                QStack<QStandardItem *> stack;
                stack.push(item);
                while (!stack.empty())
                {
                    item = stack.pop();
                    const int row_count = item->rowCount();
                    for (int i = 0; i < row_count; i++)
                    {
                        QStandardItem *child = item->child(i);
                        stack.push(child);
                    }
                    if (item->isCheckable())
                    {
                        item->setCheckState(state);
                    }
                }
            }
            /** 处理父节点 */
            {
                QStack<QStandardItem *> stack;
                stack.push(item);
                while (!stack.empty())
                {
                    item = stack.pop();
                    const Qt::CheckState sibling_state = treeview_item_sibling_check_state(item);
                    QStandardItem *parent_item = item->parent();
                    if (nullptr != parent_item)
                    {
                        stack.push(parent_item);
                        if (Qt::PartiallyChecked == sibling_state)
                        {
                            if (parent_item->isCheckable() && parent_item->isAutoTristate())
                            {
                                parent_item->setCheckState(Qt::PartiallyChecked);
                            }
                        }
                        else if (Qt::Checked == sibling_state)
                        {
                            if (parent_item->isCheckable())
                            {
                                parent_item->setCheckState(Qt::Checked);
                            }
                        }
                        else
                        {
                            if (parent_item->isCheckable())
                            {
                                parent_item->setCheckState(Qt::Unchecked);
                            }
                        }
                    }
                }
            }
        }
    }
    connect(dynamic_cast<QStandardItemModel *>(_tableview_proxy_model->sourceModel()), &QStandardItemModel::itemChanged, this, &dialog_package_manager::treeview_model_item_changed_callback, Qt::UniqueConnection);
    update_pushbutton_install_update_uninstall_status();
}

Qt::CheckState dialog_package_manager::treeview_item_sibling_check_state(const QStandardItem *item) const
{
    Qt::CheckState check_state;
    const QStandardItem *parent = item->parent();
    if (nullptr != parent)
    {
        const int brother_count = parent->rowCount();
        int checked_count = 0, un_checked_count = 0;
        for (int i = 0; i < brother_count; ++i)
        {
            const QStandardItem *sibling_item = parent->child(i);
            const Qt::CheckState state = sibling_item->checkState();
            if (Qt::Unchecked == state)
            {
                un_checked_count++;
            }
            else
            {
                checked_count++;
            }
        }
        if (checked_count > 0 && un_checked_count > 0)
        {
            check_state = Qt::PartiallyChecked;
        }
        else if (un_checked_count > 0)
        {
            check_state = Qt::Unchecked;
        }
        else
        {
            check_state = Qt::Checked;
        }
    }
    else
    {
        check_state = item->checkState();
    }
    return check_state;
}

void dialog_package_manager::update_pushbutton_install_update_uninstall_status()
{
    QStack<QStandardItem *> stack;
    const int row_count = dynamic_cast<QStandardItemModel *>(_tableview_proxy_model->sourceModel())->rowCount();

    _selected_package_infos.clear();
    _install_count = 0;
    _uninstall_count = 0;
    _update_count = 0;

    for (int i = 0; i < row_count; i++)
    {
        QStandardItem *item = dynamic_cast<QStandardItemModel *>(_tableview_proxy_model->sourceModel())->item(i);
        stack.push(item);
        while (!stack.empty())
        {
            item = stack.pop();
            const int count = item->rowCount();
            for (int j = 0; j < count; j++)
            {
                QStandardItem *child = item->child(j);
                stack.push(child);
            }
            if (item->isCheckable())
            {
                if (item->checkState() != Qt::Unchecked)
                {
                    const QStandardItem *parent = item->parent();
                    if (parent != nullptr)
                    {
                        const QString name = parent->text();
                        const QStandardItem *child_item = parent->child(item->row(), 0);
                        const QString version = child_item->text();
                        child_item = parent->child(item->row(), 3);
                        const QString status = child_item->text();
                        if (status == tr("Installed"))
                        {
                            if (version == "latest")
                            {
                                _update_count++;
                            }
                            _install_count++;
                        }
                        else if (status == tr("Not Installed"))
                        {
                            _uninstall_count++;
                        }
                        _selected_package_infos.insert(name, { version, status == tr("Installed") });
                    }
                }
            }
        }
    }

    _ui->pushbutton_uninstall->setEnabled(_install_count > 0);
    _ui->pushbutton_install->setEnabled(_uninstall_count > 0);
    _ui->pushbutton_update->setEnabled(_update_count > 0);
}

void dialog_package_manager::toolbutton_collapse_pressed_callback() const
{
    _ui->treeview->collapseAll();
}

void dialog_package_manager::toolbutton_expand_pressed_callback() const
{
    _ui->treeview->expandAll();
}

void dialog_package_manager::pushbutton_close_pressed_callback()
{
    close();
}

void dialog_package_manager::pushbutton_install_pressed_callback() const
{
    auto info_i = _selected_package_infos.constBegin();
    const xmake::log_handler_t handler = xmake::get_log_handler();
    xmake::set_log_handler(nullptr);
    while (info_i != _selected_package_infos.constEnd())
    {
        if (!info_i.value().installed)
        {
            _xmake_instance->install_package(info_i.key(), info_i.value().version);
        }
        ++info_i;
    }
    xmake::set_log_handler(handler);
}

void dialog_package_manager::pushbutton_update_pressed_callback() const
{
    qDebug() << _update_count;
}

void dialog_package_manager::pushbutton_uninstall_pressed_callback() const
{
    qDebug() << _install_count;
}
