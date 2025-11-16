/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        repository.d.ts
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
 *  2025-08-14     xqyjlj       initial version
 */

export interface RepositoryType {
  chips: {
    [k: string]: RepositoryChipVendorType
  }
  packages: {
    hal: Hal
    toolchains: Hal
    components: {
      system?: Hal
    }
  }
  $packages$?: $Packages$
  [k: string]: unknown
}

export interface RepositoryChipVendorType {
  content: {
    [k: string]: RepositoryChipSeriesType
  }
}

export interface RepositoryChipSeriesType {
  [k: string]: RepositoryChipsLineType
}

export interface RepositoryChipsLineType {
  [k: string]: RepositoryChipUnitType
}

export interface RepositoryChipUnitType {
  core: string
  current: {
    lowest: number
    run: number
  }
  flash: number
  frequency: number
  io: number
  package: string
  peripherals: {
    [k: string]: number
  }
  ram: number
  temperature: {
    max: number
    min: number
  }
  voltage: {
    max: number
    min: number
  }
}

export interface Hal {
  [k: string]: $Packages$
}

export interface $Packages$ {
  version?: {
    [k: string]: {
      urls:
        | string[]
        | {
          windows?: string[]
          linux?: string[]
          [k: string]: unknown
        }
      note: {
        en: string
        [k: string]: unknown
      }
      [k: string]: unknown
    }
  }
  author?: {
    name: string
    email: string
    website: {
      blog?: string
      github?: string
      [k: string]: unknown
    }
    [k: string]: unknown
  }
  license?: string
  vendor?: string
  vendorUrl?: I18nType
  description?: I18nType
  url?: I18nType
  support?: string
}
