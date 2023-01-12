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
// @file        NetUtil.cs
//
// Change Logs:
// Date           Author       Notes
// ------------   ----------   -----------------------------------------------
// 2023-01-13     xqyjlj       add ping
// 2023-01-11     xqyjlj       initial version
//

using System;
using System.Net;
using System.Net.Http;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace CSP.Utils;

public static class NetUtil
{
    public static async Task<bool> Check(string url) {
        SocketsHttpHandler socketsHttpHandler = new() {
            AllowAutoRedirect = true,
            UseCookies        = false
        };
        HttpClient client = new(socketsHttpHandler);
        HttpResponseMessage response = await client.SendAsync(new HttpRequestMessage {
            Method     = new HttpMethod("HEAD"),
            RequestUri = new Uri(url)
        });

        return response.StatusCode == HttpStatusCode.OK;
    }

    public static float Ping(string url) {
        string          host      = "";
        Regex           httpRegex = new(@"(?<=http[s]{0,1}://).*?(?=/)"); //http[s]://xxx.com/..
        Regex           gitRegex  = new(@"(?<=git@).*?(?=:)");            //git@git.xxx.com:xxx/xxx.git
        MatchCollection mc        = httpRegex.Matches(url);

        if (mc.Count != 1) {
            mc = gitRegex.Matches(url);
            if (mc.Count == 1) {
                host = mc[0].Value;
            }
        }
        else {
            host = mc[0].Value;
        }

        var (stdOutput, _, _) = Util.Run("ping", $"-n 1 -w 1000 {host}");
        Regex pingRegex1 = new(@"(?<=[=<])\d+(\.\d+)?(?=ms TTL=)");
        Regex pingRegex2 = new(@"(?<=time[=<])\d+(\.\d+)?(?= ms)");

        mc = pingRegex1.Matches(stdOutput);
        string timeVal = "65535";
        if (mc.Count != 1) {
            mc = pingRegex2.Matches(stdOutput);
            if (mc.Count == 1) {
                timeVal = mc[0].Value;
            }
        }
        else {
            timeVal = mc[0].Value;
        }

        if (float.TryParse(timeVal, out float time)) {
            return time;
        }

        return 65535;
    }
}