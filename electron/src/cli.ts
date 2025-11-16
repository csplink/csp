/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        cli.ts
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
 *  2025-05-05     xqyjlj       initial version
 */

import fs from 'node:fs'
import path from 'node:path'
import { Command } from 'commander'
import pkg from '../../package.json'
import { checkProjectByPath, processArgs } from '../utils'

export { processArgs as args } from '../utils'

const VITE_DEV_SERVER_URL = process.env.VITE_DEV_SERVER_URL

let electronArgs: string[] = []
if (VITE_DEV_SERVER_URL) {
  const sepIndex = process.argv.indexOf('--')
  if (sepIndex !== -1) {
    electronArgs = process.argv.slice(sepIndex + 1)
  }
}
else {
  electronArgs = process.argv.slice(1)
}

const argv = ['node', 'csp', ...electronArgs]

const cli = new Command()

cli.name('csp')
  .description('CSP (Chip Support Package) - A powerful tool for chip configuration and code generation')
  .version(pkg.version, '-v, --version', 'Display version number')

cli.argument('[file]', 'CSP project file')
  .option('-b, --backend-url <url>', 'Backend URL (default: http://127.0.0.1:55432)')
  .action((file, options) => {
    if (options.backendUrl) {
      processArgs.backendUrl = options.backendUrl
    }

    if (file) {
      let absolutePath = path.resolve(file)
      absolutePath = absolutePath.replace(/\\/g, '/')
      if (!fs.existsSync(absolutePath)) {
        console.error(`The file ${absolutePath} does not exist.`)
        return
      }
      processArgs.projectPath = absolutePath

      if (checkProjectByPath(absolutePath)) {
        processArgs.runMode = 'main'
      }
    }
  })

cli.parse(argv)
