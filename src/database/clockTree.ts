/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        clockTree.ts
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
 *  2025-05-15     xqyjlj       initial version
 */

import type {
  ClockTreeEdgeType,
  ClockTreeEdgeTypeType,
  ClockTreeNodeType,
  ClockTreeNodeTypeType,
  ClockTreeNodeUnitType,
  ClockTreeType,
} from '@/electron/types'
import type { XYPosition } from '@vue-flow/core'
import type { App } from 'vue'
import type { Ip, IpManager, IpParameter } from './ip'
import { computed, inject, markRaw } from 'vue'

// #region typedef

export class ClockTree {
  private _nodes: Record<string, ClockTreeNode> = {}
  private _edges: Record<string, ClockTreeEdge> = {}

  constructor(
    private _origin: ClockTreeType,
    public ip: Ip,
  ) {
    for (const [name, node] of Object.entries(this._origin.nodes)) {
      this._nodes[name] = new ClockTreeNode(node, name, this)
    }

    for (const [name, edge] of Object.entries(this._origin.edges)) {
      this._edges[name] = new ClockTreeEdge(edge)
    }
  }

  get origin(): ClockTreeType {
    return this._origin
  }

  get instance(): string {
    return this._origin.instance
  }

  get nodes(): Record<string, ClockTreeNode> {
    return this._nodes
  }

  get edges(): Record<string, ClockTreeEdge> {
    return this._edges
  }

  updateEdges(edges: Record<string, ClockTreeEdgeType>) {
    this._edges = {}
    this._origin.edges = edges
    for (const [name, edge] of Object.entries(this._origin.edges)) {
      this._edges[name] = new ClockTreeEdge(edge)
    }
  }
}

export class ClockTreeEdge {
  constructor(
    private _origin: ClockTreeEdgeType,
  ) {
  }

  get origin(): ClockTreeEdgeType {
    return this._origin
  }

  get type(): ClockTreeEdgeTypeType {
    return this._origin.type
  }

  get source(): string {
    return this._origin.source
  }

  get target(): string {
    return this._origin.target
  }

  get sourceHandle(): string | undefined | null {
    return this._origin.sourceHandle
  }

  get targetHandle(): string | undefined | null {
    return this._origin.targetHandle
  }

  get label(): string | undefined {
    return this._origin.label
  }
}

export class ClockTreeNode {
  constructor(
    private _origin: ClockTreeNodeType,
    private _name: string,
    private _parent: ClockTree,
  ) {
  }

  get origin(): ClockTreeNodeType {
    return this._origin
  }

  get ip(): Ip {
    return this._parent.ip
  }

  get ref(): string {
    return this._name
  }

  parameter = computed((): IpParameter => {
    const paramName = this._name
    const parameter = this.ip.containers.clockTree.refParameters.value[paramName]?.parameter
    if (!parameter) {
      console.error(`Parameter '${paramName}' not found in IP '${this.ip.instance}'.`)
    }
    return parameter.value
  })

  enabled = computed((): boolean => this.parameter.value.enabled.value)

  get type(): ClockTreeNodeTypeType {
    return this._origin.type
  }

  get position(): XYPosition {
    return this._origin.position ?? { x: 0, y: 0 }
  }

  get unit(): ClockTreeNodeUnitType | undefined {
    return this._origin.unit
  }
}

// #endregion

export class ClockTreeManager {
  private _map: Record<string, Record<string, { clockTree: ClockTree, define: string }>> = markRaw({})
  private _ipManager?: IpManager

  constructor() {
  }

  setIpManager(ipManager: IpManager) {
    this._ipManager = markRaw(ipManager)
  }

  async load(vendor: string, name: string, define: string) {
    const content = await window.electron.invoke('database:getClockTree', vendor, define) as ClockTreeType
    if (content) {
      const clockTree = new ClockTree(content, this._ipManager!.getPeripheral(vendor, content.instance)!);
      (this._map[vendor] ??= {})[name] = markRaw({ clockTree, define })
    }
  }

  save(vendor: string, name: string, clockTree?: ClockTree) {
    if (this._map[vendor]?.[name]) {
      const define = this._map[vendor][name].define
      clockTree ??= this._map[vendor][name].clockTree
      window.electron.send('database:setClockTree', vendor, define, clockTree.origin)
    }
  }

  get(vendor: string, name: string): ClockTree | null {
    if (this._map[vendor]?.[name]) {
      return this._map[vendor][name].clockTree
    }

    return null
  }
}

export function createClockTreeManagerPlugin() {
  const manager = new ClockTreeManager()

  return {
    manager,
    plugin: {
      install(app: App) {
        app.provide('database@clockTreeManager', manager)
      },
    },
    setIpManager(ipManager: IpManager) {
      manager.setIpManager(ipManager)
    },
  }
}

export function useClockTreeManager(): ClockTreeManager {
  return inject('database@clockTreeManager')!
}
