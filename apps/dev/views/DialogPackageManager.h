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
#include <QSortFilterProxyModel>
#include <QStandardItem>

#include "xmake.h"

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
    Ui::dialogPackageManager *ui_;
    QSortFilterProxyModel *tableViewProxyModel_ = nullptr;
    typedef struct
    {
        QString Version;
        bool Installed;
    } PackageInfoType;
    QMap<QString, PackageInfoType> selectedPackageInfos_;
    int installCount_ = 0;
    int uninstallCount_ = 0;
    int updateCount_ = 0;
    xmake *xmakeInstance_ = nullptr;

    void initTreeView();
    Qt::CheckState treeViewItemSiblingCheckState(const QStandardItem *item) const;
    void updatePushButtonInstallUpdateUninstallStatus();

  private slots:
    void treeViewModelItemChangedCallback(QStandardItem *item);
    void toolButtonCollapsePressedCallback() const;
    void toolButtonExpandPressedCallback() const;

    void pushButtonClosePressedCallback();
    void pushButtonInstallPressedCallback() const;
    void pushButtonUpdatePressedCallback() const;
    void pushButtonUninstallPressedCallback() const;
};

#endif /** DIALOG_PACKAGE_MANAGER_H */
