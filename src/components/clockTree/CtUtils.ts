/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        CtUtils.ts
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
 *  2025-10-08     xqyjlj       initial version
 */

import type { Connection, GraphEdge, GraphNode } from '@vue-flow/core'

export function isValidTargetConnection(connection: Connection, _elements: {
  edges: GraphEdge[]
  nodes: GraphNode[]
  sourceNode: GraphNode
  targetNode: GraphNode
}): boolean {
  return connection.sourceHandle?.startsWith('source') ?? false
}

export function isValidSourceConnection(connection: Connection, _elements: {
  edges: GraphEdge[]
  nodes: GraphNode[]
  sourceNode: GraphNode
  targetNode: GraphNode
}): boolean {
  return connection.targetHandle?.startsWith('target') ?? false
}

export function alignLeft(selectedNodes: GraphNode<any, any, string>[]) {
  if (selectedNodes.length < 2)
    return

  const minX = Math.min(...selectedNodes.map(n => n.position.x))
  selectedNodes.forEach((node) => {
    node.position.x = minX
  })
}

export function alignRight(selectedNodes: GraphNode<any, any, string>[]) {
  if (selectedNodes.length < 2)
    return

  const maxRight = Math.max(...selectedNodes.map((node) => {
    return node.position.x + node.dimensions.width
  }))

  selectedNodes.forEach((node) => {
    node.position.x = maxRight - node.dimensions.width
  })
}

export function alignTop(selectedNodes: GraphNode<any, any, string>[]) {
  if (selectedNodes.length < 2)
    return

  const minY = Math.min(...selectedNodes.map(node => node.position.y))
  selectedNodes.forEach((node) => {
    node.position.y = minY
  })
}

export function alignBottom(selectedNodes: GraphNode<any, any, string>[]) {
  if (selectedNodes.length < 2)
    return

  const maxBottom = Math.max(...selectedNodes.map((node) => {
    return node.position.y + node.dimensions.height
  }))

  selectedNodes.forEach((node) => {
    node.position.y = maxBottom - node.dimensions.height
  })
}

export function alignHorizontalCenter(selectedNodes: GraphNode<any, any, string>[]) {
  if (selectedNodes.length < 2)
    return

  const centerX = selectedNodes.reduce((sum, node) => {
    return sum + node.position.x + node.dimensions.width / 2
  }, 0) / selectedNodes.length

  selectedNodes.forEach((node) => {
    node.position.x = centerX - node.dimensions.width / 2
  })
}

export function alignVerticalCenter(selectedNodes: GraphNode<any, any, string>[]) {
  if (selectedNodes.length < 2)
    return

  const centerY = selectedNodes.reduce((sum, node) => {
    return sum + node.position.y + node.dimensions.height / 2
  }, 0) / selectedNodes.length

  selectedNodes.forEach((node) => {
    node.position.y = centerY - node.dimensions.height / 2
  })
}

export function distributeHorizontally(selectedNodes: GraphNode<any, any, string>[]) {
  if (selectedNodes.length < 3)
    return

  /* !< 按x坐标排序 */
  const sorted = [...selectedNodes].sort((a, b) => a.position.x - b.position.x)

  /* !< 计算最左和最右节点的中心点 */
  const leftWidth = sorted[0].dimensions.width
  const leftCenter = sorted[0].position.x + leftWidth / 2

  const rightWidth = sorted[sorted.length - 1].dimensions.width
  const rightCenter = sorted[sorted.length - 1].position.x + rightWidth / 2

  /* !< 计算间距 */
  const totalDistance = rightCenter - leftCenter
  const spacing = totalDistance / (sorted.length - 1)

  /* !< 更新中间节点的位置 */
  for (let i = 1; i < sorted.length - 1; i++) {
    const width = sorted[i].dimensions.width
    const newCenterX = leftCenter + spacing * i
    sorted[i].position.x = newCenterX - width / 2
  }
}

export function distributeVertically(selectedNodes: GraphNode<any, any, string>[]) {
  if (selectedNodes.length < 3)
    return

  /* !< 按y坐标排序 */
  const sorted = [...selectedNodes].sort((a, b) => a.position.y - b.position.y)

  /* !< 计算最上和最下节点的中心点 */
  const topHeight = sorted[0].dimensions.height
  const topCenter = sorted[0].position.y + topHeight / 2

  const bottomHeight = sorted[sorted.length - 1].dimensions.height
  const bottomCenter = sorted[sorted.length - 1].position.y + bottomHeight / 2

  /* !< 计算间距 */
  const totalDistance = bottomCenter - topCenter
  const spacing = totalDistance / (sorted.length - 1)

  /* !< 更新中间节点的位置 */
  for (let i = 1; i < sorted.length - 1; i++) {
    const height = sorted[i].dimensions.height
    const newCenterY = topCenter + spacing * i
    sorted[i].position.y = newCenterY - height / 2
  }
}

function findSourceEdgesRecursively(
  nodes: GraphNode[],
  edges: GraphEdge[],
  nodeId: string,
  visited = new Set<string>(),
): Set<string> {
  const edgeIds = new Set<string>()

  if (visited.has(nodeId)) {
    return edgeIds
  }
  visited.add(nodeId)

  const targetNode = nodes.find(n => n.id === nodeId)

  for (const edge of edges) {
    if (edge.target === nodeId) {
      /* !< 对于 ct-radio 类型的节点，只追踪被选中的 target handle */
      if (targetNode?.type === 'ct-radio') {
        const selectedValue = targetNode.data?.selectedValue
        const expectedTargetHandle = `target-${selectedValue}`

        if (edge.targetHandle !== expectedTargetHandle) {
          continue
        }
      }

      edgeIds.add(edge.id)
      const sourceEdges = findSourceEdgesRecursively(nodes, edges, edge.source, visited)
      sourceEdges.forEach(id => edgeIds.add(id))
    }
  }

  return edgeIds
}

export function updateEdgesAnimation(
  selectedNodes: GraphNode<any, any, string>[],
  nodes: GraphNode[],
  edges: GraphEdge[],
) {
  const edgesToAnimate = new Set<string>()

  for (const node of selectedNodes) {
    const sourceEdges = findSourceEdgesRecursively(nodes, edges, node.id)
    sourceEdges.forEach(id => edgesToAnimate.add(id))
  }

  for (const edge of edges) {
    const shouldAnimate = edgesToAnimate.has(edge.id)
    if (edge.animated !== shouldAnimate) {
      edge.animated = shouldAnimate
      edge.zIndex = shouldAnimate ? 99999 : 0
    }
  }
}
