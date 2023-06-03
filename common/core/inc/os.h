/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        os.h
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

#ifndef COMMON_CORE_CSP_OS_H
#define COMMON_CORE_CSP_OS_H

#include <QApplication>
#include <QDesktopServices>
#include <QFileDialog>
#include <QFileInfo>
#include <QMessageBox>
#include <QString>
#include <QUrl>

namespace csp {
class os {
public:
    /**
     * @brief Show an information message box.
     * @param message: the text to be displayed in the message box.
     * @param parent: the parent widget that owns the message box.
     */
    static void
    show_info(const QString &message, const QString &title = QObject::tr("Information"), QWidget *parent = nullptr)
    {
        QMessageBox::information(parent, title, message);
    }

    /**
     * @brief Show a warning message box.
     * @param message: the text to be displayed in the message box.
     * @param parent: the parent widget that owns the message box.
     */
    static void
    show_warning(const QString &message, const QString &title = QObject::tr("Warning"), QWidget *parent = nullptr)
    {
        QMessageBox::warning(parent, title, message);
    }

    /**
     * @brief Show a critical message box.
     * @param message: the text to be displayed in the message box.
     * @param parent: the parent widget that owns the message box.
     */
    static void
    show_critical(const QString &message, const QString &title = QObject::tr("Critical"), QWidget *parent = nullptr)
    {
        QMessageBox::critical(parent, title, message);
    }

    /**
     * @brief Show a error message box.
     * @param message: the text to be displayed in the message box.
     * @param parent: the parent widget that owns the message box.
     */
    static void
    show_error(const QString &message, const QString &title = QObject::tr("Error"), QWidget *parent = nullptr)
    {
        QMessageBox::critical(parent, title, message);
    }

    /**
     * @brief Display an error message and exit the application.
     * @param message: the text to be displayed in the message box.
     */
    static void
    show_error_and_exit(const QString &message, const QString &title = QObject::tr("Critical"), QWidget *parent = nullptr)
    {
        QMessageBox::critical(parent, title, message, QMessageBox::Ok);
        QApplication::quit();
    }

    /**
     * @brief Show a question message box.
     * @param message: the text to be displayed in the message box.
     * @param parent: the parent widget that owns the message box.
     */
    static void
    show_question(const QString &message, const QString &title = QObject::tr("Question"), QWidget *parent = nullptr)
    {
        QMessageBox::question(parent, title, message);
    }

    static void open_url(const QString &url)
    {
        Q_ASSERT(!url.isEmpty());

        QDesktopServices::openUrl(QUrl(url));
    }

    static bool isdir(const QString &path)
    {
        if (path.isEmpty())
            return false;

        QFileInfo fi(path);
        return fi.isDir();
    }

    static bool isfile(const QString &path)
    {
        if (path.isEmpty())
            return false;

        QFileInfo fi(path);
        return fi.isFile();
    }

    static bool exists(const QString &path)
    {
        if (path.isEmpty())
            return false;

        QFileInfo fi(path);
        return fi.exists();
    }

    static QString getexistdir()
    {
        return QFileDialog::getExistingDirectory();
    }

    static QStringList files(const QString &path, const QStringList &filters)
    {
        QDir        dir(path);
        auto        files = dir.entryInfoList(filters, QDir::Files | QDir::Hidden | QDir::NoSymLinks);
        QStringList paths;
        for (const QFileInfo &file : files)
            paths.append(file.absoluteFilePath());

        return paths;
    }

    static QStringList files(const QString &path, const QString &filter)
    {
        return files(path, QStringList() << filter);
    }

    static QStringList dirs(const QString &path, const QStringList &filters)
    {
        QDir        dir(path);
        auto        dirs = dir.entryInfoList(filters, QDir::Dirs | QDir::NoDotAndDotDot | QDir::NoSymLinks);
        QStringList paths;
        for (const QFileInfo &_dir : dirs)
            paths.append(_dir.absoluteFilePath());

        return paths;
    }

    static QStringList dirs(const QString &path, const QString &filter)
    {
        return dirs(path, QStringList() << filter);
    }
};
}  // namespace csp

#endif  // COMMON_CORE_CSP_OS_H
