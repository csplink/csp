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

#ifndef VIEW_MAIN_WINDOW_H
#define VIEW_MAIN_WINDOW_H

#include <QMainWindow>
#include <QProcess>

#include "Project.h"

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

    static void messageLogHandler(const QString &msg);

  signals:
    void signalAddLog(const QString &string);

  public slots:
    void updateModulesTreeView(const QString &company, const QString &name) const;
    void createProject();

  private slots:
    void actionNewChipTriggeredCallback(bool checked) const;
    void actionLoadTriggeredCallback(bool checked);
    void actionSaveTriggeredCallback(bool checked);
    void actionSaveAsTriggeredCallback(bool checked) const;
    void actionCloseTriggeredCallback(bool checked) const;
    void actionReportTriggeredCallback(bool checked) const;
    void actionGenerateTriggeredCallback(bool checked) const;
    void actionPackageManagerTriggeredCallback(bool checked);
    void actionBuildDebugTriggeredCallback(bool checked) const;
    void actionBuildReleaseTriggeredCallback(bool checked) const;
    void xmakeReadyReadStandardOutputCallback(const QProcess *process, const QString &msg);
    void pythonReadyReadStandardOutputOrErrorCallback(const QProcess *process, QString msg);

  private:
    Ui::viewMainWindow *ui_;
    Project *projectInstance_;

    typedef enum
    {
        STACK_INDEX_HOME,
        STACK_INDEX_CHIP_CONFIGURE,
        STACK_INDEX_EMPTY,
    } StackIndexType;

    void initMode();
    void setMode(StackIndexType index);
    static void sysMessageLogHandler(QtMsgType type, const QMessageLogContext &context, const QString &msg);
};
#endif /** VIEW_MAIN_WINDOW_H */
