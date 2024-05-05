/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ViewMainWindow.h
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
 *  2023-05-11     xqyjlj       initial version
 */

#ifndef __VIEW_MAIN_WINDOW_H__
#define __VIEW_MAIN_WINDOW_H__

#include <QMainWindow>
#include <QProcess>

#include "DockLog.h"
#include "DockModuleTree.h"
#include "DockPropertyBrowserPin.h"

QT_BEGIN_NAMESPACE
namespace Ui
{
class viewMainWindow;
}
QT_END_NAMESPACE

class ViewMainWindow final : public QMainWindow
{
    Q_OBJECT

  public:
    explicit ViewMainWindow(QWidget *parent = nullptr);
    ~ViewMainWindow() override;

  public slots:
    void createProject();

  private slots:
    void slotActionNewChipTriggered() const;
    void slotActionLoadTriggered();
    void slotActionSaveTriggered();
    void slotActionSaveAsTriggered() const;
    void slotActionCloseTriggered() const;
    void slotActionReportTriggered() const;
    void slotActionGenerateTriggered() const;
    void slotActionPackageManagerTriggered();

  private:
    Ui::viewMainWindow *ui;
    DockLog *m_dockLog;
    DockPropertyBrowserPin *m_dockPropertyBrowserPin;
    DockModuleTree *m_dockModuleTree;

    typedef enum
    {
        STACK_INDEX_HOME,
        STACK_INDEX_CHIP_CONFIGURE,
        STACK_INDEX_EMPTY,
    } StackIndexType;

    void initMode();
    void setMode(StackIndexType index);
};

#endif /** __VIEW_MAIN_WINDOW_H__ */
