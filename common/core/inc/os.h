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

#include <QMap>
#include <QObject>
#include <QString>

class os final
{
  public:
    /**
     * @brief Show an information message box.
     * @param message: the text to be displayed in the message box.
     * @param title: windows title
     * @param parent: the parent widget that owns the message box.
     */
    static void show_info(const QString &message, const QString &title = QObject::tr("Information"),
                          QWidget *parent = nullptr);

    /**
     * @brief Show a warning message box.
     * @param message: the text to be displayed in the message box.
     * @param title: windows title
     * @param parent: the parent widget that owns the message box.
     */
    static void show_warning(const QString &message, const QString &title = QObject::tr("Warning"),
                             QWidget *parent = nullptr);

    /**
     * @brief Show a critical message box.
     * @param message: the text to be displayed in the message box.
     * @param title: windows title
     * @param parent: the parent widget that owns the message box.
     */
    static void show_critical(const QString &message, const QString &title = QObject::tr("Critical"),
                              QWidget *parent = nullptr);

    /**
     * @brief Show a error message box.
     * @param message: the text to be displayed in the message box.
     * @param title: windows title
     * @param parent: the parent widget that owns the message box.
     */
    static void show_error(const QString &message, const QString &title = QObject::tr("Error"),
                           QWidget *parent = nullptr);

    /**
     * @brief Display an error message and exit the application.
     * @param title: windows title
     * @param parent: windows parent
     * @param message: the text to be displayed in the message box.
     */
    static void show_error_and_exit(const QString &message, const QString &title = QObject::tr("Critical"),
                                    QWidget *parent = nullptr);

    /**
     * @brief Show a question message box.
     * @param message: the text to be displayed in the message box.
     * @param title: windows title
     * @param parent: the parent widget that owns the message box.
     */
    static void show_question(const QString &message, const QString &title = QObject::tr("Question"),
                              QWidget *parent = nullptr);

    /**
     * @brief open a url in the default browser.
     * @param url: the url to be opened.
     */
    static void open_url(const QString &url);

    /**
     * @brief delete only the directory.
     * @param dir: directory
     */
    static bool rmdir(const QString &dir);

    /**
     * @brief make a directory.
     * @param dir: directory
     */
    static void mkdir(const QString &dir);

    /**
     * @brief check if the directory exists.
     * @param path: path
     * @return true if the directory exists, otherwise false.
     */
    static bool isdir(const QString &path);

    /**
     * @brief check if the file exists.
     * @param path: path
     * @return true if the file exists, otherwise false.
     */
    static bool isfile(const QString &path);

    /**
     * @brief check if the path exists.
     * @param path: path
     * @return true if the path exists, otherwise false.
     */
    static bool exists(const QString &path);

    /**
     * @brief open dialog and get an existing directory selected by the user.
     * @return directory.
     */
    static QString getexistdir();

    /**
     * @brief open dialog and get an existing file selected by the user.
     * @return file path.
     */
    static QString getexistfile();

    /**
     * @brief open dialog and get a file name selected by the user.
     * @param title: dialog title
     * @param default_file: default file
     * @param filter: file filter
     * @return a file path selected by the user
     */
    static QString getsavefile(const QString &title = QObject::tr(""), const QString &default_file = QString(),
                               const QString &filter = QString());

    /**
     * @brief traverse to get all the files in the specified directory
     * @param p: directory path
     * @param filters: file filter
     * @return file list
     */
    static QStringList files(const QString &p, const QStringList &filters);

    /**
     * @brief traverse to get all the files in the specified directory
     * @param path: directory path
     * @param filter: file filter
     * @return file list
     */
    static QStringList files(const QString &path, const QString &filter);

    /**
     * @brief traverse to get all the directories in the specified directory
     * @param path: directory path
     * @param filters: file filter
     * @return directory list
     */
    static QStringList dirs(const QString &path, const QStringList &filters);

    /**
     * @brief traverse to get all the directories in the specified directory
     * @param path: directory path
     * @param filter: file filter
     * @return directory list
     */
    static QStringList dirs(const QString &path, const QString &filter);

    /**
     * @brief running native shell commands with file log
     * @param program: program path or name
     * @param argv: argument vector
     * @param env: environment variable settings
     * @param msecs: timeout milliseconds
     * @param workdir: working directory
     * @param output_file: the process' standard output to the file fileName
     * @param error_file: the process' standard error to the file fileName
     * @return true if run successfully, otherwise false.
     */
    static bool execvf(const QString &program, const QStringList &argv = {}, const QMap<QString, QString> &env = {},
                       int msecs = 30000, const QString &workdir = "", const QString &output_file = "",
                       const QString &error_file = "");

    /**
     * @brief running native shell commands with qbytearray log
     * @param program: program path or name
     * @param argv: argument vector
     * @param env: environment variable settings
     * @param msecs: timeout milliseconds
     * @param workdir: working directory
     * @param output: the process' standard output to the qbytearray
     * @param error: the process' standard error to the qbytearray
     * @return true if run successfully, otherwise false.
     */
    static bool execv(const QString &program, const QStringList &argv = {}, const QMap<QString, QString> &env = {},
                      int msecs = 30000, const QString &workdir = "", QByteArray *output = nullptr,
                      QByteArray *error = nullptr);

    /**
     * @brief read a file
     * @param path: path
     * @return file content
     */
    static QByteArray readfile(const QString &path);

    /**
     * @brief write data to file
     * @param path: path
     * @param data: data
     * @param overwrite: is overwrite
     * @return true if write successfully, otherwise false.
     */
    static bool writefile(const QString &path, const QByteArray &data, bool overwrite = true);

    /**
     * @brief delete files or directory trees
     * @param path: path
     * @return true if delete successfully, otherwise false.
     */
    static bool rm(const QString &path);

    /**
     * @brief where cond is a boolean expression, writes the warning "${{str}}" and
     * exits if cond is false.
     * @param cond: condition
     * @param str: message
     */
    static void raise(bool cond, const QString &str);

    /**
     * @brief where cond is a boolean expression, writes the warning "ASSERT: 'cond' in file xyz.cpp, line 234" and
     * exits if cond is false.
     * @param cond: condition
     * @param assertion: assert message
     * @param what: what
     * @param file: file
     * @param line: line
     */
    static void raise(bool cond, const char *assertion, const QString &what, const char *file, int line);

  private:
    os() = default;
    ~os() = default;

    Q_DISABLE_COPY_MOVE(os)
};

#define os_assert(cond, what) ((cond) ? static_cast<void>(0) : os::raise(0, #cond, what, __FILE__, __LINE__))

#endif // COMMON_CORE_CSP_OS_H
