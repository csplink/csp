/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        Project.cpp
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

#include <QApplication>
#include <QDir>
#include <QGlobalStatic>

#include "CspCoderJob.h"
#include "Project.h"
#include "Settings.h"

Q_GLOBAL_STATIC(QScopedPointer<CspProject>, instance)

CspProject::CspProject()
    : QObject(),
      m_project(),
      m_path()
{
}

CspProject::~CspProject()
{
}

CspProject &CspProject::singleton()
{
    if (!*instance)
    {
        instance->reset(new CspProject());
    }
    return **instance;
}

QString CspProject::path() const
{
    return m_path;
}

void CspProject::setPath(const QString &path)
{
    if (!path.isEmpty())
    {
        const QDir root(".");
        m_path = root.absoluteFilePath(path);
    }
    else
    {
        /** TODO: failed */
    }
}

QString CspProject::halVersion() const
{
    return m_project.HalVersion;
}

void CspProject::setHalVersion(const QString &version)
{
    m_project.HalVersion = version;
}

QString CspProject::toolchainsVersion() const
{
    return m_project.ToolchainsVersion;
}

void CspProject::setToolchainsVersion(const QString &version)
{
    m_project.ToolchainsVersion = version;
}

QString CspProject::targetProjectMinVersion() const
{
    return m_project.TargetProjectMinVersion;
}

void CspProject::setTargetProjectMinVersion(const QString &version)
{
    m_project.TargetProjectMinVersion = version;
}

QString CspProject::targetProject() const
{
    return m_project.TargetProject;
}

void CspProject::setTargetProject(const QString &version)
{
    m_project.TargetProject = version;
}

QString CspProject::type() const
{
    return m_project.Type;
}

void CspProject::setType(const QString &type)
{
    m_project.Type = type;
}

QString CspProject::name() const
{
    return m_project.Name;
}

void CspProject::setName(const QString &name)
{
    m_project.Name = name;
}

QString CspProject::package() const
{
    return m_project.Package;
}

void CspProject::setPackage(const QString &package)
{
    m_project.Package = package;
}

QString CspProject::hal() const
{
    return m_project.Hal;
}

void CspProject::setHal(const QString &hal)
{
    m_project.Hal = hal;
}

QString CspProject::company() const
{
    return m_project.Company;
}

void CspProject::setCompany(const QString &company)
{
    m_project.Company = company;
}

QString CspProject::targetChip() const
{
    return m_project.TargetChip;
}

void CspProject::setTargetChip(const QString &targetChip)
{
    m_project.TargetChip = targetChip;
}

QString CspProject::pinComment(const QString &key)
{
    return m_project.PinConfigs[key].Comment;
}

void CspProject::setPinComment(const QString &key, const QString &comment)
{
    emit signalPinCommentChanged(key, m_project.PinConfigs[key].Comment, comment);
    m_project.PinConfigs[key].Comment = comment;
}

QString CspProject::pinFunction(const QString &key)
{
    return m_project.PinConfigs[key].Function;
}

void CspProject::setPinFunction(const QString &key, const QString &function)
{
    emit signalPinFunctionChanged(key, m_project.PinConfigs[key].Function, function);
    m_project.PinConfigs[key].Function = function;
}

bool CspProject::pinLocked(const QString &key)
{
    return m_project.PinConfigs[key].Locked;
}

void CspProject::setPinLocked(const QString &key, const bool locked)
{
    emit signalPinLockedChanged(key, m_project.PinConfigs[key].Locked, locked);
    m_project.PinConfigs[key].Locked = locked;
}

void CspProject::setPinConfigFunctionProperty(const QString &Key, const QString &Module, const QString &Property,
                                              const QString &Value)
{
    emit signalPinFunctionPropertyChanged(Module, Property, Key,
                                          m_project.PinConfigs[Key].FunctionProperty[Module][Property], Value);
    m_project.PinConfigs[Key].FunctionProperty[Module][Property] = Value;
}

void CspProject::clearPinConfigFunctionProperty(const QString &Key, const QString &Module, const QString &Property)
{
    if (m_project.PinConfigs[Key].FunctionProperty.contains(Module))
    {
        if (m_project.PinConfigs[Key].FunctionProperty[Module].contains(Property))
        {
            emit signalPinFunctionPropertyChanged(Module, Property, Key,
                                                  m_project.PinConfigs[Key].FunctionProperty[Module][Property], "");
            m_project.PinConfigs[Key].FunctionProperty[Module].remove(Property);
        }
    }
}

void CspProject::clearPinConfigFunctionProperty(const QString &Key, const QString &Module)
{
    if (m_project.PinConfigs[Key].FunctionProperty.contains(Module))
    {
        emit signalPinFunctionPropertyChanged(Module, "", Key, "", "");
        m_project.PinConfigs[Key].FunctionProperty.remove(Module);
    }
}

ProjectTable::PinFunctionPropertiesType &CspProject::pinConfigFunctionProperty(const QString &Key)
{
    return m_project.PinConfigs[Key].FunctionProperty;
}

QString &CspProject::pinConfigFunctionProperty(const QString &Key, const QString &Module, const QString &Property)
{
    return m_project.PinConfigs[Key].FunctionProperty[Module][Property];
}

/***********************************************/

void CspProject::loadProject(const QString &path)
{
    if (QFile::exists(path))
    {
        if (ProjectTable::loadProject(&m_project, path))
        {
            setPath(path);
            emit signalReload();
        }
    }
    else
    {
        /** TODO: failed */
    }
}

void CspProject::saveProject(const QString &path)
{
    setPath(path);
    saveProject();
}

void CspProject::saveProject()
{
    if (!m_path.isEmpty())
    {
        const QFileInfo info(m_path);
        const QString path = info.dir().absolutePath();
        const QDir dir(path);
        if (!dir.exists())
        {
            (void)dir.mkpath(path);
        }
        ProjectTable::saveProject(m_project, m_path);
    }
    else
    {
        /** TODO: failed */
    }
}

QString CspProject::dumpProject()
{
    return ProjectTable::dumpProject(m_project);
}

void CspProject::clearProject()
{
    m_project.PinConfigs.clear();
    emit signalProjectClear();
}

void CspProject::generateCode() const
{
    CspCoderJob job("coder");
    job.generate(m_path);
    /** TODO */
}
