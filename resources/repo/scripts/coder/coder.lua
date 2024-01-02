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
import("find_coder")
import("project", {alias = "generate_project"})

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

function _generate_header(file, proj, coder, user)
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
        if kind == "main" then
            builtinvars.brief = "main program body"
        else
            builtinvars.brief = string.format("this file provides code for the %s initialization", string.lower(kind))
        end
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

function _generate_user(file, kind, user, is_end)
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

function _generate_includes(file, proj, coder, user)
    local kind = path.basename(file:path())
    local header_table = {}
    if path.extension(file:path()) == ".h" then
        table.join2(header_table, coder.get_header("base"))
        table.join2(header_table, coder.get_header(string.lower(kind)))
    else
        if "main" == kind then
            table.insert(header_table, string.format("%s.h", kind))
            local modules = proj.core.modules
            for _, m in ipairs(modules) do
                table.insert(header_table, string.format("csplink/%s.h", string.lower(m)))
            end
        else
            table.insert(header_table, string.format("csplink/%s.h", kind))
        end
    end
    file:print("/* includes ------------------------------------------------------------------*/")
    for _, h in ipairs(header_table) do
        file:print("#include \"%s\"", h)
    end
    _generate_user(file, "includes", user)
end

function _generate_typedef(file, proj, coder, user)
    file:print("/* typedef -------------------------------------------------------------------*/")
    _generate_user(file, "typedef", user)
end

function _generate_define(file, proj, coder, user)
    file:print("/* define --------------------------------------------------------------------*/")
    if path.extension(file:path()) == ".h" then
        local kind = path.basename(file:path())
        local data = coder.generate(proj, kind)
        if data then
            for _, map in ipairs(data.defines or {}) do
                file:print("#define %s %s", map.key, map.value)
            end
        end
    end
    _generate_user(file, "define", user)
end

function _generate_macro(file, proj, coder, user)
    file:print("/* macro ---------------------------------------------------------------------*/")
    _generate_user(file, "macro", user)
end

function _generate_variables(file, proj, coder, user)
    if path.extension(file:path()) == ".h" then
        file:print("/* extern variables ----------------------------------------------------------*/")
        _generate_user(file, "extern variables", user)
    else
        file:print("/* variables -----------------------------------------------------------------*/")
        _generate_user(file, "variables", user)
    end
end

function _generate_functions_prototypes(file, proj, coder, user)
    file:print("/* functions prototypes ------------------------------------------------------*/")
    if path.extension(file:path()) == ".h" then
        local kind = string.lower(path.basename(file:path()))
        if "main" ~= kind then
            file:print("")
            file:print([[/**
 * @brief configure %s
 */]], kind)
            file:print("void csplink_%s_init(void);", kind)
        end
    end
    _generate_user(file, "functions prototypes", user)
end

function _generate_functions(file, proj, coder, user)
    local kind = path.basename(file:path())
    local data = coder.generate(proj, kind)
    if "main" == kind then
        file:print([[/**
 * @brief the application entry point.
 * @retval int
 */]])
        file:print("int main(void)")
        file:print("{")
        if data.code then
            file:print(string.rtrim(data.code))
        end
        local modules = proj.core.modules
        for _, m in ipairs(modules) do
            file:print("    csplink_%s_init();", string.lower(m))
        end

        file:print("    /* infinite loop */")
        file:print("    " .. user_code_begin_template, "while.0")
        if user["while.0"] then
            file:printf(user["while.0"])
        else
            file:print("    while (1)")
            file:print("    {")
        end
        file:print("        " .. user_code_end_template, "while.0")

        -- TODO: main fn

        file:print("        " .. user_code_begin_template, "while.1")
        if user["while.1"] then
            file:printf(user["while.1"])
        else
            file:print("    }")
        end
        file:print("    " .. user_code_end_template, "while.1")
        file:print("}")
    else
        file:print("void csplink_%s_init(void)", string.lower(kind))
        file:print("{")
        if data and data.code then
            file:print(string.rtrim(data.code))
        end
        file:print("}")
    end
end

function _match_user(file_path)
    if not os.isfile(file_path) then
        return {}
    end

    local user = {}
    local data = io.readfile(file_path)
    for s in string.gmatch(data, user_code_end_match .. "(.-) %*/") do
        local matcher = user_code_begin_match .. s .. " %*/\n(.-)" .. user_code_end_match .. s .. " %*/"
        local match = string.match(data, matcher)
        if match and string.len(match) > 0 then
            match = string.rtrim(match, " ") -- we must ignore right whitespace
            if string.len(match) > 0 then
                user[s] = match
            end
        end
    end
    return user
end

function _generate_h(proj, coder, kind, outputdir)
    local file_path
    if "main" == kind then
        file_path = path.join(outputdir, "core", "inc", string.lower(kind) .. ".h")
    else
        file_path = path.join(outputdir, "core", "inc", "csplink", string.lower(kind) .. ".h")
    end
    local user = _match_user(file_path)
    local file = io.open(file_path, "w")

    _generate_header(file, proj, coder, user)
    _generate_includes(file, proj, coder, user)
    _generate_typedef(file, proj, coder, user)
    _generate_define(file, proj, coder, user)
    _generate_macro(file, proj, coder, user)
    _generate_variables(file, proj, coder, user)
    _generate_functions_prototypes(file, proj, coder, user)
    _generate_user(file, "0", user, true)

    file:close()

    cprint("${color.success}create %s ok!", file_path)
end

function _generate_c(proj, coder, kind, outputdir)
    local file_path = path.join(outputdir, "core", "src", string.lower(kind) .. ".c")
    local user = _match_user(file_path)
    local file = io.open(file_path, "w")

    _generate_header(file, proj, coder, user)
    _generate_includes(file, proj, coder, user)
    _generate_typedef(file, proj, coder, user)
    _generate_define(file, proj, coder, user)
    _generate_macro(file, proj, coder, user)
    _generate_variables(file, proj, coder, user)
    _generate_functions_prototypes(file, proj, coder, user)
    _generate_user(file, "0", user)
    _generate_functions(file, proj, coder, user)
    _generate_user(file, "1", user, true)

    file:close()

    cprint("${color.success}create %s ok!", file_path)
end

function _generate(proj, outputdir, repositories_dir)
    local company = proj.core.company
    local hal = proj.core.hal
    local name = proj.core.target
    local modules = proj.core.modules
    local coder = find_coder(company, hal, name, repositories_dir)
    assert(#modules > 0, "modules is empty")
    modules = table.unique(modules)
    for _, kind in ipairs(modules) do
        _generate_h(proj, coder, kind, outputdir)
        _generate_c(proj, coder, kind, outputdir)
    end
    _generate_h(proj, coder, "main", outputdir)
    _generate_c(proj, coder, "main", outputdir)
    coder.deploy(proj, outputdir)
    generate_project(proj, coder, outputdir)
end

-- LuaFormatter off
local common_options = {
    {"p",   "project",          "kv",   nil,                                        "csp project file path."},
    {"h",   "help",             "k",    nil,                                        "print this help message and exit."},
    {"o",   "outputdir",        "v",    nil,                                        "set the output directory."},
    {"r",   "repositories",     "kv",   nil,                                        "repositories dir."},
}
-- LuaFormatter on

function _usage()
    option.show_logo()
    option.show_options(common_options)
end

function main(...)
    local argv = table.pack(...)
    local results, errors = option.raw_parse(argv, common_options)
    if results then
        if not results["project"] then
            print("fatal error: no input files")
            _usage()
            return
        end

        local outputdir = results["outputdir"] or path.directory(results["project"])
        local repositories_dir = results["repositories"] or path.join(os.scriptdir(), "..", "..", "..", "repositories")
        if results["help"] then
            _usage()
        elseif results["project"] then
            assert(os.isfile(results["project"]), "file: %s not found!", results["project"])
            local proj = json.loadfile(results["project"])
            _generate(proj, outputdir, repositories_dir)
        else
            _usage()
        end
    end
end
