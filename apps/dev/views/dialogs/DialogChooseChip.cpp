/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        DialogChooseChip.cpp
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

#include <QDesktopServices>

#include "DialogChooseChip.h"
#include "Project.h"
#include "Repo.h"
#include "WizardNewProject.h"
#include "ui_DialogChooseChip.h"

DialogChooseChip::DialogChooseChip(QWidget *parent)
    : QDialog(parent),
      ui(new Ui::dialogChooseChip)
{
    ui->setupUi(this);

    ui->splitter_2->setSizes({156, 1102});
    ui->dialogButtonBox->button(QDialogButtonBox::Ok)->setText(tr("Create"));
    ui->dialogButtonBox->button(QDialogButtonBox::Cancel)->setText(tr("Cancel"));

    setWindowFlags(Qt::Dialog | Qt::WindowCloseButtonHint | Qt::WindowMinimizeButtonHint |
                   Qt::WindowMaximizeButtonHint);
    setWindowState(Qt::WindowMaximized);

    connect(ui->dialogButtonBox, &QDialogButtonBox::clicked, this, &DialogChooseChip::slotDialogButtonBoxClicked);
    connect(ui->pushButtonName, &QPushButton::pressed, this, &DialogChooseChip::slotPushButtonNamePressed);
    connect(ui->pushButtonCompany, &QPushButton::pressed, this, &DialogChooseChip::slotPushButtonCompanyPressed);
    connect(ui->dialogButtonBox, &QDialogButtonBox::accepted, this, &DialogChooseChip::accept);
    connect(ui->dialogButtonBox, &QDialogButtonBox::rejected, this, &DialogChooseChip::reject);

    findAllKeys();
    initTreeViewChipFilter();
    initTableViewChipInfos();
}

DialogChooseChip::~DialogChooseChip()
{
    delete ui;
}

void DialogChooseChip::findAllKeys()
{
    RepositoryTable::RepositoryType repository = Repo.getRepository();
    RepositoryTable::ChipType &chips = repository.Chips;
    QMap<QString, RepositoryTable::ChipCompanyType>::iterator chipsI = chips.begin();
    while (chipsI != chips.end())
    {
        const QString companyName = chipsI.key();
        if (!m_companyKeys.contains(companyName))
        {
            m_companyKeys << companyName;
        }

        RepositoryTable::ChipCompanyType &company = chipsI.value();
        QMap<QString, RepositoryTable::ChipSeriesType>::iterator companyI = company.begin();
        while (companyI != company.end())
        {
            const QString seriesName = companyI.key();
            if (!m_seriesKeys.contains(seriesName))
            {
                m_seriesKeys << seriesName;
            }

            RepositoryTable::ChipSeriesType &series = companyI.value();
            QMap<QString, RepositoryTable::ChipLineType>::iterator seriesI = series.begin();
            while (seriesI != series.end())
            {
                const QString lineName = seriesI.key();
                if (!m_lineKeys.contains(lineName))
                {
                    m_lineKeys << lineName;
                }

                RepositoryTable::ChipLineType &line = seriesI.value();
                QMap<QString, RepositoryTable::ChipInfoType>::iterator lineI = line.begin();
                while (lineI != line.end())
                {
                    RepositoryTable::ChipInfoType &chip = lineI.value();
                    if (!m_coreKeys.contains(chip.Core))
                    {
                        m_coreKeys << chip.Core;
                    }
                    if (!m_packageKeys.contains(chip.Package))
                    {
                        m_packageKeys << chip.Package;
                    }

                    chip.Name = lineI.key();
                    chip.Company = companyName;
                    chip.Series = seriesName;
                    chip.Line = lineName;
                    m_chips.append(chip);

                    ++lineI;
                }
                ++seriesI;
            }
            ++companyI;
        }
        ++chipsI;
    }
}

void DialogChooseChip::initTreeViewChipFilter()
{
    m_companyRoot = new QStandardItem(tr("Company"));
    m_seriesRoot = new QStandardItem(tr("Series"));
    m_lineRoot = new QStandardItem(tr("Line"));
    m_coreRoot = new QStandardItem(tr("Core"));
    m_packageRoot = new QStandardItem(tr("Package"));

    m_companyRoot->setCheckable(true);
    m_seriesRoot->setCheckable(true);
    m_lineRoot->setCheckable(true);
    m_coreRoot->setCheckable(true);
    m_packageRoot->setCheckable(true);

    auto *model = new QStandardItemModel(ui->treeViewChipFilter);
    model->setHorizontalHeaderLabels(QStringList(tr("Chip Filter")));

    model->appendRow(m_companyRoot);
    model->appendRow(m_seriesRoot);
    model->appendRow(m_lineRoot);
    model->appendRow(m_coreRoot);
    model->appendRow(m_packageRoot);

    QStringList::const_iterator iter;
    for (iter = m_companyKeys.constBegin(); iter != m_companyKeys.constEnd(); ++iter)
    {
        const QString &str = *iter;
        auto *item = new QStandardItem(str);
        item->setCheckable(true);
        m_companyItems.append(item);
    }
    m_companyRoot->appendRows(m_companyItems);

    for (iter = m_seriesKeys.constBegin(); iter != m_seriesKeys.constEnd(); ++iter)
    {
        const QString &str = *iter;
        auto *item = new QStandardItem(str);
        item->setCheckable(true);
        m_seriesItems.append(item);
    }
    m_seriesRoot->appendRows(m_seriesItems);

    for (iter = m_lineKeys.constBegin(); iter != m_lineKeys.constEnd(); ++iter)
    {
        const QString &str = *iter;
        auto *item = new QStandardItem(str);
        item->setCheckable(true);
        m_lineItems.append(item);
    }
    m_lineRoot->appendRows(m_lineItems);

    for (iter = m_coreKeys.constBegin(); iter != m_coreKeys.constEnd(); ++iter)
    {
        const QString &str = *iter;
        auto *item = new QStandardItem(str);
        item->setCheckable(true);
        m_coreItems.append(item);
    }
    m_coreRoot->appendRows(m_coreItems);

    for (iter = m_packageKeys.constBegin(); iter != m_packageKeys.constEnd(); ++iter)
    {
        const QString &str = *iter;
        auto *item = new QStandardItem(str);
        item->setCheckable(true);
        m_packageItems.append(item);
    }
    m_packageRoot->appendRows(m_packageItems);

    delete ui->treeViewChipFilter->model();
    ui->treeViewChipFilter->setModel(model);
    ui->treeViewChipFilter->expandAll();

    connect(model, &QStandardItemModel::itemChanged, this, &DialogChooseChip::slotTreeViewChipFilterModelItemChanged,
            Qt::QueuedConnection);
}

void DialogChooseChip::slotTreeViewChipFilterModelItemChanged(const QStandardItem *item) const
{
    if (item == nullptr)
        return;

    const auto row_count = item->rowCount();
    if (row_count > 0) // root item
    {
        for (int i = 0; i < row_count; ++i)
        {
            auto *child_item = item->child(i);
            if (child_item == nullptr)
                continue;

            if (item->checkState() == Qt::Checked)
                child_item->setCheckState(Qt::Checked);
            else if (item->checkState() == Qt::Unchecked)
                child_item->setCheckState(Qt::Unchecked);
        }
    }
    else // root item's child
    {
        QStandardItem *parent = item->parent();
        const auto count = parent->rowCount();
        auto checked_count = 0;
        for (int i = 0; i < count; ++i)
        {
            const auto *child_item = parent->child(i);
            if (child_item == nullptr)
                continue;
            if (child_item->checkState() == Qt::Checked)
                checked_count++;
        }
        if (checked_count == count)
            parent->setCheckState(Qt::Checked);
        else if (checked_count == 0)
            parent->setCheckState(Qt::Unchecked);
        else
            parent->setCheckState(Qt::PartiallyChecked);
    }
}

void DialogChooseChip::initTableViewChipInfos()
{
    m_tableViewChipInfosProxyModel = new QSortFilterProxyModel(this);
    const auto model = new QStandardItemModel(this);
    /*设置列字段名*/
    model->setColumnCount(10);
    model->setHeaderData(0, Qt::Horizontal, tr("Name"));
    model->setHeaderData(1, Qt::Horizontal, tr("Market status"));
    model->setHeaderData(2, Qt::Horizontal, tr("Unit price for 10kU"));
    model->setHeaderData(3, Qt::Horizontal, tr("Package"));
    model->setHeaderData(4, Qt::Horizontal, tr("Flash"));
    model->setHeaderData(5, Qt::Horizontal, tr("RAM"));
    model->setHeaderData(6, Qt::Horizontal, tr("IO"));
    model->setHeaderData(7, Qt::Horizontal, tr("Frequency"));
    model->setHeaderData(8, Qt::Horizontal, tr("Company"));
    model->setHeaderData(9, Qt::Horizontal, tr("Core"));

    for (const RepositoryTable::ChipInfoType &chip : qAsConst(m_chips))
    {
        auto chips_item = new QList<QStandardItem *>();
        chips_item->append(new QStandardItem(chip.Name));
        chips_item->append(new QStandardItem(tr("Unavailable")));
        chips_item->append(new QStandardItem(tr("Unavailable")));
        chips_item->append(new QStandardItem(chip.Package));
        chips_item->append(new QStandardItem(QString::number(chip.Flash, 'f', 2)));
        chips_item->append(new QStandardItem(QString::number(chip.Ram, 'f', 2)));
        chips_item->append(new QStandardItem(QString::number(chip.IO, 10)));
        chips_item->append(new QStandardItem(QString::number(chip.Frequency, 'f', 2)));
        chips_item->append(new QStandardItem(chip.Company));
        chips_item->append(new QStandardItem(chip.Core));
        m_chipsItems.append(chips_item);

        for (const auto &item : qAsConst(*chips_item))
            item->setEditable(false);

        model->appendRow(*chips_item);
        m_chipsItems.append(chips_item);
    }
    m_tableViewChipInfosProxyModel->setSourceModel(model);

    delete ui->tableViewChipInfos->model();
    ui->tableViewChipInfos->setModel(m_tableViewChipInfosProxyModel);
    ui->tableViewChipInfos->setSelectionBehavior(QAbstractItemView::SelectRows);
    ui->tableViewChipInfos->setSelectionMode(QAbstractItemView::SingleSelection);
    ui->tableViewChipInfos->setSortingEnabled(true);
    ui->tableViewChipInfos->sortByColumn(0, Qt::AscendingOrder);
    ui->tableViewChipInfos->horizontalHeader()->setMinimumSectionSize(10);
    ui->tableViewChipInfos->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    connect(ui->tableViewChipInfos->selectionModel(), &QItemSelectionModel::selectionChanged, this,
            &DialogChooseChip::slotTableViewChipInfosSelectionModelSelectionChanged, Qt::UniqueConnection);
}

void DialogChooseChip::slotTableViewChipInfosSelectionModelSelectionChanged(const QItemSelection &selected,
                                                                            const QItemSelection &deselected)
{
    Q_UNUSED(deselected)
    setChipsInfoUi(selected.indexes());
}

void DialogChooseChip::setChipsInfoUi(const QModelIndexList &selectedIndex)
{
    if (selectedIndex.isEmpty())
        return;

    m_chipName = selectedIndex[0].data().toString();
    const auto marketStatus = selectedIndex[1].data().toString();
    const auto price = selectedIndex[2].data().toString();
    const auto package = selectedIndex[3].data().toString();
    const auto company = selectedIndex[8].data().toString();
    const auto packagePath = QString(":/packages/%1.png").arg(package);

    ui->labelMarketStatus->setText(marketStatus);
    ui->labelPrice->setText(price);
    ui->labelPackage->setText(package);
    ui->pushButtonName->setText(m_chipName);
    ui->pushButtonCompany->setText(company);

    QPixmap image;
    if (QFile::exists(packagePath))
    {
        image = QPixmap(packagePath);
    }
    else
    {
        image = QPixmap(":/packages/unknown.png");
    }
    ui->labelPackageImage->setPixmap(image);

    if (ChipSummaryTable::fileExists(company, m_chipName))
    {
        ChipSummaryTable::ChipSummaryType chipSummary;
        ChipSummaryTable::loadChipSummary(&chipSummary, company, m_chipName);
        m_halName = chipSummary.Hal;
        m_packageName = chipSummary.Package;
        m_companyName = company;

        ui->textBrowserReadme->setMarkdown(QString("# %1\n\n").arg(m_chipName) +
                                           chipSummary.Illustrate[Settings.language()]);
        ui->pushButtonName->setProperty("user_url", chipSummary.Url[Settings.language()]);
        ui->pushButtonCompany->setProperty("user_url", chipSummary.CompanyUrl[Settings.language()]);
    }
    else
    {
        m_halName = QString();
        m_packageName = QString();
        m_companyName = QString();

        ui->textBrowserReadme->setMarkdown(QString("# %1\n\n").arg(m_chipName) +
                                           tr("The chip description file <%1.yml> does not exist").arg(m_chipName));
        ui->pushButtonName->setProperty("user_url", "");
        ui->pushButtonCompany->setProperty("user_url", "");
    }
}

void DialogChooseChip::slotDialogButtonBoxClicked(const QAbstractButton *button)
{
    if (button == nullptr)
        return;

    if (button->text() == tr("Create"))
    {
        if (m_chipName.isEmpty())
        {
            qWarning().noquote() << tr("Please choose a chip.");
            return;
        }

        if (m_halName.isEmpty() || m_packageName.isEmpty() || m_companyName.isEmpty())
        {
            qWarning().noquote() << tr("The chip description file <%1.yml> does not exist").arg(m_chipName);
            return;
        }

        WizardNewProject wizard(this);
        connect(&wizard, &WizardNewProject::finished, this, [this](const int result) {
            if (result == QDialog::Accepted)
            {
                Project.setHal(m_halName);
                Project.setTargetChip(m_chipName);
                Project.setPackage(m_packageName);
                Project.setCompany(m_companyName);
                Project.setType("chip");
                emit signalCreateProject();
            }
        });
        wizard.exec();
    }
}

void DialogChooseChip::slotPushButtonNamePressed() const
{
    const auto url = ui->pushButtonName->property("user_url").toString();
    if (!url.isEmpty())
    {
        QDesktopServices::openUrl(QUrl(url));
    }
}

void DialogChooseChip::slotPushButtonCompanyPressed() const
{
    const auto url = ui->pushButtonCompany->property("user_url").toString();
    if (!url.isEmpty())
    {
        QDesktopServices::openUrl(QUrl(url));
    }
}
