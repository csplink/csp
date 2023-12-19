--
-- Licensed under the GNU General Public License v. 3 (the "License");
-- You may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--     https://www.gnu.org/licenses/gpl-3.0.html
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.
--
-- Copyright (C) 2023-2023 xqyjlj<xqyjlj@126.com>
--
-- @author      xqyjlj
-- @file        dump_package.lua
--
-- Change Logs:
-- Date           Author       Notes
-- ------------   ----------   -----------------------------------------------
-- 2023-12-17     xqyjlj       initial version
--
import("lib.detect.find_tool")
import("core.package.package")
import("core.base.json")
import("core.base.option")

local packagelist = {toolchain = {}, library = {}}

function init_packagelist()
    for _, packagedir in ipairs(os.dirs(path.absolute(path.join(os.scriptdir(), "..", "..", "..", "xmake", "packages",
                                                                "*", "*")))) do
        local packagename = path.filename(packagedir)
        local packagefile = path.join(packagedir, "xmake.lua")
        local packageinstance = package.load_from_repository(packagename, packagedir, {packagefile = packagefile})
        local on_load = packageinstance:get("load")
        if on_load then
            on_load(packageinstance)
        end
        local pkg = {}
        local urls = packageinstance:get("urls") or os.raise("%s urls is empty", packagename)
        local versions = packageinstance:get("versions") or {latest = "nil"}
        local description = packageinstance:get("description") or "unknown"
        local homepage = packageinstance:get("homepage") or "unknown"
        local license = packageinstance:get("license") or "unknown"

        if type(urls) == "table" then
            pkg["urls"] = urls
        else
            pkg["urls"] = {urls}
        end

        pkg["versions"] = packageinstance:get("versions") or {latest = "nil"}
        pkg["description"] = description
        pkg["homepage"] = homepage
        pkg["license"] = license

        if packageinstance:get("kind") then
            packagelist[packageinstance:get("kind")][packagename] = pkg
        else
            packagelist["library"][packagename] = pkg
        end
    end
end

function dump_json()
    local jsonstr = json.encode(packagelist)
    print(jsonstr)
end

-- LuaFormatter off
local common_options = {
    {nil,   "json",             "k",    nil,                                        "export as json."},
    {nil,   "dump",             "k",    nil,                                        "export as lua table."},
    {"h",   "help",             "k",    nil,                                        "print this help message and exit."},
}
-- LuaFormatter on

function usage()
    option.show_logo()
    option.show_options(common_options)
end

function main(...)
    local argv = table.pack(...)
    local results, errors = option.raw_parse(argv, common_options)
    if results then
        if results["help"] then
            usage()
        elseif results["json"] then
            init_packagelist()
            dump_json()
        elseif results["dump"] then
            init_packagelist()
            print(packagelist)
        else
            usage()
        end
    end
end
