/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ViewConfigure.h
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

#ifndef VIEW_CONFIGURE_H
#define VIEW_CONFIGURE_H

#include "project.h"
#include "propertybrowser.h"

namespace Ui
{
class viewConfigure;
}

class ViewConfigure final : public QWidget
{
    Q_OBJECT

  public:
    explicit ViewConfigure(QWidget *parent = nullptr);
    ~ViewConfigure() override;

    void setPropertyBrowser(propertybrowser *instance);
    void initView();
    void resizeView() const;

  signals:
    void signalUpdateModulesTreeView(const QString &company, const QString &name);

  protected:
    void showEvent(QShowEvent *event) override;
    void resizeEvent(QResizeEvent *event) override;

  private:
    Ui::viewConfigure *ui_;
    propertybrowser *propertyBrowserInstance_;
    project *projectInstance_;
    int resizeCounter_ = 0;

    void initProjectSettings() const;
    void initLinkerSettings() const;
    void initPackageSettings() const;

  private slots:
    void pushButtonPackageManagerPressedCallback();
};

#endif /** VIEW_CONFIGURE_H */
