#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the GNU General Public License v. 3 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/gpl-3.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2022-2024 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        database.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-24     xqyjlj       initial version
#

from jsonschema import validate
import yaml


class Database():

    def  checkPinout(self,pinout:dict)->bool :
        if pinout!=None:
            if isinstance(pinout,list):
                for pin_name, pin_info in  pinout.items():

            else:
                return False
        else:
            return False

    def getPinout(self, path: str) -> dict:
        with open(path, 'r', encoding='utf-8') as f:
            pinout = yaml.load(f.read(), Loader=yaml.FullLoader)


        if pinout!=None:
            for p in  pinout.items():

        auto pinout_i = pinout->constBegin();
        while (pinout_i != pinout->constEnd())
        {
            const QString &key = pinout_i.key();
            const PinoutUnitType &unit = pinout_i.value();
            const int &position = unit.Position;
            const QString &type = unit.Type;
            const QMap<QString, FunctionType> &functions = pinout_i.value().Functions;
            if (position > 0 && !type.isEmpty())
            {
                if (type == "I/O")
                {
                    if (functions.isEmpty())
                    {
                        qCritical().noquote() << QString("%1: pinout %2`s functions is empty").arg(path, key);
                        /** TODO: error */
                    }
                }
                else if (type == "Power" || type == "NC" || type == "Boot" || type == "Reset")
                { /* do nothings */
                }
                else
                {
                    qCritical().noquote()
                        << QString("%1: pinout %2`s type<%3> is invalid").arg(path, key, type);
                    /** TODO: error */
                }

                ++pinout_i;
            }
            else
            {
                /** TODO: QString("%1: pinout %2`s position<%3> is invalid").arg(path, key).arg(position);
                    *        QString("%1: pinout %2`s type is empty").arg(path, key);
                    */
            }
        }

        return result

    def getPinout(self, vendor: str, hal: str, name: str) -> dict:
        return self.getPinout(f"resource/database/hal/{vendor}/{hal}/{name}/pinout.yml")
