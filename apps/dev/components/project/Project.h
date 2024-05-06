/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        Project.h
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
 *  2023-05-26     xqyjlj       initial version
 */

#ifndef __PROJECT_H__
#define __PROJECT_H__

#include <QObject>

#include "ChipSummaryTable.h"
#include "IpTable.h"
#include "MapTable.h"
#include "ProjectTable.h"
#include "Settings.h"

class CspProject final : public QObject
{
    Q_OBJECT

  public:
    CspProject();
    ~CspProject() override;

    static CspProject &singleton();

    QString path() const;
    void setPath(const QString &path);

    QString halVersion() const;
    void setHalVersion(const QString &version);

    QString toolchainsVersion() const;
    void setToolchainsVersion(const QString &version);

    QString targetProjectMinVersion() const;
    void setTargetProjectMinVersion(const QString &version);

    QString targetProject() const;
    void setTargetProject(const QString &version);

    QString type() const;
    void setType(const QString &type);

    QString name() const;
    void setName(const QString &name);

    QString package() const;
    void setPackage(const QString &package);

    QString hal() const;
    void setHal(const QString &hal);

    QString company() const;
    void setCompany(const QString &company);

    QString targetChip() const;
    void setTargetChip(const QString &targetChip);

    QString pinComment(const QString &key);
    void setPinComment(const QString &key, const QString &comment);

    QString pinFunction(const QString &key);
    void setPinFunction(const QString &key, const QString &function);

    bool pinLocked(const QString &key);
    void setPinLocked(const QString &key, bool locked);

    void setPinConfigFunctionProperty(const QString &Key, const QString &Module, const QString &Property,
                                      const QString &Value);
    void clearPinConfigFunctionProperty(const QString &Key, const QString &Module, const QString &Property);
    void clearPinConfigFunctionProperty(const QString &Key, const QString &Module);
    ProjectTable::PinFunctionPropertiesType &pinConfigFunctionProperty(const QString &Key);
    QString &pinConfigFunctionProperty(const QString &Key, const QString &Module, const QString &Property);

    void loadProject(const QString &path);
    void loadProjectWithDialog(QWidget *parent);
    void saveProject(const QString &path);
    bool saveProject();
    void createProject();
    QString dumpProject();
    void clearProject();
    void generateCode() const;

  signals:
    void signalReload();
    void signalPinCommentChanged(const QString &name, const QString &oldValue, const QString &newValue);
    void signalPinFunctionChanged(const QString &name, const QString &oldValue, const QString &newValue);
    void signalPinLockedChanged(const QString &name, bool oldValue, bool newValue);
    void signalPinFunctionPropertyChanged(const QString &module, const QString &property, const QString &name,
                                          const QVariant &oldValue, const QVariant &newValue);
    void signalProjectClear();

  private:
    ProjectTable::ProjectType m_project;
    QString m_path;

    Q_DISABLE_COPY_MOVE(CspProject)
};

#define Project CspProject::singleton()

#endif // __PROJECT_H__
