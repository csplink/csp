/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        TestCaseQtJson.h
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
 *  2023-12-03     xqyjlj       initial version
 */

#include <QDebug>
#include <QtTest>

#include "QtJson.h"

class TestCaseQtJson final : public QObject
{
    Q_OBJECT

  private slots:
    static void qstring()
    {
        const nlohmann::json j = QString("test for qtjson");
        QCOMPARE(QString::fromStdString(j.dump()), R"("test for qtjson")");

        const nlohmann::json e = nlohmann::json::parse(R"("test for qtjson")");
        QString s;
        e.get_to(s);
        QCOMPARE(s, "test for qtjson");
    }

    static void qmap()
    {
        const nlohmann::json j = QMap<QString, QString>{{"type", "test"}};
        QCOMPARE(QString::fromStdString(j.dump()), R"({"type":"test"})");

        const nlohmann::json e = nlohmann::json::parse(R"({"type":"test"})");
        QMap<QString, QString> m;
        e.get_to(m);
        QVERIFY(!m.isEmpty());
        QVERIFY(m.contains("type"));
        QCOMPARE(m["type"], "test");
    }

    static void qvector()
    {
        const nlohmann::json j = QVector<QString>{"1", "2", "3"};
        QCOMPARE(QString::fromStdString(j.dump()), R"(["1","2","3"])");

        const nlohmann::json e = nlohmann::json::parse(R"(["1","2","3"])");
        QVector<QString> v;
        e.get_to(v);
        QVERIFY(!v.isEmpty());
        QCOMPARE(v.at(0), "1");
        QCOMPARE(v.length(), 3);
    }

    static void qlist()
    {
        const nlohmann::json j = QList<QString>{"1", "2", "3"};
        QCOMPARE(QString::fromStdString(j.dump()), R"(["1","2","3"])");

        const nlohmann::json e = nlohmann::json::parse(R"(["1","2","3"])");
        QList<QString> v;
        e.get_to(v);
        QVERIFY(!v.isEmpty());
        QCOMPARE(v.at(0), "1");
        QCOMPARE(v.length(), 3);
    }
};

QTEST_MAIN(TestCaseQtJson)

#include "TestCaseQtJson.moc"
