/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        utils.h
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
 *  2023-04-21     xqyjlj       initial version
 */

#ifndef COMMON_UTILS_H
#define COMMON_UTILS_H

#include <QApplication>
#include <QMessageBox>
#include <QString>

class utils {
public:
    /**
     * @brief Show an information message box.
     * @param message: the text to be displayed in the message box.
     * @param parent: the parent widget that owns the message box.
     */
    static void show_info(const QString &message, QWidget *parent = nullptr)
    {
        QMessageBox::information(parent, QObject::tr("Information"), message);
    }

    /**
     * @brief Show a warning message box.
     * @param message: the text to be displayed in the message box.
     * @param parent: the parent widget that owns the message box.
     */
    static void show_warning(const QString &message, QWidget *parent = nullptr)
    {
        QMessageBox::warning(parent, QObject::tr("Warning"), message);
    }

    /**
     * @brief Show a critical message box.
     * @param message: the text to be displayed in the message box.
     * @param parent: the parent widget that owns the message box.
     */
    static void show_critical(const QString &message, QWidget *parent = nullptr)
    {
        QMessageBox::critical(parent, QObject::tr("Critical"), message);
    }

    /**
     * @brief Show a error message box.
     * @param message: the text to be displayed in the message box.
     * @param parent: the parent widget that owns the message box.
     */
    static void show_error(const QString &message, QWidget *parent = nullptr)
    {
        QMessageBox::critical(parent, QObject::tr("Error"), message);
    }

    /**
     * @brief Display an error message and exit the application.
     * @param message: the text to be displayed in the message box.
     */
    static void show_error_and_exit(const QString &message)
    {
        QMessageBox::critical(nullptr, QObject::tr("Error"), message, QMessageBox::Ok);
        QApplication::quit();
    }

    /**
     * @brief Show a question message box.
     * @param message: the text to be displayed in the message box.
     * @param parent: the parent widget that owns the message box.
     */
    static void show_question(const QString &message, QWidget *parent = nullptr)
    {
        QMessageBox::question(parent, QObject::tr("Question"), message);
    }
};

#endif  // COMMON_UTILS_H