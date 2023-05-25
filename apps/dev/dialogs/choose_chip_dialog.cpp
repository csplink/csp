/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        choose_chip_dialog.cpp
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
#include <QPushButton>

#include "choose_chip_dialog.h"
#include "os.h"
#include "ui_choose_chip_dialog.h"

using namespace csp;

choose_chip_dialog::choose_chip_dialog(QWidget *parent) : QDialog(parent), ui(new Ui::choose_chip_dialog)
{
    ui->setupUi(this);
    ui->splitter_2->setSizes(QList<int>() << 156 << 1102);
    ui->dialogbuttonbox->button(QDialogButtonBox::Ok)->setText(tr("Create"));
    ui->dialogbuttonbox->button(QDialogButtonBox::Cancel)->setText(tr("Cancel"));
    setWindowState(Qt::WindowMaximized);

    connect(ui->dialogbuttonbox, &QDialogButtonBox::accepted, this, &choose_chip_dialog::accept, Qt::UniqueConnection);
    connect(ui->dialogbuttonbox, &QDialogButtonBox::rejected, this, &choose_chip_dialog::reject, Qt::UniqueConnection);

    _repo_instance = repo::get_instance();
    find_all_keys();
    init_treeview_chip_filter();
    init_tableview_chip_infos();
}

choose_chip_dialog::~choose_chip_dialog()
{
    delete ui;
}

void choose_chip_dialog::find_all_keys()
{
    auto repository = _repo_instance->get_repository();
    auto chips      = &repository->chips;
    auto chips_i    = chips->constBegin();
    while (chips_i != chips->constEnd())
    {
        auto company_name = chips_i.key();
        if (!_company_keys.contains(company_name))
            _company_keys << company_name;

        auto company   = &chips_i.value();
        auto company_i = company->constBegin();
        while (company_i != company->constEnd())
        {
            auto series_name = company_i.key();
            if (!_series_keys.contains(series_name))
                _series_keys << series_name;

            auto series   = &company_i.value();
            auto series_i = series->constBegin();
            while (series_i != series->constEnd())
            {
                auto line_name = series_i.key();
                if (!_line_keys.contains(line_name))
                    _line_keys << line_name;

                auto line   = &series_i.value();
                auto line_i = line->constBegin();
                while (line_i != line->constEnd())
                {
                    auto mcu = const_cast<repository_table::chip_info_t *>(&line_i.value());
                    if (!_core_keys.contains(mcu->core))
                        _core_keys << mcu->core;
                    if (!_package_keys.contains(mcu->package))
                        _package_keys << mcu->package;

                    mcu->name    = line_i.key();
                    mcu->company = company_name;
                    mcu->series  = series_name;
                    mcu->line    = line_name;
                    _chips.append(mcu);

                    line_i++;
                }
                series_i++;
            }
            company_i++;
        }
        chips_i++;
    }
}

void choose_chip_dialog::init_treeview_chip_filter()
{
    _company_root = new QStandardItem(tr("Company"));
    _series_root  = new QStandardItem(tr("Series"));
    _line_root    = new QStandardItem(tr("Line"));
    _core_root    = new QStandardItem(tr("Core"));
    _package_root = new QStandardItem(tr("Package"));

    _company_root->setCheckable(true);
    _series_root->setCheckable(true);
    _line_root->setCheckable(true);
    _core_root->setCheckable(true);
    _package_root->setCheckable(true);

    auto *model = new QStandardItemModel(ui->treeview_chip_filter);
    model->setHorizontalHeaderLabels(QStringList(tr("Chip Filter")));

    model->appendRow(_company_root);
    model->appendRow(_series_root);
    model->appendRow(_line_root);
    model->appendRow(_core_root);
    model->appendRow(_package_root);

    QStringList::const_iterator iter;
    for (iter = _company_keys.constBegin(); iter != _company_keys.constEnd(); ++iter)
    {
        const QString &str  = *iter;
        auto          *item = new QStandardItem(str);
        item->setCheckable(true);
        _company_items.append(item);
    }
    _company_root->appendRows(_company_items);

    for (iter = _series_keys.constBegin(); iter != _series_keys.constEnd(); ++iter)
    {
        const QString &str  = *iter;
        auto          *item = new QStandardItem(str);
        item->setCheckable(true);
        _series_items.append(item);
    }
    _series_root->appendRows(_series_items);

    for (iter = _line_keys.constBegin(); iter != _line_keys.constEnd(); ++iter)
    {
        const QString &str  = *iter;
        auto          *item = new QStandardItem(str);
        item->setCheckable(true);
        _line_items.append(item);
    }
    _line_root->appendRows(_line_items);

    for (iter = _core_keys.constBegin(); iter != _core_keys.constEnd(); ++iter)
    {
        const QString &str  = *iter;
        auto          *item = new QStandardItem(str);
        item->setCheckable(true);
        _core_items.append(item);
    }
    _core_root->appendRows(_core_items);

    for (iter = _package_keys.constBegin(); iter != _package_keys.constEnd(); ++iter)
    {
        const QString &str  = *iter;
        auto          *item = new QStandardItem(str);
        item->setCheckable(true);
        _package_items.append(item);
    }
    _package_root->appendRows(_package_items);

    ui->treeview_chip_filter->setModel(model);
    ui->treeview_chip_filter->expandAll();

    connect(model, &QStandardItemModel::itemChanged, this,
            &choose_chip_dialog::treeview_chip_filter_model_item_changed_callback, Qt::QueuedConnection);
}

void choose_chip_dialog::treeview_chip_filter_model_item_changed_callback(QStandardItem *item)
{
    if (item == nullptr)
        return;

    auto row_count = item->rowCount();
    if (row_count > 0)  // root item
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
    else  // root item's child
    {
        QStandardItem *parent        = item->parent();
        auto           count         = parent->rowCount();
        auto           checked_count = 0;
        for (int i = 0; i < count; ++i)
        {
            auto *child_item = parent->child(i);
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

void choose_chip_dialog::init_tableview_chip_infos()
{
    _tableview_chip_infos_proxy_model = new QSortFilterProxyModel(this);
    auto model                        = new QStandardItemModel(this);
    /*设置列字段名*/
    model->setColumnCount(10);
    model->setHeaderData(0, Qt::Horizontal, tr("Name"));
    model->setHeaderData(1, Qt::Horizontal, tr("Status"));
    model->setHeaderData(2, Qt::Horizontal, tr("Unit price for 10kU"));
    model->setHeaderData(3, Qt::Horizontal, tr("Package"));
    model->setHeaderData(4, Qt::Horizontal, tr("Flash"));
    model->setHeaderData(5, Qt::Horizontal, tr("RAM"));
    model->setHeaderData(6, Qt::Horizontal, tr("IO"));
    model->setHeaderData(7, Qt::Horizontal, tr("Frequency"));
    model->setHeaderData(8, Qt::Horizontal, tr("Company"));
    model->setHeaderData(9, Qt::Horizontal, tr("Core"));

    QList<repository_table::chip_info_t *>::const_iterator iter;
    for (iter = _chips.constBegin(); iter != _chips.constEnd(); ++iter)
    {
        auto chips_item = new QList<QStandardItem *>();
        chips_item->append(new QStandardItem((*iter)->name));
        chips_item->append(new QStandardItem(tr("Unavailable")));
        chips_item->append(new QStandardItem(tr("Unavailable")));
        chips_item->append(new QStandardItem((*iter)->package));
        chips_item->append(new QStandardItem(QString::number((*iter)->flash, 'f', 2)));
        chips_item->append(new QStandardItem(QString::number((*iter)->ram, 'f', 2)));
        chips_item->append(new QStandardItem(QString::number((*iter)->io, 10)));
        chips_item->append(new QStandardItem(QString::number((*iter)->flash, 'f', 2)));
        chips_item->append(new QStandardItem((*iter)->company));
        chips_item->append(new QStandardItem((*iter)->core));
        _chips_items.append(chips_item);

        for (auto &item : *chips_item)
            item->setEditable(false);

        model->appendRow(*chips_item);
        _chips_items.append(chips_item);
    }
    _tableview_chip_infos_proxy_model->setSourceModel(model);
    ui->tableview_chip_infos->setModel(_tableview_chip_infos_proxy_model);
    ui->tableview_chip_infos->setSelectionBehavior(QAbstractItemView::SelectRows);
    ui->tableview_chip_infos->setSelectionMode(QAbstractItemView::SingleSelection);
    ui->tableview_chip_infos->setSortingEnabled(true);
    ui->tableview_chip_infos->sortByColumn(0, Qt::AscendingOrder);
    connect(ui->tableview_chip_infos->selectionModel(), &QItemSelectionModel::selectionChanged, this,
            &choose_chip_dialog::tableview_chip_infos_selection_model_selection_changed_callback, Qt::QueuedConnection);
}

void choose_chip_dialog::tableview_chip_infos_selection_model_selection_changed_callback(
    const QItemSelection &selected,
    const QItemSelection &deselected)
{
    Q_UNUSED(deselected);
    set_chips_info_ui(selected.indexes());
}

void choose_chip_dialog::set_chips_info_ui(const QModelIndexList &selected_indexes)
{
    if (selected_indexes.isEmpty())
        return;

    auto chip_name     = selected_indexes[0].data().toString();
    auto market_status = selected_indexes[1].data().toString();
    auto price         = selected_indexes[2].data().toString();
    auto package       = selected_indexes[3].data().toString();
    auto company       = selected_indexes[8].data().toString();
    auto package_path  = QString(":/packages/%1.png").arg(package);

    ui->label_market_status->setText(market_status);
    ui->label_price->setText(price);
    ui->label_package->setText(package);
    ui->pushbutton_name->setText(chip_name);
    ui->pushbutton_company->setText(company);

    QPixmap image;
    if (QFile::exists(package_path))
        image = QPixmap(package_path);
    else
        image = QPixmap(":/packages/unknown.png");
    image.scaled(ui->label_package_image->size(), Qt::IgnoreAspectRatio, Qt::SmoothTransformation);
    ui->label_package_image->setPixmap(image);

    if (_repo_instance->chip_summary_exists(company, chip_name))
    {
        auto chip_summary = _repo_instance->get_chip_summary(company, chip_name);
        ui->textbrowser_readme->setMarkdown(QString("# %1\n\n").arg(chip_name) + chip_summary.illustrate["zh-CN"]);
        ui->pushbutton_name->setProperty("user_url", chip_summary.url["zh-CN"]);
        ui->pushbutton_company->setProperty("user_url", chip_summary.company_url["zh-CN"]);
    }
    else
    {
        ui->textbrowser_readme->setMarkdown(QString("# %1\n\n").arg(chip_name) +
                                            tr("The chip description file <%1.yml> does not exist").arg(chip_name));
        ui->pushbutton_name->setProperty("user_url", "nil");
        ui->pushbutton_company->setProperty("user_url", "nil");
    }
}

void choose_chip_dialog::on_dialogbuttonbox_clicked(QAbstractButton *button)
{
    if (button == nullptr)
        return;

    if (button->text() == tr("Create"))
    {
    }
}

void choose_chip_dialog::on_pushbutton_name_pressed()
{
    auto url = ui->pushbutton_name->property("user_url").toString();
    if (url == "nil")
        return;

    os::open_url(url);
}

void choose_chip_dialog::on_pushbutton_company_pressed()
{
    auto url = ui->pushbutton_company->property("user_url").toString();
    if (url == "nil")
        return;

    os::open_url(url);
}
