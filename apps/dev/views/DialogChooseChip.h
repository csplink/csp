/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        DialogChooseChip.h
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

#include "Project.h"
#include "repo.h"

namespace Ui
{
class dialogChooseChip;
}

class DialogChooseChip final : public QDialog
{
    Q_OBJECT

  public:
    explicit DialogChooseChip(QWidget *parent = nullptr);
    ~DialogChooseChip() override;

  signals:
    void signalsCreateProject();

  private slots:
    void treeViewChipFilterModelItemChangedCallback(const QStandardItem *item) const;
    void tableViewChipInfosSelectionModelSelectionChangedCallback(const QItemSelection &selected,
                                                                  const QItemSelection &deselected);
    void dialogButtonBoxClickedCallback(const QAbstractButton *button);
    void pushButtonNamePressedCallback() const;
    void pushButtonCompanyPressedCallback() const;

  private:
    Ui::dialogChooseChip *ui_;
    repo *repoInstance_;
    Project *projectInstance_ = nullptr;

    QString chipName_;
    QString halName_;
    QString packageName_;
    QString companyName_;

    QStringList companyKeys_;
    QStringList seriesKeys_;
    QStringList lineKeys_;
    QStringList coreKeys_;
    QStringList packageKeys_;

    QStandardItem *companyRoot_ = nullptr;
    QStandardItem *seriesRoot_ = nullptr;
    QStandardItem *lineRoot_ = nullptr;
    QStandardItem *coreRoot_ = nullptr;
    QStandardItem *packageRoot_ = nullptr;

    QList<QStandardItem *> companyItems_;
    QList<QStandardItem *> seriesItems_;
    QList<QStandardItem *> lineItems_;
    QList<QStandardItem *> coreItems_;
    QList<QStandardItem *> packageItems_;

    QList<QList<QStandardItem *> *> chipsItems_;
    QSortFilterProxyModel *tableViewChipInfosProxyModel_ = nullptr;
    QList<repository_table::chip_info_t *> chips_;

    void findAllKeys();
    void initTreeViewChipFilter();
    void initTableViewChipInfos();
    void setChipsInfoUi(const QModelIndexList &selected_indexes);
};

#endif /** DIALOG_CHOOSE_CHIP_H */
