/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        PackageDescriptionTable.h
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
 *  Copyright (C) 2023-2024 xqyjlj<xqyjlj@126.com>
 *
 * ****************************************************************************
 *  Change Logs:
 *  Date           Author       Notes
 *  ------------   ----------   -----------------------------------------------
 *  2023-06-04     xqyjlj       initial version
 */

#ifndef PACKAGE_DESCRIPTION_TABLE_H
#define PACKAGE_DESCRIPTION_TABLE_H

#include <QDebug>
#include <QMap>

class PackageDescriptionTable final : public QObject
{
    Q_OBJECT
  public:
    typedef struct
    {
        QString Name;
        QString Email;
        QMap<QString, QString> Website;
    } AuthorType;

    typedef struct
    {
        AuthorType Author;
        QString Name;
        QString Version;
        QString License;
        QString Type;
        QString Vendor;
        QMap<QString, QString> VendorUrl;
        QMap<QString, QString> Description;
        QMap<QString, QString> Url;
        QString SupportContact;
    } PackageDescriptionType;

    static bool loadPackageDescription(PackageDescriptionType *packageDescription, const QString &path);

  private:
    explicit PackageDescriptionTable();
    ~PackageDescriptionTable();
};

QDebug operator<<(QDebug, const PackageDescriptionTable::PackageDescriptionType &);
QDebug operator<<(QDebug, const PackageDescriptionTable::AuthorType &);

#endif /** PACKAGE_DESCRIPTION_TABLE_H */
