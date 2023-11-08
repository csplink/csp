/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        path.h
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

#ifndef CSP_PATH_H
#define CSP_PATH_H

#include <QString>

class path final
{
  public:
    /**
     * @brief get the file name with no suffix at the end of the path
     * @param p: path
     * @return the file name with no suffix at the end of the path
     */
    static QString basename(const QString &p);

    /**
     * @brief get the file name with the last suffix of the path
     * @param p: path
     * @return the file name with the last suffix of the path
     */
    static QString filename(const QString &p);

    /**
     * @brief get the suffix of the path
     * @param p: path
     * @return the suffix of the path
     */
    static QString extension(const QString &p);

    /**
     * @brief get the directory of the path
     * @param p: path
     * @return the directory of the path
     */
    static QString directory(const QString &p);

    /**
     * @brief convert to relative path
     * @param p: path
     * @param rootdir: root directory
     * @return the relative path of the path
     */
    static QString relative(const QString &p, const QString &rootdir = ".");

    /**
     * @brief convert to absolute path
     * @param p: path
     * @param rootdir: root directory
     * @return the absolute path of the path
     */
    static QString absolute(const QString &p, const QString &rootdir = ".");

    /**
     * @brief check if the path is relative
     * @param p: path
     * @return true if the path is relative, otherwise false
     */
    static bool is_absolute(const QString &p);

    /**
     * @brief get the file path of the application executable
     * @return the file path of the application executable
     */
    static QString appfile();

    /**
     * @brief get the directory of the application executable
     * @return the directory of the application executable
     */
    static QString appdir();

  private:
    path() = default;
    ~path() = default;

    Q_DISABLE_COPY_MOVE(path)
};

#endif // CSP_PATH_H
