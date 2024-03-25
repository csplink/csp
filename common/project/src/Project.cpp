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
    return project_.Name;
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
    if (!project_.Hal.isEmpty())
    {
        loadMaps(project_.Hal);
    }

    if (!project_.Hal.isEmpty() && !project_.TargetChip.isEmpty())
    {
        loadIps(project_.Hal, project_.TargetChip);
    }

    if (!project_.Company.isEmpty() && !project_.TargetChip.isEmpty())
    {
        loadChipSummary(project_.Company, project_.TargetChip);
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
        if (chipSummary_.Name.isEmpty())
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
    return project_.PinConfigs[Key];
}

void Project::setPinComment(const QString &Key, const QString &Comment)
{
    emit signalsPinPropertyChanged("comment", Key, project_.PinConfigs[Key].Comment, Comment);
    project_.PinConfigs[Key].Comment = Comment;
}

QString &Project::getPinComment(const QString &Key)
{
    return project_.PinConfigs[Key].Comment;
}

void Project::setPinFunction(const QString &Key, const QString &Function)
{
    emit signalsPinPropertyChanged("function", Key, project_.PinConfigs[Key].Function, Function);
    project_.PinConfigs[Key].Function = Function;
}

QString &Project::getPinFunction(const QString &Key)
{
    return project_.PinConfigs[Key].Function;
}

void Project::setPinLocked(const QString &Key, const bool Locked)
{
    emit signalsPinPropertyChanged("locked", Key, project_.PinConfigs[Key].Locked, Locked);
    project_.PinConfigs[Key].Locked = Locked;
}

bool Project::getPinLocked(const QString &Key)
{
    return project_.PinConfigs[Key].Locked;
}

void Project::setPinConfigFunctionProperty(const QString &Key, const QString &Module, const QString &Property, const QString &Value)
{
    emit signalsPinFunctionPropertyChanged(Module, Property, Key, project_.PinConfigs[Key].FunctionProperty[Module][Property], Value);
    project_.PinConfigs[Key].FunctionProperty[Module][Property] = Value;
}

void Project::clearPinConfigFunctionProperty(const QString &Key, const QString &Module, const QString &Property)
{
    if (project_.PinConfigs[Key].FunctionProperty.contains(Module))
    {
        if (project_.PinConfigs[Key].FunctionProperty[Module].contains(Property))
        {
            emit signalsPinFunctionPropertyChanged(Module, Property, Key, project_.PinConfigs[Key].FunctionProperty[Module][Property], "");
            project_.PinConfigs[Key].FunctionProperty[Module].remove(Property);
        }
    }
}

void Project::clearPinConfigFunctionProperty(const QString &Key, const QString &Module)
{
    if (project_.PinConfigs[Key].FunctionProperty.contains(Module))
    {
        emit signalsPinFunctionPropertyChanged(Module, "", Key, "", "");
        project_.PinConfigs[Key].FunctionProperty.remove(Module);
    }
}

ProjectTable::PinFunctionPropertiesType &Project::getPinConfigFunctionProperty(const QString &Key)
{
    return project_.PinConfigs[Key].FunctionProperty;
}

QString &Project::getPinConfigFunctionProperty(const QString &Key, const QString &Module, const QString &Property)
{
    return project_.PinConfigs[Key].FunctionProperty[Module][Property];
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
    project_.PinConfigs.clear();
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
            emit signalsLog(msg);
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
    (void)runXmake("f", { "-y", "-m", Mode }, info.dir().absolutePath());
    (void)runXmake("", { "-y", "-j8" }, info.dir().absolutePath());
}

const ProjectTable::ProjectType &Project::getProjectTable()
{
    return project_;
}
