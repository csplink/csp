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

#ifndef CSP_PROJECT_H
#define CSP_PROJECT_H

#include <QObject>

#include "ChipSummaryTable.h"
#include "Config.h"
#include "IpTable.h"
#include "MapTable.h"
#include "ProjectTable.h"

#define CSP_PRIVATE_PROJECT_SETTER_GETTER_HELPER(NAME, VALUE, FUNCTION) \
    void set##NAME(const decltype(VALUE) &v)                            \
    {                                                                   \
        (VALUE) = v;                                                    \
        FUNCTION();                                                     \
    }                                                                   \
    const decltype(VALUE) &get##NAME()                                  \
    {                                                                   \
        return VALUE;                                                   \
    }

class Project final : public QObject
{
    Q_OBJECT

  public:
    /**
     * @brief init config
     */
    static void init();

    /**
     * @brief deinit config
     */
    static void deinit();

    /**
     * @brief get project file path
     * @return project file path
     */
    QString getPath() const;

    /**
     * @brief set project file path
     * @param Path: project file path
     */
    void setPath(const QString &Path);

    /**
     * @brief get project name
     * @return project name
     */
    QString getName() const;

    /**
     * @brief get ip map
     * @return ip map as a modifiable reference
     */
    IpTable::IpsType &getIps();

    /**
     * @brief get hal map
     * @return hal map as a modifiable reference
     */
    MapTable::MapsType &getMaps();

    void loadChipSummary(const QString &Company, const QString &Name);

    ChipSummaryTable::ChipSummaryType &getChipSummary();

    const ProjectTable::ProjectType &getProjectTable();

    /******************* pin ************************/
    /**
     * @brief get pin config by pin name
     * @param Key: pin name
     * @return pin config as a modifiable reference
     */
    ProjectTable::PinConfigType &getPinConfig(const QString &Key);

    /**
     * @brief set pin comment by pin name
     * @param Key: pin name
     * @param Comment: pin comment
     */
    void setPinComment(const QString &Key, const QString &Comment);

    /**
     * @brief get pin comment by pin name
     * @param Key: pin name
     * @return pin comment as a modifiable reference
     */
    QString &getPinComment(const QString &Key);

    /**
     * @brief set pin function by pin name
     * @param Key: pin name
     * @param Function: pin function
     */
    void setPinFunction(const QString &Key, const QString &Function);

    /**
     * @brief get pin function by pin name
     * @param Key: pin name
     * @return pin function as a modifiable reference
     */
    QString &getPinFunction(const QString &Key);

    /**
     * @brief set pin locked by pin name
     * @param Key: pin name
     * @param Locked: pin locked
     */
    void setPinLocked(const QString &Key, bool Locked);

    /**
     * @brief get pin locked by pin name
     * @param Key: pin name
     * @return pin locked
     */
    bool getPinLocked(const QString &Key);

    /**
     * @brief set pin config function property
     * @param Key: pin name
     * @param Module: module name
     * @param Property: property name
     * @param Value: property value
     */
    void setPinConfigFunctionProperty(const QString &Key, const QString &Module, const QString &Property, const QString &Value);

    /**
     * @brief clear pin config function property
     * @param Key: pin name
     * @param Module: module name
     * @param Property: property name
     */
    void clearPinConfigFunctionProperty(const QString &Key, const QString &Module, const QString &Property);

    /**
     * @brief clear pin config function module properties
     * @param Key: pin name
     * @param Module: module name
     */
    void clearPinConfigFunctionProperty(const QString &Key, const QString &Module);

    /**
     * @brief get pin config function properties
     * @param Key: pin name
     * @return pin config function properties as a modifiable reference
     */
    ProjectTable::PinFunctionPropertiesType &getPinConfigFunctionProperty(const QString &Key);

    /**
     * @brief get pin config function property
     * @param Key: pin name
     * @param Module: module name
     * @param Property: property name
     * @return pin config function property as a modifiable reference
     */
    QString &getPinConfigFunctionProperty(const QString &Key, const QString &Module, const QString &Property);

    /***********************************************/

    /**
     * @brief load project from file
     * @param Path: project file path
     */
    void loadProject(const QString &Path);

    /**
     * @brief save project to file
     * @param Path: project file path
     */
    void saveProject(const QString &Path);

    /**
     * @brief save project to file
     */
    void saveProject();

    /**
     * @brief dump project
     * @return project string
     */
    QString dumpProject();

    /**
     * @brief clear project
     */
    void clearProject();

    /**
     * @brief 生成代码
     */
    void generateCode() const;

    /**
     * @brief 构建工程
     */
    void build(const QString &mode) const;

  private:
    inline static Project *instance_ = nullptr;
    ProjectTable::ProjectType project_; // project table
    QString path_;                      // project file path
    IpTable::IpsType ips_;              // ip map
    MapTable::MapsType maps_;           // hal map
    ChipSummaryTable::ChipSummaryType chipSummary_;

  public:
    /**
     * @brief get project instance
     * @return project instance
     */
    static Project *getInstance();
    CSP_PRIVATE_PROJECT_SETTER_GETTER_HELPER(ProjectCompany, project_.Company, void)
    CSP_PRIVATE_PROJECT_SETTER_GETTER_HELPER(ProjectHal, project_.Hal, void)
    CSP_PRIVATE_PROJECT_SETTER_GETTER_HELPER(ProjectHalVersion, project_.HalVersion, void)
    CSP_PRIVATE_PROJECT_SETTER_GETTER_HELPER(ProjectModules, project_.Modules, void)
    CSP_PRIVATE_PROJECT_SETTER_GETTER_HELPER(ProjectPackage, project_.Package, void)
    CSP_PRIVATE_PROJECT_SETTER_GETTER_HELPER(ProjectTargetChip, project_.TargetChip, void)
    CSP_PRIVATE_PROJECT_SETTER_GETTER_HELPER(ProjectToolchains, project_.Toolchains, void)
    CSP_PRIVATE_PROJECT_SETTER_GETTER_HELPER(ProjectToolchainsVersion, project_.ToolchainsVersion, void)
    CSP_PRIVATE_PROJECT_SETTER_GETTER_HELPER(ProjectType, project_.Type, void)
    CSP_PRIVATE_PROJECT_SETTER_GETTER_HELPER(ProjectName, project_.Name, void)
    CSP_PRIVATE_PROJECT_SETTER_GETTER_HELPER(ProjectPinConfigs, project_.PinConfigs, void)
    CSP_PRIVATE_PROJECT_SETTER_GETTER_HELPER(ProjectTargetProject, project_.TargetProject, void)
    CSP_PRIVATE_PROJECT_SETTER_GETTER_HELPER(ProjectTargetProjectMinVersion, project_.TargetProjectMinVersion, void)
    CSP_PRIVATE_PROJECT_SETTER_GETTER_HELPER(ProjectVersion, project_.Version, void)

  signals:
    /**
     * @brief project property changed signal
     * @param Property: property name
     * @param Name: pin name
     * @param OldValue: old value
     * @param NewValue: new value
     */
    void signalsPinPropertyChanged(const QString &Property, const QString &Name, const QVariant &OldValue, const QVariant &NewValue);
    void signalsPinFunctionPropertyChanged(const QString &Module, const QString &Property, const QString &Name, const QVariant &OldValue, const QVariant &NewValue);
    void signalsProjectClear();
    void signalsLog(const QString &Msg) const;

  private:
    Project() = default;
    ~Project() override = default;

    Q_DISABLE_COPY_MOVE(Project)

    /**
     * @brief load hal map from db
     * @param Hal: hal name
     * @return hal map as a modifiable reference
     */
    void loadMaps(const QString &Hal);

    /**
     * @brief load ip map from db
     * @param Hal: hal name
     * @param Name: chip name
     * @return ip map as a modifiable reference
     */
    void loadIps(const QString &Hal, const QString &Name);

    void loadDb();
};

#endif // CSP_PROJECT_H
