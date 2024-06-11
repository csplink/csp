/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        Debug.h
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
 *  Copyright (C) 2024-2024 xqyjlj<xqyjlj@126.com>
 *
 * ****************************************************************************
 *  Change Logs:
 *  Date           Author       Notes
 *  ------------   ----------   -----------------------------------------------
 *  2024-06-07     xqyjlj       initial version
 */

#ifndef DEBUG_H
#define DEBUG_H

#include <QDebug>
#include <QObject>
#include <QThread>

#define LOG_D()                     qDebug().noquote()
#define LOG_I()                     qInfo().noquote()
#define LOG_W()                     qWarning().noquote()
#define LOG_E()                     qCritical().noquote()

#define SHOW_I(PARENT, TITLE, TEXT) Debug.showInformationMessageBox(PARENT, TITLE, TEXT)

#define SHOW_W(PARENT, TITLE, TEXT) Debug.showWarningMessageBox(PARENT, TITLE, TEXT)

#define SHOW_E(PARENT, TITLE, TEXT) Debug.showCriticalMessageBox(PARENT, TITLE, TEXT)

class CspDebug final : public QObject
{
    Q_OBJECT
  public:
    enum
    {
        MessageBoxInformation,
        MessageBoxWarning,
        MessageBoxCritical,
    };

    explicit CspDebug();
    static CspDebug &singleton();

    void showInformationMessageBox(QWidget *parent, const QString &title, const QString &text);
    void showWarningMessageBox(QWidget *parent, const QString &title, const QString &text);
    void showCriticalMessageBox(QWidget *parent, const QString &title, const QString &text);

  signals:
    void signalShowMessageBox(int type, const QString &title, const QString &message);

  private:
    QThread *m_mainThread;

    Q_DISABLE_COPY_MOVE(CspDebug)
};

#define Debug CspDebug::singleton()

#endif /** DEBUG_H */
