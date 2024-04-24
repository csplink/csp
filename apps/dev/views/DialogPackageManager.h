/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        DialogPackageManager.h
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

#ifndef DIALOG_PACKAGE_MANAGER_H
#define DIALOG_PACKAGE_MANAGER_H

#include <QDialog>
#include <QMap>
#include <QSortFilterProxyModel>
#include <QStandardItem>

#include "ToolCspRepo.h"

namespace Ui
{
class dialogPackageManager;
}

class DialogPackageManager final : public QDialog
{
    Q_OBJECT

  public:
    explicit DialogPackageManager(QWidget *parent = nullptr);
    ~DialogPackageManager() override;

  private:
    typedef enum
    {
        PACKAGE_INFO_ID_NAME = 0,
        PACKAGE_INFO_ID_SIZE,
        PACKAGE_INFO_ID_HOMEPAGE,
        PACKAGE_INFO_ID_STATUS,
        PACKAGE_INFO_ID_DESCRIPTION,
        PACKAGE_INFO_ID_LICENSE,
        PACKAGE_INFO_ID_SHA,
        PACKAGE_INFO_ID_COUNT,
    } PackageInfoIdType;

    typedef struct
    {
        QString Type;
        QString Version;
        bool Installed;
        int Row;
        const QStandardItem *Parent;
    } PackageInfoType;

    Ui::dialogPackageManager *ui_;
    QSortFilterProxyModel *tableViewProxyModel_ = nullptr;
    QMap<QString, PackageInfoType> selectedPackageInfos_;
    int installCount_ = 0;
    int uninstallCount_ = 0;
    int updateCount_ = 0;
    QFontMetrics *fontMetrics_;

    void initTreeView();
    Qt::CheckState treeViewItemSiblingCheckState(const QStandardItem *item) const;
    void updatePushButtonInstallUpdateUninstallStatus();
    void runCspRepoCommand(const QString &command) const;

    QList<QStandardItem *> *createPackageInfoItems(const QMap<QString, ToolCspRepo::InformationType> *Packages);

  private slots:
    void treeViewModelItemChangedCallback(QStandardItem *item);
    void toolButtonCollapsePressedCallback() const;
    void toolButtonExpandPressedCallback() const;

    void pushButtonClosePressedCallback();
    void pushButtonInstallPressedCallback();
    void pushButtonUpdatePressedCallback();
    void pushButtonUninstallPressedCallback();
};

#endif /** DIALOG_PACKAGE_MANAGER_H */
