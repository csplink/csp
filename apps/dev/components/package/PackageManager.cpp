/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        PackageManager.cpp
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
 *  Copyright (C) 2024-2024 xqyjlj<xqyjlj@126.com>
 *
 * ****************************************************************************
 *  Change Logs:
 *  Date           Author       Notes
 *  ------------   ----------   -----------------------------------------------
 *  2024-06-08     xqyjlj       initial version
 */

#include <QDir>
#include <QFile>
#include <QFileInfoList>
#include <QGlobalStatic>

#include "Debug.h"
#include "PackageDescriptionTable.h"
#include "PackageManager.h"
#include "QtJson.h"
#include "QtYaml.h"
#include "Settings.h"
#include "quazip.h"
#include "quazipfile.h"

namespace QT_YAML
{
QT_YAML_GEN_PARSE_CODE(CspPackageManager::PackageType, Path)
} // namespace QT_YAML

namespace QT_JSON
{
QT_JSON_GEN_PARSE_CODE(CspPackageManager::PackageType, Path)
} // namespace QT_JSON

QT_DEBUG_ADD_TYPE(CspPackageManager::PackageType)
QT_DEBUG_ADD_TYPE(CspPackageManager::PackageVersionType)
QT_DEBUG_ADD_TYPE(CspPackageManager::PackagesType)

Q_GLOBAL_STATIC(QScopedPointer<CspPackageManager>, instance)

CspPackageManager::CspPackageManager()
    : QObject(),
      m_packages(),
      m_repositoryIndexFilePath(Settings.repositoryIndexFile()),
      m_workerThread(nullptr)
{

    m_workerThread = new CspPackageManagerWorkerThread(this->parent(), "", this);

    if (!QFile::exists(m_repositoryIndexFilePath))
    {
        QFile file(m_repositoryIndexFilePath);
        file.open(QIODevice::WriteOnly);
        file.close();
    }

    loadPackages(&m_packages, m_repositoryIndexFilePath);

    dump();
}

CspPackageManager::~CspPackageManager()
{
    save();
}

CspPackageManager &CspPackageManager::singleton()
{
    if (!*instance)
    {
        instance->reset(new CspPackageManager());
    }
    return **instance;
}

bool CspPackageManager::loadPackages(PackagesType *packages, const QString &path)
{
    bool rtn = false;

    if (packages != nullptr)
    {
        QFile file(path);
        if (file.open(QIODevice::ReadOnly))
        {
            try
            {
                const std::string buffer = file.readAll().toStdString();
                const YAML::Node yaml_data = YAML::Load(buffer);
                YAML::convert<PackagesType>::decode(yaml_data, *packages);
                rtn = true;
            }
            catch (std::exception &e)
            {
                SHOW_E(nullptr, tr("Package manager"),
                       QString("Try to parse file \"%1\" failed. reason: %2").arg(path, e.what()));
                throw;
            }

            file.close();
        }
        else
        {
            SHOW_W(nullptr, tr("Package manager"), QString("The file %1 not found!").arg(path));
        }
    }
    else
    {
        SHOW_E(nullptr, tr("Package manager"), "The package description ptr is nullptr!");
    }
    return rtn;
}

void CspPackageManager::uninstall(const QString &name, const QString &version)
{
    const QString path = packagePath(name, version);
    QMutexLocker locker(&mutex);
    QDir dir(path);

    if (dir.exists())
    {
        dir.removeRecursively();
        m_packages[name][version] = {};
        save();
    }
    else
    {
        LOG_W() << QString("The package %1:%2 is not installed");
    }
}

void CspPackageManager::install(const QString &path)
{
    QMutexLocker locker(&mutex);
    if (!unzip(path))
    {
        emit signalFinish(false);
        return;
    }

    if (!install())
    {
        emit signalFinish(false);
        return;
    }

    emit signalFinish(true);
}

void CspPackageManager::installAsync(const QString &path)
{
    m_workerThread->setPath(path);
    m_workerThread->start();
}

bool CspPackageManager::unzip(const QString &path)
{
    bool rtn = false;

    QuaZip archive(path);
    if (archive.open(QuaZip::mdUnzip))
    {
        QString dstPath = Settings.repository() + "/tmp";
        QDir dir(dstPath);
        if (dir.exists())
        {
            dir.removeRecursively();
        }
        int count = archive.getEntriesCount();
        int i = 0;
        QString fileName;

        for (bool f = archive.goToFirstFile(); f; f = archive.goToNextFile())
        {
            fileName = archive.getCurrentFileName();

            emit signalUpdateFileName(fileName);

            if (fileName.endsWith("/"))
            {
                dir.mkpath(fileName);
            }
            else
            {
                QuaZipFile zipFile;
                QFile dstFile;
                int bytesRead;
                static constexpr int blockSize = 1024 * 1024;
                char buffer[blockSize] = {0};

                zipFile.setZipName(archive.getZipName());
                zipFile.setFileName(fileName);
                zipFile.open(QIODevice::ReadOnly);
                dstFile.setFileName(QString("%1/%2").arg(dstPath, fileName));

                if (dstFile.open(QIODevice::WriteOnly))
                {
                    while ((bytesRead = zipFile.read(buffer, blockSize)) > 0)
                    {
                        dstFile.write(buffer, bytesRead);
                    }
                    dstFile.close();
                }
                else
                {
                    SHOW_E(nullptr, tr("Package Installer"), QString("Can not open file: %1").arg(dstFile.fileName()));
                    return rtn;
                }
                zipFile.close();
            }

            i++;
            emit signalUpdateProgress((i * 100.0) / count);
        }

        QFileInfoList files =
            dir.entryInfoList({}, QDir::Files | QDir::Dirs | QDir::Hidden | QDir::NoSymLinks | QDir::NoDotAndDotDot);
        count = files.count();
        if (count == 1 && files[0].isDir())
        {
            dir.rename(files[0].absoluteFilePath(), Settings.repository() + "/tmp.tmp");
            dir.rmdir(dstPath);
            dir.rename(Settings.repository() + "/tmp.tmp", dstPath);
        }

        rtn = true;
    }
    else
    {
        SHOW_E(nullptr, tr("Package Installer"), QString("Can not open file: %1").arg(path));
    }

    return rtn;
}

bool CspPackageManager::install()
{
    bool rtn = false;
    QString dstPath = Settings.repository() + "/tmp";
    QDir dir(dstPath);
    QFileInfoList files = dir.entryInfoList({"*.sdp"}, QDir::Files | QDir::Hidden | QDir::NoSymLinks);
    int count = files.count();
    if (count > 0)
    {
        PackageDescriptionTable::PackageDescriptionType packageDescription;
        PackageDescriptionTable::loadPackageDescription(&packageDescription, files[0].absoluteFilePath());

        const QString &name = packageDescription.Name;
        const QString &type = packageDescription.Type;
        const QString &vendor = packageDescription.Vendor;
        const QString &version = packageDescription.Version;

        QString parentPath = QString("%1/%2/%3/%4").arg(Settings.repository(), type.toLower(), vendor, name);
        QString path = QString("%1/%2").arg(parentPath, version);
        QDir parentDir(parentPath);
        if (!parentDir.exists())
        {
            if (!parentDir.mkpath(parentPath))
            {
                SHOW_E(nullptr, tr("Package Installer"), QString("Can not mkdir: %1").arg(parentPath));
                return rtn;
            }
        }

        if (!dir.rename(dstPath, path))
        {
            SHOW_E(nullptr, tr("Package Installer"), QString("Can not rename: %1 to %2").arg(dstPath, path));
            return rtn;
        }

        PackageType package = {.Path = path};

        m_packages[name][version] = package;

        save();

        rtn = true;
    }
    else
    {
        SHOW_E(nullptr, tr("Package Installer"), QString("Can not find package description file"));
        return rtn;
    }

    return rtn;
}

QStringList CspPackageManager::packages()
{
    return m_packages.keys();
}

QStringList CspPackageManager::packageVersions(const QString &name)
{
    return m_packages[name].keys();
}

bool CspPackageManager::packageInstalled(const QString &name, const QString &version)
{
    return !packagePath(name, version).isEmpty();
}

QString CspPackageManager::packagePath(const QString &name, const QString &version)
{
    return m_packages[name][version].Path;
}

void CspPackageManager::save()
{
    const QString yaml = dump();

    QFile file(m_repositoryIndexFilePath);
    if (file.open(QIODevice::WriteOnly))
    {
        file.write(yaml.toUtf8());
        file.close();
    }
}

QString CspPackageManager::dump()
{
    const YAML::Node yaml = YAML::convert<PackagesType>::encode(m_packages);
    YAML::Emitter out;

    out << yaml;

    return QString(out.c_str());
}
