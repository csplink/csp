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
#include <QtConcurrent/QtConcurrent>

#include "DialogPackageManager.h"
#include "ToolCspRepo.h"
#include "ui_DialogPackageManager.h"

DialogPackageManager::DialogPackageManager(QWidget *parent)
    : QDialog(parent),
      ui_(new Ui::dialogPackageManager)
{
    ui_->setupUi(this);

    ui_->progressBar->setHidden(true);
    fontMetrics_ = new QFontMetrics(ui_->labelStatus->font());

    setWindowFlags(Qt::Dialog | Qt::WindowCloseButtonHint | Qt::WindowMinimizeButtonHint | Qt::WindowMaximizeButtonHint);

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
    delete fontMetrics_;
    delete ui_;
}

QList<QStandardItem *> *DialogPackageManager::createPackageInfoItems(const QMap<QString, ToolCspRepo::InformationType> *Packages)
{
    QList<QStandardItem *> *items = new QList<QStandardItem *>;
    QMap<QString, ToolCspRepo::InformationType>::const_iterator iterator = Packages->constBegin();
    while (iterator != Packages->constEnd())
    {
        /** Name */
        QStandardItem *const item = new QStandardItem(iterator.key());
        item->setCheckable(true);
        item->setAutoTristate(true);
        items->append(item);
        /** Size */
        items->append(new QStandardItem());
        /** Home Page */
        items->append(new QStandardItem(iterator.value().Homepage));
        /** Status */
        items->append(new QStandardItem());
        /** Description */
        items->append(new QStandardItem(iterator.value().Description));
        /** License */
        items->append(new QStandardItem(iterator.value().License));

        const QMap<QString, ToolCspRepo::VersionType> *versions = &iterator.value().Versions;
        QMap<QString, ToolCspRepo::VersionType>::const_iterator versionsIterator = versions->constBegin();
        while (versionsIterator != versions->constEnd())
        {
            QList<QStandardItem *> *child_items = new QList<QStandardItem *>;
            /** Name */
            QStandardItem *const child_item = new QStandardItem(versionsIterator.key());
            child_item->setCheckable(true);
            child_item->setAutoTristate(true);
            child_items->append(child_item);
            /** Size */
            child_items->append(new QStandardItem(QString::number(versionsIterator.value().Size, 'f', 2)));
            /** Home Page */
            child_items->append(new QStandardItem());
            /** Status */
            child_items->append(new QStandardItem(QApplication::style()->standardIcon(versionsIterator.value().Installed ? QStyle::SP_DialogYesButton : QStyle::SP_DialogNoButton),
                                                  versionsIterator.value().Installed ? tr("Installed") : tr("Not Installed")));
            /** Description */
            child_items->append(new QStandardItem());
            /** License */
            child_items->append(new QStandardItem());
            /** Sha */
            child_items->append(new QStandardItem(versionsIterator.value().Sha));

            for (const auto &i : qAsConst(*child_items))
            {
                i->setEditable(false);
            }

            item->appendRow(*child_items);
            ++versionsIterator;
        }

        for (const auto &i : qAsConst(*items))
        {
            i->setEditable(false);
        }

        ++iterator;
    }

    return items;
}

void DialogPackageManager::initTreeView()
{
    tableViewProxyModel_ = new QSortFilterProxyModel(this);
    QStandardItemModel *model = new QStandardItemModel(ui_->treeView);
    model->setColumnCount(PACKAGE_INFO_ID_COUNT);
    model->setHeaderData(PACKAGE_INFO_ID_NAME, Qt::Horizontal, tr("Name"));
    model->setHeaderData(PACKAGE_INFO_ID_SIZE, Qt::Horizontal, tr("Size"));
    model->setHeaderData(PACKAGE_INFO_ID_HOMEPAGE, Qt::Horizontal, tr("Home Page"));
    model->setHeaderData(PACKAGE_INFO_ID_STATUS, Qt::Horizontal, tr("Status"));
    model->setHeaderData(PACKAGE_INFO_ID_DESCRIPTION, Qt::Horizontal, tr("Description"));
    model->setHeaderData(PACKAGE_INFO_ID_LICENSE, Qt::Horizontal, tr("License"));
    model->setHeaderData(PACKAGE_INFO_ID_SHA, Qt::Horizontal, tr("Sha"));

    ToolCspRepo::PackageType packages;
    ToolCspRepo::loadPackages(&packages);

    const QMap<QString, ToolCspRepo::InformationType> *library = &packages["Library"];
    const QMap<QString, ToolCspRepo::InformationType> *toolchains = &packages["Toolchains"];

    QStandardItem *const libraryItem = new QStandardItem("Library");
    QStandardItem *const toolchainsItem = new QStandardItem("Toolchains");

    libraryItem->appendRow(*createPackageInfoItems(library));
    toolchainsItem->appendRow(*createPackageInfoItems(toolchains));

    model->appendRow(libraryItem);
    model->appendRow(toolchainsItem);

    connect(model, &QStandardItemModel::itemChanged, this, &DialogPackageManager::treeViewModelItemChangedCallback, Qt::UniqueConnection);
    tableViewProxyModel_->setSourceModel(model);

    delete ui_->treeView->model();
    ui_->treeView->setModel(tableViewProxyModel_);
    ui_->treeView->expandAll();
    ui_->treeView->header()->setMinimumSectionSize(10);
    ui_->treeView->header()->setSectionResizeMode(QHeaderView::Interactive);
    ui_->treeView->header()->setSectionsMovable(false);
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

            updatePushButtonInstallUpdateUninstallStatus();
        }
    }
    connect(dynamic_cast<QStandardItemModel *>(tableViewProxyModel_->sourceModel()), &QStandardItemModel::itemChanged, this, &DialogPackageManager::treeViewModelItemChangedCallback, Qt::UniqueConnection);
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
                        if (parent->isCheckable())
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
                            selectedPackageInfos_.insert(name, { parent->parent()->text(), version, status == tr("Installed"), item->row(), parent });
                        }
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

void DialogPackageManager::pushButtonInstallPressedCallback()
{
    runCspRepoCommand("install");
    updatePushButtonInstallUpdateUninstallStatus();
}

void DialogPackageManager::pushButtonUpdatePressedCallback()
{
    runCspRepoCommand("update");
    updatePushButtonInstallUpdateUninstallStatus();
}

void DialogPackageManager::pushButtonUninstallPressedCallback()
{
    runCspRepoCommand("uninstall");
    updatePushButtonInstallUpdateUninstallStatus();
}

void DialogPackageManager::runCspRepoCommand(const QString &command) const
{
    auto infoIterator = selectedPackageInfos_.constBegin();
    while (infoIterator != selectedPackageInfos_.constEnd())
    {
        const QString &name = infoIterator.key();
        const QString &type = infoIterator.value().Type;
        const QString &version = infoIterator.value().Version;
        const QStandardItem *parent = infoIterator.value().Parent;
        const int row = infoIterator.value().Row;
        const bool installed = infoIterator.value().Installed;

        QFuture<int> future;
        bool isMatched;

        /** install */
        if (!installed && command == "install")
        {
            isMatched = true;
            future = QtConcurrent::run([name, version] {
                const int errorCode = ToolCspRepo::installPackage(name, version);
                return errorCode;
            });
        }
        /** update */
        else if (installed && version == "latest" && command == "update")
        {
            isMatched = true;
            future = QtConcurrent::run([name] {
                const int errorCode = ToolCspRepo::updatePackage(name);
                return errorCode;
            });
        }
        /** uninstall */
        else if (installed && command == "uninstall")
        {
            isMatched = true;
            future = QtConcurrent::run([name, version] {
                const int errorCode = ToolCspRepo::uninstallPackage(name, version);
                return errorCode;
            });
        }
        else
        {
            isMatched = false;
            qWarning().noquote() << QString("Invalid command : \"%1\"").arg(command);
            future = QtConcurrent::run([] {
                return 0;
            });
        }

        if (isMatched)
        {
            QApplication::setOverrideCursor(Qt::WaitCursor);
            ui_->progressBar->setHidden(false);
            while (!future.isFinished())
            {
                QApplication::processEvents();
            }
            ui_->progressBar->setHidden(true);
            future.waitForFinished();
            QApplication::restoreOverrideCursor();
            if (future.result() == 0)
            {
                ui_->labelStatus->setText(QString("%1 %2 successful").arg(name, command));
                ToolCspRepo::PackageType packages;
                ToolCspRepo::loadPackages(&packages, name);
                const ToolCspRepo::VersionType &versionInfo = packages[type][name].Versions[version];
                parent->child(row, PACKAGE_INFO_ID_SIZE)->setText(QString::number(versionInfo.Size, 'f', 2));
                parent->child(row, PACKAGE_INFO_ID_STATUS)->setIcon(QApplication::style()->standardIcon(versionInfo.Installed ? QStyle::SP_DialogYesButton : QStyle::SP_DialogNoButton));
                parent->child(row, PACKAGE_INFO_ID_STATUS)->setText(versionInfo.Installed ? tr("Installed") : tr("Not Installed"));
                parent->child(row, PACKAGE_INFO_ID_SHA)->setText(versionInfo.Sha);
            }
            else
            {
                ui_->labelStatus->setText(QString("%1 %2 failure").arg(name, command));
                break;
            }
        }

        ++infoIterator;
    }
}
