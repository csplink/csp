/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        Debug.cpp
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

#include <QCoreApplication>
#include <QGlobalStatic>
#include <QMessageBox>
#include <QThread>

#include "Debug.h"

Q_GLOBAL_STATIC(QScopedPointer<CspDebug>, instance)

CspDebug::CspDebug()
    : QObject(),
      m_mainThread(nullptr)
{
    m_mainThread = QCoreApplication::instance()->thread();
}

CspDebug &CspDebug::singleton()
{
    if (!*instance)
    {
        instance->reset(new CspDebug());
    }
    return **instance;
}

void CspDebug::showInformationMessageBox(QWidget *parent, const QString &title, const QString &text)
{
    LOG_I() << QString("%1:: %2").arg(title, text);
    if (QThread::currentThread() != m_mainThread)
    {
        emit signalShowMessageBox(MessageBoxInformation, title, text);
    }
    else
    {
        QMessageBox::information(parent, title, text);
    }
}

void CspDebug::showWarningMessageBox(QWidget *parent, const QString &title, const QString &text)
{
    LOG_W() << QString("%1:: %2").arg(title, text);
    if (QThread::currentThread() != m_mainThread)
    {
        emit signalShowMessageBox(MessageBoxWarning, title, text);
    }
    else
    {
        QMessageBox::warning(parent, title, text);
    }
}

void CspDebug::showCriticalMessageBox(QWidget *parent, const QString &title, const QString &text)
{
    LOG_E() << QString("%1:: %2").arg(title, text);
    if (QThread::currentThread() != m_mainThread)
    {
        emit signalShowMessageBox(MessageBoxCritical, title, text);
    }
    else
    {
        QMessageBox::critical(parent, title, text);
    }
}
