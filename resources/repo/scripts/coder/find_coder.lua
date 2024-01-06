--
-- Licensed under the GNU General Public License v. 3 (the "License")
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
-- Copyright (C) 2023-2024 xqyjlj<xqyjlj@126.com>
--
-- @author      xqyjlj
-- @file        find_coder.lua
--
-- Change Logs:
-- Date           Author       Notes
-- ------------   ----------   -----------------------------------------------
-- 2024-01-02     xqyjlj       initial version
--
import("core.base.semver")

function main(hal, name, repositories_dir)
    local moduledir
    local version
    local l = hal:split(" ")
    if #l == 1 then
        hal = l[1]
        version = "latest"
    elseif #l == 2 then
        hal = l[1]
        if l[2] == "latest" then
            version = "latest"
        else
            local ver = semver.new(l[2])
            version = string.format("v%s.%s.%s", ver:major(), ver:minor(), ver:patch())
        end
    else
        assert(false, "invalid hal (%s)", hal)
    end
    local haldir = path.join(repositories_dir, hal, version)
    coder = assert(import("tools.coder.xmake", {anonymous = true, try = true, rootdir = haldir}),
                   "coder %s not found! repositories: %s", hal, haldir)
    if not coder.moduledir then
        coder.moduledir = function()
            return hal
        end
    end
    return coder
end
