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
// 2023-01-11     xqyjlj       initial version
//

using System;
using System.Net;
using System.Net.Http;
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
}