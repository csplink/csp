/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ip.ts
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
 *  2025-05-20     xqyjlj       initial version
 */

import type { I18nType } from './i18n'

export interface IpType {
  parameters: {
    [key: string]: IpParameterType | IpParameterConditionType[]
  }
  containers?: IpContainersType
  presets?: {
    [key: string]: IpObjectType | IpObjectConditionType[]
  }
  pins?: {
    [key: string]: {
      [key: string]: {
        [key: string]: {
          default: boolean
        }
      }
    }
  }
  clockTree?: IpClockTreeType
  activated?: string
}

export interface IpParameterType {
  display?: I18nType
  description: I18nType
  readonly?: boolean
  type: 'enum' | 'integer' | 'float' | 'boolean' | 'radio' | 'string'
  values?: {
    [key: string]: IpParameterValueUnitType
  }
  group?: string
  default: string | number | boolean
  expression?: IpExpressionType
  visible?: boolean
  max?: number | string
  min?: number | string
}

export interface IpParameterValueUnitSignalUnitType {
  mode: string
}

export interface IpParameterValueUnitType {
  expression?: IpExpressionType
  comment: I18nType
  signals?: {
    [key: string]: IpParameterValueUnitSignalUnitType
  }
}

export interface IpParameterConditionType {
  condition: string
  content: IpParameterType
}

export interface IpObjectType {
  refParameters?: {
    [key: string]: IpRefParameterType
  }
}

export interface IpRefParameterType {
  values?: string[]
  default?: string
  condition?: string
  readonly?: boolean
}

export interface IpObjectConditionType {
  condition: string
  content: IpObjectType
}

export interface IpContainersType {
  overview?: IpContainerObjectType | IpObjectConditionType[]
  modes?: IpContainerObjectType | IpObjectConditionType[]
  configurations?: IpContainerObjectType | IpObjectConditionType[]
}

export interface IpContainerObjectType extends IpObjectType {
}

export interface IpContainerObjectConditionType {
  condition: string
  content: IpObjectConditionType
}

export interface IpExpressionType {
  display: string
}

export interface IpClockTreeElementUnitType {
  refParameter: string
  type?: 'divisor' | 'multiplexed' | 'multiple'
  enable?: string | boolean
  output?: string[]
  input?: string[]
}

export interface IpClockTreeType {
  elements: {
    [k: string]: IpClockTreeElementUnitType
  }
  i18n?: {
    [k: string]: I18nType
  }
}
