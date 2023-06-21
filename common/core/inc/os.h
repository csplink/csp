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

class os {
public:
    /**
     * @brief Show an information message box.
     * @param message: the text to be displayed in the message box.
     * @param parent: the parent widget that owns the message box.
     */
    static void
    show_info(const QString &message, const QString &title = QObject::tr("Information"), QWidget *parent = nullptr);

    /**
     * @brief Show a warning message box.
     * @param message: the text to be displayed in the message box.
     * @param parent: the parent widget that owns the message box.
     */
    static void
    show_warning(const QString &message, const QString &title = QObject::tr("Warning"), QWidget *parent = nullptr);

    /**
     * @brief Show a critical message box.
     * @param message: the text to be displayed in the message box.
     * @param parent: the parent widget that owns the message box.
     */
    static void
    show_critical(const QString &message, const QString &title = QObject::tr("Critical"), QWidget *parent = nullptr);

    /**
     * @brief Show a error message box.
     * @param message: the text to be displayed in the message box.
     * @param parent: the parent widget that owns the message box.
     */
    static void
    show_error(const QString &message, const QString &title = QObject::tr("Error"), QWidget *parent = nullptr);

    /**
     * @brief Display an error message and exit the application.
     * @param message: the text to be displayed in the message box.
     */
    static void show_error_and_exit(const QString &message,
                                    const QString &title  = QObject::tr("Critical"),
                                    QWidget       *parent = nullptr);

    /**
     * @brief Show a question message box.
     * @param message: the text to be displayed in the message box.
     * @param parent: the parent widget that owns the message box.
     */
    static void
    show_question(const QString &message, const QString &title = QObject::tr("Question"), QWidget *parent = nullptr);

    /**
     * @brief open a url in the default browser.
     * @param url: the url to be opened.
     */
    static void open_url(const QString &url);

    /**
     * @brief check if the directory exists.
     * @param p: path
     * @return true if the directory exists, otherwise false.
     */
    static bool isdir(const QString &p);

    /**
     * @brief check if the file exists.
     * @param p: path
     * @return true if the file exists, otherwise false.
     */
    static bool isfile(const QString &p);

    /**
     * @brief check if the path exists.
     * @param p: path
     * @return true if the path exists, otherwise false.
     */
    static bool exists(const QString &p);

    /**
     * @brief open dialog and get an existing directory selected by the user.
     * @return directory.
     */
    static QString getexistdir();

    /**
     * @brief traverse to get all the files in the specified directory
     * @param p: directory path
     * @param filters: file filter
     * @return file list
     */
    static QStringList files(const QString &p, const QStringList &filters);

    /**
     * @brief traverse to get all the files in the specified directory
     * @param p: directory path
     * @param filters: file filter
     * @return file list
     */
    static QStringList files(const QString &p, const QString &filter);

    /**
     * @brief traverse to get all the directories in the specified directory
     * @param p: directory path
     * @param filters: file filter
     * @return directory list
     */
    static QStringList dirs(const QString &p, const QStringList &filters);

    /**
     * @brief traverse to get all the directories in the specified directory
     * @param p: directory path
     * @param filters: file filter
     * @return directory list
     */
    static QStringList dirs(const QString &p, const QString &filter);

private:
    os();
    ~os();

    os(const os &signal);
    const os &operator=(const os &signal);
};

#endif  // COMMON_CORE_CSP_OS_H
