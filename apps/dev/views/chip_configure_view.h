/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        chip_configure_view.h
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
 *  2023-05-14     xqyjlj       initial version
 */

#ifndef CHIP_CONFIGURE_VIEW_H
#define CHIP_CONFIGURE_VIEW_H

#include "project.h"
#include "propertybrowser.h"

namespace Ui
{
class chip_configure_view;
}

class chip_configure_view final : public QWidget
{
    Q_OBJECT

  public:
    explicit chip_configure_view(QWidget *parent = nullptr);
    virtual ~chip_configure_view() override;

    void set_propertybrowser(propertybrowser *instance);
    void init_view();
    void resize_view() const;

  signals:
    void signal_update_modules_treeview(const QString &company, const QString &name);

  protected:
    virtual void showEvent(QShowEvent *event) override;
    virtual void resizeEvent(QResizeEvent *event) override;

  private:
    Ui::chip_configure_view *_ui;
    propertybrowser *_propertybrowser_instance;
    project *_project_instance;
    int resize_counter = 0;
};

#endif // CHIP_CONFIGURE_VIEW_H
