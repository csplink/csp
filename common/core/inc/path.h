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

namespace csp {

class path {
public:
    static QString basename(const QString &p);
    static QString filename(const QString &p);
    static QString extension(const QString &p);
    static QString directory(const QString &p);
    static QString relative(const QString &p, const QString &rootdir = ".");
    static QString absolute(const QString &p, const QString &rootdir = ".");
    static bool    is_absolute(const QString &p);
    static QString appfile();
    static QString appdir();

private:
    path();
    ~path();

    path(const path &signal);
    const path &operator=(const path &signal);
};

}  // namespace csp

#endif  // CSP_PATH_H
