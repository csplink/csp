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

#include "RepositoryTable.h"

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

  private slots:
    void slotTreeViewChipFilterModelItemChanged(const QStandardItem *item) const;
    void slotTableViewChipInfosSelectionModelSelectionChanged(const QItemSelection &selected,
                                                              const QItemSelection &deselected);
    void slotDialogButtonBoxClicked(const QAbstractButton *button);
    void slotPushButtonNamePressed() const;
    void slotPushButtonVendorPressed() const;

  private:
    Ui::dialogChooseChip *ui;

    QString m_chipName;
    QString m_halName;
    QString m_packageName;
    QString m_vendorName;

    QStringList m_vendorKeys;
    QStringList m_seriesKeys;
    QStringList m_lineKeys;
    QStringList m_coreKeys;
    QStringList m_packageKeys;

    QStandardItem *m_vendorRoot = nullptr;
    QStandardItem *m_seriesRoot = nullptr;
    QStandardItem *m_lineRoot = nullptr;
    QStandardItem *m_coreRoot = nullptr;
    QStandardItem *m_packageRoot = nullptr;

    QList<QStandardItem *> m_vendorItems;
    QList<QStandardItem *> m_seriesItems;
    QList<QStandardItem *> m_lineItems;
    QList<QStandardItem *> m_coreItems;
    QList<QStandardItem *> m_packageItems;

    QList<QList<QStandardItem *> *> m_chipsItems;
    QSortFilterProxyModel *m_tableViewChipInfosProxyModel = nullptr;
    QList<RepositoryTable::ChipInfoType> m_chips;

    void findAllKeys();
    void initTreeViewChipFilter();
    void initTableViewChipInfos();
    void setChipsInfoUi(const QModelIndexList &selectedIndex);
};

#endif /** DIALOG_CHOOSE_CHIP_H */
