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
-- Copyright (C) 2023-2023 xqyjlj<xqyjlj@126.com>
--
-- @author      xqyjlj
-- @file        coder.lua
--
-- Change Logs:
-- Date           Author       Notes
-- ------------   ----------   -----------------------------------------------
-- 2023-12-19     xqyjlj       initial version
--
import("core.base.json")
import("core.base.option")
import("core.base.semver")

local license = [[
/**
 * ****************************************************************************
 *  @author      ${{author}}
 *  @file        ${{file}}
 *  @brief       ${{brief}}
 *
 * ****************************************************************************
 *  @attention
 *
 *  Copyright (C) ${{date}} csplink software.
 *  All rights reserved.
 *
 * ****************************************************************************
 */
]]

local user_code_begin_template = "/**< add user code begin %s */"
local user_code_end_template = "/**> add user code end %s */"
local user_code_begin_match = "/%*%*< add user code begin " -- .. "(.-) %*/"
local user_code_end_match = "/%*%*> add user code end " -- .. "(.-) %*/"

local project_table = {}
local user_code = {header = nil}

function find_coder(company, hal, name)
    local moduledir
    moduledir = string.format("%s.%s.xmake", string.lower(company), string.lower(hal))
    coder = assert(import(moduledir, {anonymous = true, try = true}), "coder %s not found!", moduledir)
    if not coder.moduledir then
        coder.moduledir = function()
            return moduledir
        end
    end
    return coder
end

function generate_header(file, project, coder, user)
    user = user or {}
    file:print(user_code_begin_template, "header")
    if user.header then
        file:printf(user.header)
    else
        local kind = path.basename(file:path())
        local builtinvars = {}
        builtinvars.author = string.format("csplink coder: %s(%s)", string.lower(coder.moduledir()),
                                           string.lower(coder.version()))
        builtinvars.file = path.filename(file:path())
        builtinvars.brief = string.format("this file provides code for the %s initialization", string.lower(kind))
        builtinvars.date = os.date("%Y")

        local header = string.gsub(license:trim(), "%${{(.-)}}", function(variable)
            variable = variable:trim()
            local value = builtinvars[variable]
            return type(value) == "function" and value() or value
        end)
        file:print(header)
    end
    file:print(user_code_end_template, "header")
    file:print("")
end

function generate_user(file, kind, user, is_end)
    is_end = is_end or false
    file:print(user_code_begin_template, kind)
    if user[kind] then
        file:printf(user[kind])
    else
        file:print("")
    end
    file:print(user_code_end_template, kind)
    if not is_end then
        file:print("")
    end
end

function generate_includes(file, project, coder, user)
    local kind = path.basename(file:path())
    local header_table = {}
    if path.extension(file:path()) == ".h" then
        table.join2(header_table, coder.get_header("csp.base"))
        table.join2(header_table, coder.get_header(string.lower(kind)))
    else
        table.insert(header_table, string.format("%s.h", kind))
    end
    file:print("/* includes ------------------------------------------------------------------*/")
    for _, h in ipairs(header_table) do
        file:print("#include \"%s\"", h)
    end
    generate_user(file, "includes", user)
end

function generate_typedef(file, project, coder, user)
    file:print("/* typedef -------------------------------------------------------------------*/")
    generate_user(file, "typedef", user)
end

function generate_define(file, project, coder, user)
    file:print("/* define --------------------------------------------------------------------*/")
    generate_user(file, "define", user)
end

function generate_macro(file, project, coder, user)
    file:print("/* macro ---------------------------------------------------------------------*/")
    generate_user(file, "macro", user)
end

function generate_variables(file, project, coder, user)
    if path.extension(file:path()) == ".h" then
        file:print("/* extern variables ----------------------------------------------------------*/")
        generate_user(file, "extern variables", user)
    else
        file:print("/* variables -----------------------------------------------------------------*/")
        generate_user(file, "variables", user)
    end
end

function generate_functions_prototypes(file, project, coder, user)
    file:print("/* functions prototypes ------------------------------------------------------*/")
    if path.extension(file:path()) == ".h" then
        local kind = string.lower(path.basename(file:path()))
        file:print("")
        file:print([[/**
 * @brief configure %s
 *
 */]], kind)
        file:print("extern void csplink_%s_init(void);", kind)
    end
    generate_user(file, "functions prototypes", user)
end

function generate_functions(file, project, coder)
    local kind = path.basename(file:path())
    local code = coder.generate(project_table, kind)
    file:print("void csplink_%s_init(void)", string.lower(kind))
    file:print("{")
    file:print(string.rtrim(code.code))
    file:print("}")
end

function match_user(file_path)
    if not os.isfile(file_path) then
        return {}
    end

    local user = {}
    local data = io.readfile(file_path)
    for s in string.gmatch(data, user_code_end_match .. "(.-) %*/") do
        local matcher = user_code_begin_match .. s .. " %*/\n(.-)" .. user_code_end_match .. s .. " %*/"
        local match = string.match(data, matcher)
        if match and string.len(match) > 0 then
            user[s] = match
        end
    end
    return user
end

function generate_h(project, coder, kind, outputdir)
    local file_path = path.join(outputdir, "core", "inc", string.lower(kind) .. ".h")
    local user = match_user(file_path)
    local file = io.open(file_path, "w")

    generate_header(file, project_table, coder, user)
    generate_includes(file, project_table, coder, user)
    generate_typedef(file, project_table, coder, user)
    generate_define(file, project_table, coder, user)
    generate_macro(file, project_table, coder, user)
    generate_variables(file, project_table, coder, user)
    generate_functions_prototypes(file, project_table, coder, user)
    generate_user(file, "0", user, true)

    file:close()

    cprint("${color.success}create %s ok!", file_path)
end

function generate_c(project, coder, kind, outputdir)
    local file_path = path.join(outputdir, "core", "src", string.lower(kind) .. ".c")
    local user = match_user(file_path)
    local file = io.open(file_path, "w")

    generate_header(file, project_table, coder, user)
    generate_includes(file, project_table, coder, user)
    generate_typedef(file, project_table, coder, user)
    generate_define(file, project_table, coder, user)
    generate_macro(file, project_table, coder, user)
    generate_variables(file, project_table, coder, user)
    generate_functions_prototypes(file, project_table, coder, user)
    generate_user(file, "0", user)
    generate_functions(file, project_table, coder)
    generate_user(file, "1", user, true)

    file:close()

    cprint("${color.success}create %s ok!", file_path)
end

function generate(outputdir)
    local company = project_table.core.company
    local hal = project_table.core.hal
    local name = project_table.core.target
    local modules = project_table.core.modules
    local coder = find_coder(company, hal, name)
    assert(#modules > 0, "modules is empty")
    for _, kind in ipairs(modules) do
        generate_h(project_table, coder, kind, outputdir)
        generate_c(project_table, coder, kind, outputdir)
    end
end

-- LuaFormatter off
local common_options = {
    {"p",   "project",          "kv",   nil,                                        "csp project file path."},
    {"h",   "help",             "k",    nil,                                        "print this help message and exit."},
    {"o",   "outputdir",        "v",    nil,                                        "set the output directory."},
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
        if not results["project"] then
            print("fatal error: no input files")
            usage()
            return
        end

        local outputdir = results["outputdir"] or path.directory(results["project"])
        if results["help"] then
            usage()
        elseif results["project"] then
            assert(os.isfile(results["project"]), "file: %s not found!", results["project"])
            project_table = json.loadfile(results["project"])
            generate(outputdir)
        else
            usage()
        end
    end
end
