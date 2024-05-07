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

#ifndef __VIEW_CONFIGURE_H__
#define __VIEW_CONFIGURE_H__

#include "PropertyBrowserPin.h"

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

    void setPropertyBrowser(PropertyBrowserPin *instance);

  protected:
    void resizeEvent(QResizeEvent *event) override;

  private:
    Ui::viewConfigure *ui;
    PropertyBrowserPin *m_propertyBrowserInstance;
    int m_resizeCounter;

    void initView();
    void initMainView();
    void initProjectSettings() const;
    void initLinkerSettings() const;
    void initPackageSettings() const;
    void initToolchainsSettings() const;
    void flushComboBoxPackageVersion() const;
    void flushComboBoxToolchainsVersionVersion() const;

  private slots:
    void slotPushButtonPackageManagerPressed();
    void slotPushButtonZoomInPressed() const;
    void slotPushButtonZoomResetPressed() const;
    void slotPushButtonZoomOutPressed() const;
    void slotComboBoxPackageVersionCurrentTextChanged(const QString &text);
    void slotComboBoxBuildScriptIdeCurrentTextChanged(const QString &text);
    void slotComboBoxBuildScriptIdeMinVersionCurrentTextChanged(const QString &text);
    void slotCheckBoxEnableToolchainsStateChanged(int State);
    void slotPushButtonToolchainsManagerPressed();
    void slotComboBoxToolchainsVersionCurrentTextChanged(const QString &text);
    void slotLineEditHeapSizeTextChanged(const QString &text);
    void slotLineEditStackSizeTextChanged(const QString &text);

    void slotProjectReloaded();
};

#endif /** __VIEW_CONFIGURE_H__ */
