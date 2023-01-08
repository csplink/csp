// Licensed under the Apache License, Version 2.0 (the "License");
// You may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// Copyright (C) 2022-2023 xqyjlj<xqyjlj@126.com>
//
// @author      xqyjlj
// @file        Icon.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-08     xqyjlj       initial version
//

using System.Windows.Media.Imaging;

namespace CSP.Resources
{
    public static class Icon
    {
        private static readonly IconInstance Instance = new();

        public static BitmapImage BlockEight {
            get => Instance.BlockEight;
        }

        public static BitmapImage BlockFive {
            get => Instance.BlockFive;
        }

        public static BitmapImage BlockFour {
            get => Instance.BlockFour;
        }

        public static BitmapImage BlockNine {
            get => Instance.BlockNine;
        }

        public static BitmapImage BlockOne {
            get => Instance.BlockOne;
        }

        public static BitmapImage BlocksAndArrows {
            get => Instance.BlocksAndArrows;
        }

        public static BitmapImage BlockSeven {
            get => Instance.BlockSeven;
        }

        public static BitmapImage BlockSix {
            get => Instance.BlockSix;
        }

        public static BitmapImage BlockTen {
            get => Instance.BlockTen;
        }

        public static BitmapImage BlockThree {
            get => Instance.BlockThree;
        }

        public static BitmapImage BlockTwo {
            get => Instance.BlockTwo;
        }

        public static BitmapImage C {
            get => Instance.C;
        }

        public static BitmapImage Chip {
            get => Instance.Chip;
        }

        public static BitmapImage CSharp {
            get => Instance.CSharp;
        }

        public static BitmapImage Error {
            get => Instance.Error;
        }

        public static BitmapImage Git {
            get => Instance.Git;
        }

        public static BitmapImage Information {
            get => Instance.Information;
        }

        public static BitmapImage Json {
            get => Instance.Json;
        }

        public static BitmapImage Lib {
            get => Instance.Lib;
        }

        public static BitmapImage Log {
            get => Instance.Log;
        }

        public static BitmapImage New {
            get => Instance.New;
        }

        public static BitmapImage Pdf {
            get => Instance.Pdf;
        }

        public static BitmapImage Pin {
            get => Instance.Pin;
        }

        public static BitmapImage PlayOne {
            get => Instance.PlayOne;
        }

        public static BitmapImage PPT {
            get => Instance.PPT;
        }

        public static BitmapImage Setting {
            get => Instance.Setting;
        }

        public static BitmapImage System {
            get => Instance.System;
        }

        public static BitmapImage Time {
            get => Instance.Time;
        }

        public static BitmapImage Timer {
            get => Instance.Timer;
        }

        public static BitmapImage Warning {
            get => Instance.Warning;
        }

        public static BitmapImage Xml {
            get => Instance.Xml;
        }

        public static BitmapImage YellowFolder {
            get => Instance.YellowFolder;
        }
    }
}