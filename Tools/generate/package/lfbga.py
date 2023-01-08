#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2022-2023 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        lfbga.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2023-01-08     xqyjlj       initial version
#

template_package = """<UserControl
    x:Class="CSP.Modules.Pages.MCU.Views.Components.Package.{type}.{name}View"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:lfbga="clr-namespace:CSP.Modules.Pages.MCU.Components.LFBGA"
    xmlns:panAndZoom="clr-namespace:Wpf.Controls.PanAndZoom;assembly=Wpf.Controls.PanAndZoom"
    xmlns:prism="http://prismlibrary.com/"
    Width="{width}"
    Height="{height}"
    prism:ViewModelLocator.AutoWireViewModel="True">
    <panAndZoom:ZoomBorder Stretch="None">
        <Border
            Background="#FFCBCEC1"
            BorderBrush="Black"
            BorderThickness="5">
            <Grid>
                <Grid.RowDefinitions>
{row_definitions}                </Grid.RowDefinitions>
                <Grid.ColumnDefinitions>
{column_definitions}                </Grid.ColumnDefinitions>
{data}            </Grid>
        </Border>
    </panAndZoom:ZoomBorder>
</UserControl>
"""

template_pin = """                <lfbga:Pin
                    Grid.Row="{row}"
                    Grid.Column="{column}"
                    DataContext="{{Binding Pins[{index}]}}"
                    Direction="Left" />
"""

seq = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "R", "T", "U", "V", "W", "Y"]


def generate_lfbga(name, config):
    row = config["number"]["row"]
    column = config["number"]["column"]
    type = config["type"]
    width = 150 * int(row)
    height = 150 * int(column)
    count = config["count"]
    row_definitions = ""
    column_definitions = ""
    for i in range(0, row):
        row_definitions += "                    <RowDefinition />\n"
    for i in range(0, column):
        column_definitions += "                    <ColumnDefinition />\n"
    pin = ""
    index = 0
    ignore = []
    for cfg in config["ignore"]:
        for key, item in cfg.items():
            r = seq.index(key)
            for i in item:
                ignore.append(r * int(column) + int(i) - 1)
    for i in range(0, row):
        for j in range(0, column):
            if not (i * column + j - 1) in ignore:
                pin += template_pin.format(row=i, column=j, index=index)
                index += 1
    if not index == count:
        raise ValueError("index: {index} != count: {count}".format(index=index, count=count))
    package = template_package.format(type=type,
                                      name=name.upper(),
                                      width=width,
                                      height=height,
                                      row_definitions=row_definitions,
                                      column_definitions=column_definitions,
                                      data=pin)
    return package
