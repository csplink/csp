/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        DialogPackageManager.cpp
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

#include "DialogPackageManager.h"
#include "ui_DialogPackageManager.h"
#include "xmake.h"

DialogPackageManager::DialogPackageManager(QWidget *parent)
    : QDialog(parent),
      ui_(new Ui::dialogPackageManager)
{
    ui_->setupUi(this);

    xmakeInstance_ = xmake::get_instance();

    setWindowFlags(Qt::Dialog | Qt::WindowCloseButtonHint | Qt::WindowMinimizeButtonHint |
                   Qt::WindowMaximizeButtonHint);

    connect(ui_->toolButtonCollapse, &QPushButton::pressed, this, &DialogPackageManager::toolButtonCollapsePressedCallback, Qt::UniqueConnection);
    connect(ui_->toolButtonExpand, &QPushButton::pressed, this, &DialogPackageManager::toolButtonExpandPressedCallback, Qt::UniqueConnection);
    connect(ui_->pushButtonClose, &QPushButton::pressed, this, &DialogPackageManager::pushButtonClosePressedCallback, Qt::UniqueConnection);
    connect(ui_->pushButtonInstall, &QPushButton::pressed, this, &DialogPackageManager::pushButtonInstallPressedCallback, Qt::UniqueConnection);
    connect(ui_->pushButtonUpdate, &QPushButton::pressed, this, &DialogPackageManager::pushButtonUpdatePressedCallback, Qt::UniqueConnection);
    connect(ui_->pushButtonUninstall, &QPushButton::pressed, this, &DialogPackageManager::pushButtonUninstallPressedCallback, Qt::UniqueConnection);

    initTreeView();
}

DialogPackageManager::~DialogPackageManager()
{
    delete ui_;
}

void DialogPackageManager::initTreeView()
{
    tableViewProxyModel_ = new QSortFilterProxyModel(this);
    QStandardItemModel *model = new QStandardItemModel(ui_->treeView);
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
    connect(model, &QStandardItemModel::itemChanged, this, &DialogPackageManager::treeViewModelItemChangedCallback, Qt::UniqueConnection);
    tableViewProxyModel_->setSourceModel(model);

    delete ui_->treeView->model();
    ui_->treeView->setModel(tableViewProxyModel_);
    ui_->treeView->expandAll();
    ui_->treeView->setSortingEnabled(true);
    ui_->treeView->sortByColumn(0, Qt::AscendingOrder);
    ui_->treeView->header()->setMinimumSectionSize(10);
    ui_->treeView->header()->setSectionResizeMode(QHeaderView::Interactive);
}

void DialogPackageManager::treeViewModelItemChangedCallback(QStandardItem *item)
{
    disconnect(dynamic_cast<QStandardItemModel *>(tableViewProxyModel_->sourceModel()), &QStandardItemModel::itemChanged, this, &DialogPackageManager::treeViewModelItemChangedCallback);
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
                    const Qt::CheckState sibling_state = treeViewItemSiblingCheckState(item);
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
    connect(dynamic_cast<QStandardItemModel *>(tableViewProxyModel_->sourceModel()), &QStandardItemModel::itemChanged, this, &DialogPackageManager::treeViewModelItemChangedCallback, Qt::UniqueConnection);
    updatePushButtonInstallUpdateUninstallStatus();
}

Qt::CheckState DialogPackageManager::treeViewItemSiblingCheckState(const QStandardItem *item) const
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

void DialogPackageManager::updatePushButtonInstallUpdateUninstallStatus()
{
    QStack<QStandardItem *> stack;
    const int row_count = dynamic_cast<QStandardItemModel *>(tableViewProxyModel_->sourceModel())->rowCount();

    selectedPackageInfos_.clear();
    installCount_ = 0;
    uninstallCount_ = 0;
    updateCount_ = 0;

    for (int i = 0; i < row_count; i++)
    {
        QStandardItem *item = dynamic_cast<QStandardItemModel *>(tableViewProxyModel_->sourceModel())->item(i);
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
                                updateCount_++;
                            }
                            installCount_++;
                        }
                        else if (status == tr("Not Installed"))
                        {
                            uninstallCount_++;
                        }
                        selectedPackageInfos_.insert(name, { version, status == tr("Installed") });
                    }
                }
            }
        }
    }

    ui_->pushButtonUninstall->setEnabled(installCount_ > 0);
    ui_->pushButtonInstall->setEnabled(uninstallCount_ > 0);
    ui_->pushButtonUpdate->setEnabled(updateCount_ > 0);
}

void DialogPackageManager::toolButtonCollapsePressedCallback() const
{
    ui_->treeView->collapseAll();
}

void DialogPackageManager::toolButtonExpandPressedCallback() const
{
    ui_->treeView->expandAll();
}

void DialogPackageManager::pushButtonClosePressedCallback()
{
    close();
}

void DialogPackageManager::pushButtonInstallPressedCallback() const
{
    auto info_i = selectedPackageInfos_.constBegin();
    const xmake::log_handler_t handler = xmake::get_log_handler();
    xmake::set_log_handler(nullptr);
    while (info_i != selectedPackageInfos_.constEnd())
    {
        if (!info_i.value().Installed)
        {
            xmakeInstance_->install_package(info_i.key(), info_i.value().Version);
        }
        ++info_i;
    }
    xmake::set_log_handler(handler);
}

void DialogPackageManager::pushButtonUpdatePressedCallback() const
{
    qDebug() << updateCount_;
}

void DialogPackageManager::pushButtonUninstallPressedCallback() const
{
    qDebug() << installCount_;
}
