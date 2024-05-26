/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        Settings.h
 * @brief
 *
 *****************************************************************************
 * @attention
 * Licensed under the GNU General Public License v. 3 (the "License")
 * You may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.gnu.org/licenses/gpl-3.0.html
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Copyright (C) 2024-2024 xqyjlj<xqyjlj@126.com>
 *
 *****************************************************************************
 * Change Logs:
 * Date           Author       Notes
 * ------------   ----------   -----------------------------------------------
 * 2024-04-27     xqyjlj       initial version
 */

#ifndef SETTINGS_H
#define SETTINGS_H

#include <QObject>
#include <QSettings>

class CspSettings final : public QObject
{
    Q_OBJECT
  public:
    explicit CspSettings();
    static CspSettings &singleton();

    /**
     * @brief get the display language
     *
     * @note default: "QLocale()"
     *
     * @synchronous true
     *
     * @reentrancy true
     *
     * @return QString: language
     */
    QString language() const;

    /**
     * @brief set the display language
     *
     * @param[in] language language
     *
     * @synchronous true
     *
     * @reentrancy true
     */
    void setLanguage(const QString &language);

    /**
     * @brief get the database directory
     *
     * @note default: "database"
     *
     * @synchronous true
     *
     * @reentrancy true
     *
     * @return QString: the database directory
     */
    QString database() const;

    /**
     * @brief set the database directory
     *
     * @param[in] database the database directory
     *
     * @synchronous true
     *
     * @reentrancy true
     */
    void setDatabase(const QString &database);

    QString workspace() const;
    void setWorkspace(const QString &workspace);

    QString repository() const;
    void setRepository(const QString &repository);

    QString tools() const;
    void setTools(const QString &tools);

    QString xmake() const;
    void setXmake(const QString &xmake);

    QString git() const;
    void setGit(const QString &git);

    QString python() const;
    void setPython(const QString &python);

    QString openPath() const;
    void setOpenPath(const QString &path);

    QString packagePath() const;
    void setPackagePath(const QString &path);

    QMap<QString, QString> env() const;

  private:
    QSettings m_settings;
    QSettings m_recent;

    static void checkDirValid(const char *key, const QString &dir, bool create);

    Q_DISABLE_COPY_MOVE(CspSettings)
};

#define Settings CspSettings::singleton()

#endif /** SETTINGS_H */
