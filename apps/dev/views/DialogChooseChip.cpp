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

#include <QDebug>
#include <QDesktopServices>

#include "DialogChooseChip.h"
#include "WizardNewProject.h"
#include "ui_DialogChooseChip.h"

DialogChooseChip::DialogChooseChip(QWidget *parent)
    : QDialog(parent), ui_(new Ui::dialogChooseChip)
{
    ui_->setupUi(this);

    repoInstance_ = Repo::getInstance();
    projectInstance_ = Project::getInstance();

    ui_->splitter_2->setSizes(QList<int>() << 156 << 1102);
    ui_->dialogButtonBox->button(QDialogButtonBox::Ok)->setText(tr("Create"));
    ui_->dialogButtonBox->button(QDialogButtonBox::Cancel)->setText(tr("Cancel"));

    setWindowFlags(Qt::Dialog | Qt::WindowCloseButtonHint | Qt::WindowMinimizeButtonHint |
                   Qt::WindowMaximizeButtonHint);
    setWindowState(Qt::WindowMaximized);

    connect(ui_->dialogButtonBox, &QDialogButtonBox::clicked, this, &DialogChooseChip::dialogButtonBoxClickedCallback, Qt::UniqueConnection);
    connect(ui_->pushButtonName, &QPushButton::pressed, this, &DialogChooseChip::pushButtonNamePressedCallback, Qt::UniqueConnection);
    connect(ui_->pushButtonCompany, &QPushButton::pressed, this, &DialogChooseChip::pushButtonCompanyPressedCallback, Qt::UniqueConnection);
    connect(ui_->dialogButtonBox, &QDialogButtonBox::accepted, this, &DialogChooseChip::accept, Qt::UniqueConnection);
    connect(ui_->dialogButtonBox, &QDialogButtonBox::rejected, this, &DialogChooseChip::reject, Qt::UniqueConnection);

    findAllKeys();
    initTreeViewChipFilter();
    initTableViewChipInfos();
}

DialogChooseChip::~DialogChooseChip()
{
    delete ui_;
}

void DialogChooseChip::findAllKeys()
{
    const auto repository = repoInstance_->getRepository();
    const auto chips = &repository->Chips;
    auto chips_i = chips->constBegin();
    while (chips_i != chips->constEnd())
    {
        auto company_name = chips_i.key();
        if (!companyKeys_.contains(company_name))
            companyKeys_ << company_name;

        const auto company = &chips_i.value();
        auto company_i = company->constBegin();
        while (company_i != company->constEnd())
        {
            auto series_name = company_i.key();
            if (!seriesKeys_.contains(series_name))
                seriesKeys_ << series_name;

            const auto series = &company_i.value();
            auto series_i = series->constBegin();
            while (series_i != series->constEnd())
            {
                auto line_name = series_i.key();
                if (!lineKeys_.contains(line_name))
                    lineKeys_ << line_name;

                const auto line = &series_i.value();
                auto line_i = line->constBegin();
                while (line_i != line->constEnd())
                {
                    auto mcu = const_cast<RepositoryTable::ChipInfoType *>(&line_i.value());
                    if (!coreKeys_.contains(mcu->Core))
                        coreKeys_ << mcu->Core;
                    if (!packageKeys_.contains(mcu->Package))
                        packageKeys_ << mcu->Package;

                    mcu->Name = line_i.key();
                    mcu->Company = company_name;
                    mcu->Series = series_name;
                    mcu->Line = line_name;
                    chips_.append(mcu);

                    ++line_i;
                }
                ++series_i;
            }
            ++company_i;
        }
        ++chips_i;
    }
}

void DialogChooseChip::initTreeViewChipFilter()
{
    companyRoot_ = new QStandardItem(tr("Company"));
    seriesRoot_ = new QStandardItem(tr("Series"));
    lineRoot_ = new QStandardItem(tr("Line"));
    coreRoot_ = new QStandardItem(tr("Core"));
    packageRoot_ = new QStandardItem(tr("Package"));

    companyRoot_->setCheckable(true);
    seriesRoot_->setCheckable(true);
    lineRoot_->setCheckable(true);
    coreRoot_->setCheckable(true);
    packageRoot_->setCheckable(true);

    auto *model = new QStandardItemModel(ui_->treeViewChipFilter);
    model->setHorizontalHeaderLabels(QStringList(tr("Chip Filter")));

    model->appendRow(companyRoot_);
    model->appendRow(seriesRoot_);
    model->appendRow(lineRoot_);
    model->appendRow(coreRoot_);
    model->appendRow(packageRoot_);

    QStringList::const_iterator iter;
    for (iter = companyKeys_.constBegin(); iter != companyKeys_.constEnd(); ++iter)
    {
        const QString &str = *iter;
        auto *item = new QStandardItem(str);
        item->setCheckable(true);
        companyItems_.append(item);
    }
    companyRoot_->appendRows(companyItems_);

    for (iter = seriesKeys_.constBegin(); iter != seriesKeys_.constEnd(); ++iter)
    {
        const QString &str = *iter;
        auto *item = new QStandardItem(str);
        item->setCheckable(true);
        seriesItems_.append(item);
    }
    seriesRoot_->appendRows(seriesItems_);

    for (iter = lineKeys_.constBegin(); iter != lineKeys_.constEnd(); ++iter)
    {
        const QString &str = *iter;
        auto *item = new QStandardItem(str);
        item->setCheckable(true);
        lineItems_.append(item);
    }
    lineRoot_->appendRows(lineItems_);

    for (iter = coreKeys_.constBegin(); iter != coreKeys_.constEnd(); ++iter)
    {
        const QString &str = *iter;
        auto *item = new QStandardItem(str);
        item->setCheckable(true);
        coreItems_.append(item);
    }
    coreRoot_->appendRows(coreItems_);

    for (iter = packageKeys_.constBegin(); iter != packageKeys_.constEnd(); ++iter)
    {
        const QString &str = *iter;
        auto *item = new QStandardItem(str);
        item->setCheckable(true);
        packageItems_.append(item);
    }
    packageRoot_->appendRows(packageItems_);

    delete ui_->treeViewChipFilter->model();
    ui_->treeViewChipFilter->setModel(model);
    ui_->treeViewChipFilter->expandAll();

    connect(model, &QStandardItemModel::itemChanged, this,
            &DialogChooseChip::treeViewChipFilterModelItemChangedCallback, Qt::QueuedConnection);
}

void DialogChooseChip::treeViewChipFilterModelItemChangedCallback(const QStandardItem *item) const
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
    tableViewChipInfosProxyModel_ = new QSortFilterProxyModel(this);
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

    for (QList<RepositoryTable::ChipInfoType *>::const_iterator iter = chips_.constBegin(); iter != chips_.constEnd();
         ++iter)
    {
        auto chips_item = new QList<QStandardItem *>();
        chips_item->append(new QStandardItem((*iter)->Name));
        chips_item->append(new QStandardItem(tr("Unavailable")));
        chips_item->append(new QStandardItem(tr("Unavailable")));
        chips_item->append(new QStandardItem((*iter)->Package));
        chips_item->append(new QStandardItem(QString::number((*iter)->Flash, 'f', 2)));
        chips_item->append(new QStandardItem(QString::number((*iter)->Ram, 'f', 2)));
        chips_item->append(new QStandardItem(QString::number((*iter)->IO, 10)));
        chips_item->append(new QStandardItem(QString::number((*iter)->Frequency, 'f', 2)));
        chips_item->append(new QStandardItem((*iter)->Company));
        chips_item->append(new QStandardItem((*iter)->Core));
        chipsItems_.append(chips_item);

        for (const auto &item : *chips_item)
            item->setEditable(false);

        model->appendRow(*chips_item);
        chipsItems_.append(chips_item);
    }
    tableViewChipInfosProxyModel_->setSourceModel(model);

    delete ui_->tableViewChipInfos->model();
    ui_->tableViewChipInfos->setModel(tableViewChipInfosProxyModel_);
    ui_->tableViewChipInfos->setSelectionBehavior(QAbstractItemView::SelectRows);
    ui_->tableViewChipInfos->setSelectionMode(QAbstractItemView::SingleSelection);
    ui_->tableViewChipInfos->setSortingEnabled(true);
    ui_->tableViewChipInfos->sortByColumn(0, Qt::AscendingOrder);
    ui_->tableViewChipInfos->horizontalHeader()->setMinimumSectionSize(10);
    ui_->tableViewChipInfos->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    connect(ui_->tableViewChipInfos->selectionModel(), &QItemSelectionModel::selectionChanged, this,
            &DialogChooseChip::tableViewChipInfosSelectionModelSelectionChangedCallback, Qt::UniqueConnection);
}

void DialogChooseChip::tableViewChipInfosSelectionModelSelectionChangedCallback(
    const QItemSelection &selected, const QItemSelection &deselected)
{
    Q_UNUSED(deselected)
    setChipsInfoUi(selected.indexes());
}

void DialogChooseChip::setChipsInfoUi(const QModelIndexList &selected_indexes)
{
    if (selected_indexes.isEmpty())
        return;

    chipName_ = selected_indexes[0].data().toString();
    const auto market_status = selected_indexes[1].data().toString();
    const auto price = selected_indexes[2].data().toString();
    const auto package = selected_indexes[3].data().toString();
    const auto company = selected_indexes[8].data().toString();
    const auto package_path = QString(":/packages/%1.png").arg(package);

    ui_->labelMarketStatus->setText(market_status);
    ui_->labelPrice->setText(price);
    ui_->labelPackage->setText(package);
    ui_->pushButtonName->setText(chipName_);
    ui_->pushButtonCompany->setText(company);

    QPixmap image;
    if (QFile::exists(package_path))
    {
        image = QPixmap(package_path);
    }
    else
    {
        image = QPixmap(":/packages/unknown.png");
    }
    ui_->labelPackageImage->setPixmap(image);

    if (Repo::chipSummaryExists(company, chipName_))
    {
        ChipSummaryTable::ChipSummaryType chip_summary;
        Repo::loadChipSummary(&chip_summary, company, chipName_);
        halName_ = chip_summary.Hal;
        packageName_ = chip_summary.Package;
        companyName_ = company;

        ui_->textBrowserReadme->setMarkdown(QString("# %1\n\n").arg(chipName_) +
                                            chip_summary.Illustrate[Config::language()]);
        ui_->pushButtonName->setProperty("user_url", chip_summary.Url[Config::language()]);
        ui_->pushButtonCompany->setProperty("user_url", chip_summary.CompanyUrl[Config::language()]);
    }
    else
    {
        halName_ = QString();
        packageName_ = QString();
        companyName_ = QString();

        ui_->textBrowserReadme->setMarkdown(QString("# %1\n\n").arg(chipName_) +
                                            tr("The chip description file <%1.yml> does not exist").arg(chipName_));
        ui_->pushButtonName->setProperty("user_url", "");
        ui_->pushButtonCompany->setProperty("user_url", "");
    }
}

void DialogChooseChip::dialogButtonBoxClickedCallback(const QAbstractButton *button)
{
    if (button == nullptr)
        return;

    if (button->text() == tr("Create"))
    {
        if (chipName_.isEmpty())
        {
            qWarning().noquote() << tr("Please choose a chip.");
            return;
        }

        if (halName_.isEmpty() || packageName_.isEmpty() || companyName_.isEmpty())
        {
            qWarning().noquote() << tr("The chip description file <%1.yml> does not exist").arg(chipName_);
            return;
        }

        WizardNewProject wizard(this);
        connect(&wizard, &WizardNewProject::finished, this, [this](const int result) {
            if (result == QDialog::Accepted)
            {
                projectInstance_->setProjectHal(halName_);
                projectInstance_->setProjectTargetChip(chipName_);
                projectInstance_->setProjectPackage(packageName_);
                projectInstance_->setProjectCompany(companyName_);
                projectInstance_->setProjectType("chip");
                emit signalsCreateProject();
            }
        });
        wizard.exec();
    }
}

void DialogChooseChip::pushButtonNamePressedCallback() const
{
    const auto url = ui_->pushButtonName->property("user_url").toString();
    if (!url.isEmpty())
    {
        QDesktopServices::openUrl(QUrl(url));
    }
}

void DialogChooseChip::pushButtonCompanyPressedCallback() const
{
    const auto url = ui_->pushButtonCompany->property("user_url").toString();
    if (!url.isEmpty())
    {
        QDesktopServices::openUrl(QUrl(url));
    }
}
