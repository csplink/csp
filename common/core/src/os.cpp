/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        os.cpp
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
 *  2023-05-25     xqyjlj       initial version
 */

#include <QApplication>
#include <QDebug>
#include <QDesktopServices>
#include <QFileDialog>
#include <QFileInfo>
#include <QMessageBox>
#include <QProcess>
#include <QString>
#include <QTemporaryFile>
#include <QUrl>

#include "os.h"

void os::show_info(const QString &message, const QString &title, QWidget *parent)
{
    QMessageBox::information(parent, title, message);
}

void os::show_warning(const QString &message, const QString &title, QWidget *parent)
{
    QMessageBox::warning(parent, title, message);
}

void os::show_critical(const QString &message, const QString &title, QWidget *parent)
{
    QMessageBox::critical(parent, title, message);
}

void os::show_error(const QString &message, const QString &title, QWidget *parent)
{
    QMessageBox::critical(parent, title, message);
}

void os::show_error_and_exit(const QString &message, const QString &title, QWidget *parent)
{
    QMessageBox::critical(parent, title, message, QMessageBox::Ok);
    QApplication::quit();
}

void os::show_question(const QString &message, const QString &title, QWidget *parent)
{
    QMessageBox::question(parent, title, message);
}

void os::open_url(const QString &url)
{
    Q_ASSERT(!url.isEmpty());

    QDesktopServices::openUrl(QUrl(url));
}

bool os::rmdir(const QString &dir)
{
    Q_ASSERT(!dir.isEmpty());

    if (!isdir(dir))
        return false;

    QDir d(dir);
    return d.removeRecursively();
}

void os::mkdir(const QString &dir)
{
    Q_ASSERT(!dir.isEmpty());

    if (isdir(dir))
        return;

    const QDir d(dir);
}

bool os::isdir(const QString &p)
{
    if (p.isEmpty())
        return false;

    const QFileInfo fi(p);
    return fi.isDir();
}

bool os::isfile(const QString &p)
{
    if (p.isEmpty())
        return false;

    const QFileInfo fi(p);
    return fi.isFile();
}

bool os::exists(const QString &p)
{
    if (p.isEmpty())
        return false;

    const QFileInfo fi(p);
    return fi.exists();
}

QString os::getexistdir()
{
    return QFileDialog::getExistingDirectory();
}

QString os::getexistfile()
{
    return QFileDialog::getOpenFileName();
}

QString os::getsavefile(const QString &title, const QString &default_file, const QString &filter)
{
    return QFileDialog::getSaveFileName(nullptr, title, default_file, filter);
}

QStringList os::files(const QString &p, const QStringList &filters)
{
    if (!isdir(p))
        return {};

    const QDir  dir(p);
    auto        files = dir.entryInfoList(filters, QDir::Files | QDir::Hidden | QDir::NoSymLinks);
    QStringList paths;
    for (const QFileInfo &file : files)
        paths.append(file.absoluteFilePath());

    return paths;
}

QStringList os::files(const QString &p, const QString &filter)
{
    return files(p, QStringList() << filter);
}

QStringList os::dirs(const QString &p, const QStringList &filters)
{
    if (!isdir(p))
        return {};

    const QDir  dir(p);
    auto        dirs = dir.entryInfoList(filters, QDir::Dirs | QDir::NoDotAndDotDot | QDir::NoSymLinks);
    QStringList paths;
    for (const QFileInfo &info : dirs)
        paths.append(info.absoluteFilePath());

    return paths;
}

QStringList os::dirs(const QString &p, const QString &filter)
{
    return dirs(p, QStringList() << filter);
}

bool os::execvf(const QString                &program,
                const QStringList            &argv,
                const QMap<QString, QString> &env,
                const int                     msecs,
                const QString                &workdir,
                const QString                &output_file,
                const QString                &error_file)
{
    QProcess            process;
    const bool          use_output  = !output_file.isEmpty();
    const bool          use_error   = !error_file.isEmpty();
    QProcessEnvironment environment = QProcessEnvironment::systemEnvironment();

    Q_ASSERT(!program.isEmpty());

    auto env_i = env.constBegin();
    while (env_i != env.constEnd())
    {
        environment.insert(env_i.key(), env_i.value());
        ++env_i;
    }

    process.setProgram(program);
    process.setArguments(argv);
    process.setProcessEnvironment(environment);

    if (use_output)
        process.setStandardOutputFile(output_file);
    if (use_error)
        process.setStandardErrorFile(error_file);
    if (isdir(workdir))
        process.setWorkingDirectory(workdir);

    process.start();

    if (!process.waitForFinished(msecs))
        return false;

    return true;
}

bool os::execv(const QString                &program,
               const QStringList            &argv,
               const QMap<QString, QString> &env,
               int                           msecs,
               const QString                &workdir,
               QByteArray                   *output,
               QByteArray                   *error)
{
    QProcess            process;
    QProcessEnvironment environment = QProcessEnvironment::systemEnvironment();

    Q_ASSERT(!program.isEmpty());

    auto env_i = env.constBegin();
    while (env_i != env.constEnd())
    {
        environment.insert(env_i.key(), env_i.value());
        ++env_i;
    }

    process.setProgram(program);
    process.setArguments(argv);
    process.setProcessEnvironment(environment);

    if (isdir(workdir))
        process.setWorkingDirectory(workdir);

    process.start();

    if (!process.waitForFinished(msecs))
        return false;

    if (output != nullptr)
        *output = process.readAllStandardOutput();
    if (error != nullptr)
        *error = process.readAllStandardError();

    return true;
}

QByteArray os::readfile(const QString &p)
{
    if (!isfile(p))
        return {};

    QFile file(p);

    if (!file.open(QIODevice::ReadOnly))
        return {};
    QByteArray data = file.readAll();
    file.close();

    return data;
}

bool os::writefile(const QString &p, const QByteArray &data, bool overwrite)
{
    Q_ASSERT(!p.isEmpty());

    QIODevice::OpenMode mode;

    if (data.isEmpty())
        return false;

    QFile file(p);

    if (overwrite)
        mode = QIODevice::WriteOnly;
    else
        mode = QIODevice::Append;

    if (!file.open(mode))
        return false;

    file.write(data);
    file.close();

    return true;
}

bool os::rm(const QString &p)
{
    if (isfile(p))
    {
        return QFile::remove(p);
    }
    else if (isdir(p))
    {
        QDir dir(p);
        return dir.removeRecursively();
    }
    return false;
}
