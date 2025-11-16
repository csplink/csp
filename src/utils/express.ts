/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        express.ts
 *  @brief
 *
 * ****************************************************************************
 *  @attention
 *  Licensed under the Apache License v. 2 (the "License");
 *  You may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      https://www.apache.org/licenses/LICENSE-2.0.html
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *  Copyright (C) 2025-2025 xqyjlj<xqyjlj@126.com>
 *
 * ****************************************************************************
 *  Change Logs:
 *  Date           Author       Notes
 *  ------------   ----------   -----------------------------------------------
 *  2025-06-06     xqyjlj       initial version
 */

import type { Expression } from 'expr-eval'
import { Parser } from 'expr-eval'

export class Express {
  private parser = new Parser({
    operators: {
      assignment: false,
    },
  })

  private cache: Record<string, Expression> = {}

  constructor() {
    this.parser.functions.is_empty = Express.isEmpty
  }

  /**
   * 计算表达式的值。
   *
   * @param expression 表达式字符串（https://github.com/silentmatt/expr-eval）
   * @param context 上下文对象，包含变量的值
   * @returns 表达式的计算结果
   */
  evaluateExpression<T>(expression: string, context: Record<string, any>, defaultValue: T | null = null): T | null {
    try {
      let exp: Expression = this.cache[expression]
      if (!exp) {
        exp = this.parser.parse(expression)
        this.cache[expression] = exp
      }
      exp = this.parser.parse(expression)
      const value = exp.evaluate(context)
      return value
    }
    catch (error) {
      if (error instanceof TypeError
        && error.message.includes('Cannot read properties of undefined')) {
        return defaultValue /*! < 如果是访问未定义属性导致的错误，返回默认值 */
      }
      else if (error instanceof Error && error.message.includes('undefined variable')) {
        return defaultValue /*! < 如果是访问未定义属性导致的错误，返回默认值 */
      }
      console.error(`Expression: "(${expression})" evaluate error:`, error)
      return defaultValue
    }
  }

  /**
   * 提取表达式中的所有变量名称（支持点分隔的成员访问链）。
   * 比如：a、b.c、foo.bar.baz
   *
   * @param expression 表达式字符串（https://github.com/silentmatt/expr-eval）
   * @returns 排序后的唯一变量名列表
   */
  evaluateExtract(expression: string): string[] {
    try {
      const exp = Parser.parse(expression)
      const functions = Object.keys(this.parser.functions)
      let variables = exp.variables({ withMembers: true })
      variables = variables.filter(v => !functions.includes(v))
      return variables
    }
    catch (error) {
      console.error(`Expression: "(${expression})" evaluate extract:`, error)
      return []
    }
  }

  /**
   * Escape special characters in a string for use in a regular expression.
   * @param str The string to escape.
   * @returns The escaped string.
   */
  static escapeRegExp(str: string): string {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  }

  static isEmpty(object: any): boolean {
    if (
      (object === null)
      || (typeof object === 'string' && object.length === 0)
      || (Array.isArray(object) && object.length === 0)
      || (typeof object === 'object' && Object.keys(object).length === 0)
    ) {
      return true
    }
    return false
  }
}
