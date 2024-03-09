/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ViewHome.h
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

#ifndef VIEW_HOME_H
#define VIEW_HOME_H

#include <QWidget>

#include "project.h"

namespace Ui
{
class viewHome;
}

class ViewHome final : public QWidget
{
    Q_OBJECT

  public:
    explicit ViewHome(QWidget *parent = nullptr);
    ~ViewHome() override;

  signals:
    void signalCreateProject();
    void signalOpenExistingProject(bool checked);

  public slots:
    void pushButtonCreateChipProjectClickedCallback(bool checked);
    void createChipProject();

  private slots:
    void pushButtonCreateBoardProjectClickedCallback(bool checked) const;
    void dialogChooseChipFinishedCallback(int result) const;
    void pushButtonOpenExistingProjectClickedCallback(bool checked);

  private:
    Ui::viewHome *ui_;
    project *projectInstance_;
};

#endif /** VIEW_HOME_H */
