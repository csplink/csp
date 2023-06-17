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

#include "os.h"

namespace csp {

os::os() = default;

os::~os() = default;

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

bool os::isdir(const QString &p)
{
    if (p.isEmpty())
        return false;

    QFileInfo fi(p);
    return fi.isDir();
}

bool os::isfile(const QString &p)
{
    if (p.isEmpty())
        return false;

    QFileInfo fi(p);
    return fi.isFile();
}

bool os::exists(const QString &p)
{
    if (p.isEmpty())
        return false;

    QFileInfo fi(p);
    return fi.exists();
}

QString os::getexistdir()
{
    return QFileDialog::getExistingDirectory();
}

QStringList os::files(const QString &p, const QStringList &filters)
{
    if (!isdir(p))
        return {};

    QDir        dir(p);
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

    QDir        dir(p);
    auto        dirs = dir.entryInfoList(filters, QDir::Dirs | QDir::NoDotAndDotDot | QDir::NoSymLinks);
    QStringList paths;
    for (const QFileInfo &_dir : dirs)
        paths.append(_dir.absoluteFilePath());

    return paths;
}

QStringList os::dirs(const QString &p, const QString &filter)
{
    return dirs(p, QStringList() << filter);
}

}  // namespace csp
