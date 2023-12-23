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
-- @file        xmake.lua
--
-- Change Logs:
-- Date           Author       Notes
-- ------------   ----------   -----------------------------------------------
-- 2023-12-19     xqyjlj       initial version
--
local _version = "v0.0.1"

function version()
    return _version
end

function _assert(gpiox, index, x, y)
    assert(x == y, "P%s%s std.gpio_mode_t: %s is invalid, should be %s!", gpiox, index, x, y)
end

function _generate_gpio(gpiox, pins)
    gpiox = string.upper(gpiox)
    local code_table = {}
    table.insert(code_table, string.format("    /* enable the GPIO%s ports clock */", gpiox))
    table.insert(code_table, string.format("    RCM_EnableAPB2PeriphClock(RCM_APB2_PERIPH_GPIO%s);", gpiox))
    table.insert(code_table, "")
    for _, func in ipairs(table.orderkeys(pins)) do
        for _, index in ipairs(table.orderkeys(pins[func])) do
            local pin_id = {}
            local property = pins[func][index]["config"]["function_property"]["gpio"]
            table.insert(pin_id, string.format("GPIO_PIN_%s", index))
            pin_id = table.concat(pin_id, " | ")
            table.insert(code_table, string.format("    /* configure the GPIO%s, %s */", gpiox, pin_id))
            if func == "gpio-output" then -- first should add pin level
                -- level
                local pin_level
                if property["std.gpio_level_t"] == "std.gpio_level_low" then
                    pin_level = "BIT_RESET"
                elseif property["std.gpio_level_t"] == "std.gpio_level_high" then
                    pin_level = "BIT_SET"
                else
                    assert(0, "P%s%s std.gpio_output_type_t: %s is invalid!", gpiox, index,
                           property["std.gpio_output_type_t"])
                end
                table.insert(code_table,
                             string.format("    GPIO_WriteBitValue(GPIO%s, %s, %s);", gpiox, pin_id, pin_level))
                table.insert(code_table, "")
            end
            table.insert(code_table, string.format("    config.pin = %s;", pin_id))
            if func == "gpio-analog" then -- analog
                _assert(gpiox, index, property["std.gpio_mode_t"], "std.gpio_mode_analog")
                table.insert(code_table, "    config.mode = GPIO_MODE_ANALOG;")
            elseif func == "gpio-input" then -- input
                _assert(gpiox, index, property["std.gpio_mode_t"], "std.gpio_mode_input")
                -- pull
                if property["std.gpio_pull_t"] == "std.gpio_pull_up" then
                    table.insert(code_table, "    config.mode = GPIO_MODE_IN_PU;")
                elseif property["std.gpio_pull_t"] == "std.gpio_pull_down" then
                    table.insert(code_table, "    config.mode = GPIO_MODE_IN_PD;")
                elseif property["std.gpio_pull_t"] == "std.gpio_pull_no" then
                    table.insert(code_table, "    config.mode = GPIO_MODE_IN_FLOATING;")
                else
                    assert(0, "P%s%s std.gpio_pull_t: %s is invalid!", gpiox, index, property["std.gpio_pull_t"])
                end
            elseif func == "gpio-output" then -- output
                _assert(gpiox, index, property["std.gpio_mode_t"], "std.gpio_mode_output")
                -- output_type
                if property["std.gpio_output_type_t"] == "std.gpio_output_pp" then
                    table.insert(code_table, "    config.mode = GPIO_MODE_OUT_PP;")
                elseif property["std.gpio_output_type_t"] == "std.gpio_output_od" then
                    table.insert(code_table, "    config.mode = GPIO_MODE_OUT_OD;")
                else
                    assert(0, "P%s%s std.gpio_output_type_t: %s is invalid!", gpiox, index,
                           property["std.gpio_output_type_t"])
                end
                -- speed
                if property["std.gpio_speed_t"] == "std.gpio_speed_low" then
                    table.insert(code_table, "    config.speed = GPIO_SPEED_10MHz;")
                elseif property["std.gpio_speed_t"] == "std.gpio_speed_medium" then
                    table.insert(code_table, "    config.speed = GPIO_SPEED_2MHz;") -- why 2MHz?
                elseif property["std.gpio_speed_t"] == "std.gpio_speed_high" then
                    table.insert(code_table, "    config.speed = GPIO_SPEED_50MHz;")
                else
                    assert(0, "P%s%s std.gpio_speed_t: %s is invalid!", gpiox, index, property["std.gpio_speed_t"])
                end
            else
                assert(0, "P%s%s function: %s is invalid!", gpiox, index, func)
            end
            table.insert(code_table, string.format("    GPIO_Config(GPIO%s, &config);", gpiox))
            table.insert(code_table, "")
        end
    end
    return table.concat(code_table, "\n")
end

function generate_gpio(project)
    local group = {}
    for name, pin in pairs(project.pin_configs) do
        name = string.lower(name)
        func = string.lower(pin["function"])
        if pin.locked and string.startswith(func, "gpio-") then
            if string.match(name, "^p%l%d+$") then
                local gpiox, index = string.match(name, "^p(%l)(%d+)$")
                if gpiox and index then
                    if not group[gpiox] then
                        group[gpiox] = {}
                    end
                    if not group[gpiox][func] then
                        group[gpiox][func] = {}
                    end
                    group[gpiox][func][index] = {name = name, gpiox = gpiox, index = index, config = pin}
                end
            end
        end
    end

    local code_table = {}
    table.insert(code_table, "    GPIO_Config_T config = {0};")
    table.insert(code_table, "")
    for _, gpiox in ipairs(table.orderkeys(group)) do
        local code = _generate_gpio(gpiox, group[gpiox])
        table.insert(code_table, code)
    end

    return table.concat(code_table, "\n")
end

function generate_gpio_module(project)
end

function generate(project, kind)
    if string.lower(kind) == "gpio" then
        modules = generate_gpio_module(project)
        return {code = generate_gpio(project), modules = modules}
    end
end

function get_header(kind)
    kind = string.lower(kind)
    if kind == "csp.base" then
        return {"apm32f10x.h"}
    elseif kind == "gpio" then
        return {"apm32f10x_gpio.h", "apm32f10x_eint.h", "apm32f10x_misc.h", "apm32f10x_rcm.h"}
    else
        return {}
    end
end
