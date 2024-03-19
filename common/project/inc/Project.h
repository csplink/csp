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

class Project final : public QObject
{
    Q_OBJECT

  public:
    typedef enum
    {
        CSP_CORE_ATTRIBUTE_TYPE_HAL = 0,
        CSP_CORE_ATTRIBUTE_TYPE_TARGET,
        CSP_CORE_ATTRIBUTE_TYPE_PACKAGE,
        CSP_CORE_ATTRIBUTE_TYPE_COMPANY,
        CSP_CORE_ATTRIBUTE_TYPE_TYPE,
    } CoreAttributeType;

    /**
     * @brief init config
     */
    static void init();

    /**
     * @brief deinit config
     */
    static void deinit();

    /******************* core ***********************/
    /**
     * @brief get core config value by core name
     * @param Type: core attribute type
     * @return core config value
     */
    QString getCore(CoreAttributeType Type) const;

    /**
     * @brief set core config value by core name
     * @param Type: core attribute type
     * @param Value: core config value
     */
    void setCore(CoreAttributeType Type, const QString &Value);
    /***********************************************/

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
     * @brief set project name
     * @param Name: project name
     */
    void setName(const QString &Name);

    /**
     * @brief get ip map
     * @return ip map as a modifiable reference
     */
    ip_table::ips_t &getIps();

    /**
     * @brief get hal map
     * @return hal map as a modifiable reference
     */
    map_table::maps_t &getMaps();

    void loadChipSummary(const QString &Company, const QString &Name);
    chip_summary_table::chip_summary_t &getChipSummary();

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
    ProjectTable::pin_function_properties_t &getPinConfigFunctionProperty(const QString &Key);

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
    void build(const QString &Mode) const;

    int runXmake(const QString &Command, const QStringList &Args, const QString &WorkDir = Config::defaultWorkDir()) const;

  private:
    inline static Project *instance_ = nullptr;
    ProjectTable::ProjectType project_; // project table
    QString path_;                      // project file path
    ip_table::ips_t ips_;               // ip map
    map_table::maps_t maps_;            // hal map
    chip_summary_table::chip_summary_t chipSummary_;

  public:
    /**
     * @brief get project instance
     * @return project instance
     */
    static Project *getInstance();

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
    void signalsXMakeLog(const QString &Msg) const;

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
