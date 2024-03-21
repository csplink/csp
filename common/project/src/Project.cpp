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

#include <QDebug>
#include <QDir>
#include <QProcess>

#include "Config.h"
#include "Project.h"
#include "XMake.h"

void Project::init()
{
    if (instance_ == nullptr)
    {
        instance_ = new Project();
    }
}

void Project::deinit()
{
    delete instance_;
    instance_ = nullptr;
}

Project *Project::getInstance()
{
    return instance_;
}

QString Project::getCore(const CoreAttributeType Type) const
{
    QString value;

    switch (Type)
    {
    case CORE_ATTRIBUTE_TYPE_HAL:
        value = project_.core.hal;
        break;
    case CORE_ATTRIBUTE_TYPE_TARGET:
        value = project_.core.target;
        break;
    case CORE_ATTRIBUTE_TYPE_PACKAGE:
        value = project_.core.package;
        break;
    case CORE_ATTRIBUTE_TYPE_COMPANY:
        value = project_.core.company;
        break;
    case CORE_ATTRIBUTE_TYPE_TYPE:
        value = project_.core.type;
        break;
    }

    return value;
}

void Project::setCore(const CoreAttributeType Type, const QString &Value)
{
    if (!Value.isEmpty())
    {
        switch (Type)
        {
        case CORE_ATTRIBUTE_TYPE_HAL:
            project_.core.hal = Value;
            break;
        case CORE_ATTRIBUTE_TYPE_TARGET:
            project_.core.target = Value;
            break;
        case CORE_ATTRIBUTE_TYPE_PACKAGE:
            project_.core.package = Value;
            break;
        case CORE_ATTRIBUTE_TYPE_COMPANY:
            project_.core.company = Value;
            break;
        case CORE_ATTRIBUTE_TYPE_TYPE:
            project_.core.type = Value;
            break;
        }

        loadDb();
    }
    else
    {
        /** TODO: failed */
    }
}

QString Project::getPath() const
{
    return path_;
}

void Project::setPath(const QString &Path)
{
    if (!Path.isEmpty())
    {
        const QDir root(".");
        path_ = root.absoluteFilePath(Path);
    }
    else
    {
        /** TODO: failed */
    }
}

QString Project::getName() const
{
    return project_.name;
}

void Project::setName(const QString &Name)
{
    if (!Name.isEmpty())
    {
        project_.name = Name;
    }
    else
    {
        /** TODO: failed */
    }
}

void Project::loadIps(const QString &Hal, const QString &Name)
{
    if (!Hal.isEmpty() && !Name.isEmpty())
    {
        if (ips_.isEmpty())
        {
            IpTable::loadIps(&ips_, Hal, Name);
        }
    }
    else
    {
        /** TODO: failed */
    }
}

void Project::loadDb()
{
    if (!project_.core.hal.isEmpty())
    {
        loadMaps(project_.core.hal);
    }

    if (!project_.core.target.isEmpty() && !project_.core.hal.isEmpty())
    {
        loadIps(project_.core.hal, project_.core.target);
    }

    if (!project_.core.company.isEmpty() && !project_.core.hal.isEmpty())
    {
        loadChipSummary(project_.core.company, project_.core.target);
    }
}

IpTable::IpsType &Project::getIps()
{
    return ips_;
}

void Project::loadMaps(const QString &Hal)
{
    if (!Hal.isEmpty())
    {
        if (maps_.isEmpty())
        {
            MapTable::loadMaps(&maps_, Hal);
        }
    }
    else
    {
        /** TODO: failed */
    }
}

MapTable::MapsType &Project::getMaps()
{
    return maps_;
}

void Project::loadChipSummary(const QString &Company, const QString &Name)
{
    if (!Company.isEmpty() && !Name.isEmpty())
    {
        if (chipSummary_.name.isEmpty())
        {
            ChipSummaryTable::loadChipSummary(&chipSummary_, Company, Name);
        }
    }
    else
    {
        /** TODO: failed */
    }
}

ChipSummaryTable::ChipSummaryType &Project::getChipSummary()
{
    return chipSummary_;
}

/******************* pin ************************/
ProjectTable::PinConfigType &Project::getPinConfig(const QString &Key)
{
    return project_.pin_configs[Key];
}

void Project::setPinComment(const QString &Key, const QString &Comment)
{
    emit signalsPinPropertyChanged("comment", Key, project_.pin_configs[Key].comment, Comment);
    project_.pin_configs[Key].comment = Comment;
}

QString &Project::getPinComment(const QString &Key)
{
    return project_.pin_configs[Key].comment;
}

void Project::setPinFunction(const QString &Key, const QString &Function)
{
    emit signalsPinPropertyChanged("function", Key, project_.pin_configs[Key].function, Function);
    project_.pin_configs[Key].function = Function;
}

QString &Project::getPinFunction(const QString &Key)
{
    return project_.pin_configs[Key].function;
}

void Project::setPinLocked(const QString &Key, const bool Locked)
{
    emit signalsPinPropertyChanged("locked", Key, project_.pin_configs[Key].locked, Locked);
    project_.pin_configs[Key].locked = Locked;
}

bool Project::getPinLocked(const QString &Key)
{
    return project_.pin_configs[Key].locked;
}

void Project::setPinConfigFunctionProperty(const QString &Key, const QString &Module, const QString &Property, const QString &Value)
{
    emit signalsPinFunctionPropertyChanged(Module, Property, Key, project_.pin_configs[Key].function_property[Module][Property], Value);
    project_.pin_configs[Key].function_property[Module][Property] = Value;
}

void Project::clearPinConfigFunctionProperty(const QString &Key, const QString &Module, const QString &Property)
{
    if (project_.pin_configs[Key].function_property.contains(Module))
    {
        if (project_.pin_configs[Key].function_property[Module].contains(Property))
        {
            emit signalsPinFunctionPropertyChanged(Module, Property, Key, project_.pin_configs[Key].function_property[Module][Property], "");
            project_.pin_configs[Key].function_property[Module].remove(Property);
        }
    }
}

void Project::clearPinConfigFunctionProperty(const QString &Key, const QString &Module)
{
    if (project_.pin_configs[Key].function_property.contains(Module))
    {
        emit signalsPinFunctionPropertyChanged(Module, "", Key, "", "");
        project_.pin_configs[Key].function_property.remove(Module);
    }
}

ProjectTable::pin_function_properties_t &Project::getPinConfigFunctionProperty(const QString &Key)
{
    return project_.pin_configs[Key].function_property;
}

QString &Project::getPinConfigFunctionProperty(const QString &Key, const QString &Module, const QString &Property)
{
    return project_.pin_configs[Key].function_property[Module][Property];
}

/***********************************************/

void Project::loadProject(const QString &Path)
{
    if (QFile::exists(Path))
    {
        ProjectTable::loadProject(&project_, Path);

        setPath(Path);

        loadDb();
    }
    else
    {
        /** TODO: failed */
    }
}

void Project::saveProject(const QString &Path)
{
    ProjectTable::saveProject(project_, Path);
}

void Project::saveProject()
{
    if (!path_.isEmpty())
    {
        const QFileInfo info(path_);
        const QString path = info.dir().absolutePath();
        const QDir dir(path);
        if (!dir.exists())
        {
            (void)dir.mkpath(path);
        }
        ProjectTable::saveProject(project_, path_);
    }
    else
    {
        /** TODO: failed */
    }
}

QString Project::dumpProject()
{
    return ProjectTable::dumpProject(project_);
}

void Project::clearProject()
{
    project_.pin_configs.clear();
    emit signalsProjectClear();
}

int Project::runXmake(const QString &Command, const QStringList &Args, const QString &WorkDir) const
{
    const QString program = Config::toolXmake();
    const QMap<QString, QString> env = Config::env();
    QStringList list;
    if (!Command.isEmpty())
    {
        list = QStringList{ Command, "-D" };
    }
    list << Args;

    QProcessEnvironment environment = QProcessEnvironment::systemEnvironment();
    auto env_i = env.constBegin();
    while (env_i != env.constEnd())
    {
        environment.insert(env_i.key(), env_i.value());
        ++env_i;
    }
    QProcess *process = new QProcess();
    process->setProgram(program);
    process->setArguments(list);
    process->setProcessEnvironment(environment);

    const QDir dir(WorkDir);
    if (dir.exists())
    {
        process->setWorkingDirectory(WorkDir);
    }

    connect(process, &QProcess::readyReadStandardOutput, this, [this, process]() {
        const QByteArray output = process->readAllStandardOutput();
        if (!output.isEmpty())
        {
            const QString msg = output.trimmed();
            emit signalsXMakeLog(msg);
        }
    });
    connect(process, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished), [process](const int ExitCode, const QProcess::ExitStatus ExitStatus) {
        Q_UNUSED(ExitCode);
        Q_UNUSED(ExitStatus);
        process->deleteLater();
    });

    process->start();
    process->waitForFinished(30000);
    return process->exitCode();
}

void Project::generateCode() const
{
    const QFileInfo info(path_);
    runXmake("csp-coder", { QString("--project-file=") + path_, QString("--output=") + info.dir().absolutePath(), QString("--repositories=") + Config::repositoriesDir() });
}

void Project::build(const QString &Mode) const
{
    const QFileInfo info(path_);
    runXmake("f", { "-y", "-m", Mode }, info.dir().absolutePath());
    runXmake("", { "-y", "-j8" }, info.dir().absolutePath());
}
