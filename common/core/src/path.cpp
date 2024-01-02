/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        path.cpp
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
 *  2023-06-17     xqyjlj       initial version
 */

#include <QApplication>
#include <QDir>
#include <QFileInfo>

#include "os.h"
#include "path.h"

QString path::basename(const QString &p)
{
    if (p.isEmpty())
        return "";

    const QFileInfo info(p);
    return info.baseName();
}

QString path::filename(const QString &p)
{
    if (p.isEmpty())
        return "";

    if (os::isdir(p))
        return "";

    const QFileInfo info(p);
    return info.fileName();
}

QString path::extension(const QString &p)
{
    if (p.isEmpty())
        return "";

    const QFileInfo info(p);
    return info.suffix();
}

QString path::directory(const QString &p)
{
    if (p.isEmpty())
        return "";

    const QFileInfo info(p);
    return info.dir().absolutePath();
}

QString path::relative(const QString &p, const QString &rootdir)
{
    if (!os::exists(p) || !os::exists(rootdir))
        return "";

    const QDir root(rootdir);
    return root.relativeFilePath(p);
}

QString path::absolute(const QString &p, const QString &rootdir)
{
    if (!os::exists(p) || !os::exists(rootdir))
        return "";

    const QDir root(rootdir);
    return root.absoluteFilePath(p);
}

bool path::is_absolute(const QString &p)
{
    if (!os::exists(p))
        return false;

    const QFileInfo info(p);
    return info.isAbsolute();
}

QString path::appfile()
{
    return QCoreApplication::applicationFilePath();
}

QString path::appdir()
{
    return QCoreApplication::applicationDirPath();
}
