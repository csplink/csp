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
import type { App } from 'vue'
import { inject } from 'vue'
import * as xpath from 'xpath'

// #region typedef

export class ClockTree {
  private _svg: string
  private _widgets: Record<string, GeometryType> = {}

  constructor(svg: string, widgets: Record<string, GeometryType>) {
    this._svg = svg
    this._widgets = widgets
  }

  get svg(): string {
    return this._svg
  }

  get widgets(): Record<string, GeometryType> {
    return this._widgets
  }
}

class MxCell {
  private _origin: Element
  private _id: string
  private _value: string
  private _parent: number
  private _vertex: number
  private _edge: number
  private _shape: string[] = []
  private _style: Record<string, string> = {}

  constructor(element: Element) {
    this._origin = element
    this._id = element.getAttribute('id') ?? 'unknown'
    this._value = element.getAttribute('value') ?? ''
    this._parent = Number.parseInt(element.getAttribute('parent') ?? '0', 10)
    this._vertex = Number.parseInt(element.getAttribute('vertex') ?? '0', 10)
    this._edge = Number.parseInt(element.getAttribute('edge') ?? '0', 10)

    const styleStr = element.getAttribute('style') ?? ''
    const styles = styleStr.trim().replace(/;+$/, '').split(';')

    for (const style of styles) {
      if (style.includes('=')) {
        const [key, value] = style.split('=')
        if (key === 'shape') {
          this._shape.push(value)
        }
        this._style[key] = value
      }
      else if (style) {
        this._shape.push(style)
      }
    }
  }

  get origin(): Element {
    return this._origin
  }

  get id(): string {
    return this._id
  }

  get value(): string {
    return this._value
  }

  get shape(): string[] {
    return this._shape
  }

  get style(): Record<string, string> {
    return this._style
  }

  get parent(): number {
    return this._parent
  }

  get vertex(): number {
    return this._vertex
  }

  get edge(): number {
    return this._edge
  }
}

interface GeometryType {
  x: number
  y: number
  width: number
  height: number
}

// #endregion

export class ClockTreeManager {
  private _map: Record<string, Record<string, ClockTree>> = {}

  constructor() {
  }

  /**
   * 判断给定的单元格是否为“widget”，
   * 备注：widget 本质上也是一种特殊的 graphics
   * 判定标准：
   * - 背景填充为透明（'none' 或 'default'）
   * - edge 属性为 0
   * - 没有文本内容
   * - 形状为无圆角的矩形或椭圆
   * - 边框宽度为 1
   *
   * @param cell 要判断的单元格
   * @returns 是否为组件
   */
  private isWidget(cell: MxCell): boolean {
    const fillColor = cell.style.fillColor ?? 'none'

    if (cell.value !== '' || cell.shape.includes('text')) {
      return false
    }
    else if (cell.edge === 1) {
      return false
    }
    else if (fillColor === 'none' || fillColor === 'default') {
      const strokeWidth = Number.parseInt(cell.style.strokeWidth ?? '1', 10)
      if (strokeWidth !== 1) {
        return false
      }
      else if (cell.style.rounded === '0' || cell.shape.includes('ellipse')) {
        return true
      }
    }

    return false
  }

  /**
   * 判断给定的单元格是否为图形（graphics）。
   * 判定标准：
   * - 有圆角设置（rounded 不为空即可）
   * - 或形状为梯形（trapezoid）
   *
   * @param cell 要判断的单元格
   * @returns 是否为图形
   */
  private isGraphics(cell: MxCell): boolean {
    if (cell.style.rounded || cell.shape.includes('trapezoid')) {
      return true
    }

    return false
  }

  /**
   * 判断给定的单元格是否为线条（line）。
   * 判定标准：
   * - 形状为 'line'
   * - 或 edge 属性为 1 且边框颜色为 'none' 或 'default'
   *
   * @param cell 要判断的单元格
   * @returns 是否为线条
   */
  private isLine(cell: MxCell): boolean {
    const strokeColor = cell.style.strokeColor ?? 'none'
    if (cell.shape.includes('line')
      || (cell.edge === 1 && (strokeColor === 'none' || strokeColor === 'default'))
    ) {
      return true
    }

    return false
  }

  /**
   * 判断给定的单元格是否为文本（text）。
   * 判定标准：
   * - 有文本内容或形状为 text
   * - 背景为透明（'none' 或 'default'）
   *
   * @param cell 要判断的单元格
   * @returns 是否为文本
   */
  private isText(cell: MxCell): boolean {
    const fillColor = cell.style.fillColor ?? 'none'
    if ((cell.value !== '' || cell.shape.includes('text'))
      && (fillColor === 'none' || fillColor === 'default')) {
      return true
    }

    return false
  }

  /**
   * 递归更新线条类元素（如 path 和 ellipse）的颜色。
   * - 对于 <path> 元素，更新 stroke 和（如果 fill 非 'none'）的 fill 颜色。
   * - 对于 <ellipse> 元素，同时更新 fill 和 stroke。
   *
   * @param element 当前处理的 SVG/DOM 元素
   * @param color 要设置的颜色值（如 "#ff0000"）
   */
  //   private updateLineElement(element: Element, color: string): void {
  //     const children = Array.from(element.childNodes).filter(node => node.nodeType === 1) as Element[]

  //     for (const e of children) {
  //       switch (e.tagName) {
  //         case 'path':
  //         {
  //           e.setAttribute('stroke', color)
  //           if (e.getAttribute('fill') !== 'none') {
  //             e.setAttribute('fill', color)
  //           }
  //           break
  //         }
  //         case 'ellipse':
  //         {
  //           e.setAttribute('fill', color)
  //           e.setAttribute('stroke', color)
  //           break
  //         }
  //       }

  //       if (e.childNodes.length > 0) {
  //         this.updateLineElement(e, color)
  //       }
  //     }
  //   }

  /**
   * 递归更新文本类元素的颜色。
   * - 仅处理带有 fill 属性的 <g> 元素，并更新其 fill 颜色。
   *
   * @param element 当前处理的 SVG/DOM 元素
   * @param color 要设置的颜色值
   */
  //   private updateTextElement(element: Element, color: string): void {
  //     const children = Array.from(element.childNodes).filter(node => node.nodeType === 1) as Element[]

  //     for (const e of children) {
  //       if (e.tagName === 'g' && e.hasAttribute('fill')) {
  //         e.setAttribute('fill', color)
  //       }

  //       if (e.childNodes.length > 0) {
  //         this.updateTextElement(e, color)
  //       }
  //     }
  //   }

  /**
   * 递归更新图形类元素的颜色。
   * - 对于 <rect> <path> 和 <ellipse>，如果存在 stroke 属性则更新 stroke 颜色。
   * - 对于 <g> 元素，如果存在 fill 属性则更新 fill 颜色。
   *
   * @param element 当前处理的 SVG/DOM 元素
   * @param color 要设置的颜色值
   */
  private updateGraphicsElement(element: Element, color: string): void {
    const children = Array.from(element.childNodes).filter(node => node.nodeType === 1) as Element[]

    for (const e of children) {
      switch (e.tagName) {
        case 'rect':
        case 'ellipse':
        case 'path':
        {
          if (e.hasAttribute('stroke')) {
            e.setAttribute('stroke', color)
          }
          break
        }
        case 'g':
        {
          if (e.hasAttribute('fill')) {
            e.setAttribute('fill', color)
          }
          break
        }
      }

      if (e.childNodes.length > 0) {
        this.updateGraphicsElement(e, color)
      }
    }
  }

  /**
   * 批量更新线条类元素的颜色。
   * - 根据每个 ID 查找对应 SVG 元素，并递归修改其颜色。
   * - 如果找不到某个 ID 的元素，则输出错误并终止处理。
   *
   * @param root SVG 根节点
   * @param lines 包含线条单元格 ID 的数组
   * @param color 要设置的颜色值
   * @param select XPath 查询函数
   */
  //   private updateLines(root: HTMLElement, lines: string[], color: string, select: xpath.XPathSelect) {
  //     for (const id of lines) {
  //       const element = this.findSvgElement(root, id, select)
  //       if (!element) {
  //         console.error(`The '${id}' id is not found`)
  //         break
  //       }
  //       this.updateLineElement(element, color)
  //     }
  //   }

  /**
   * 批量更新文本类元素的颜色。
   * - 根据每个 ID 查找对应 SVG 元素，并递归修改其 fill 属性。
   * - 如果找不到某个 ID 的元素，则输出错误并终止处理。
   *
   * @param root SVG 根节点
   * @param texts 包含文本单元格 ID 的数组
   * @param color 要设置的颜色值
   * @param select XPath 查询函数
   */
  //   private updateTexts(root: HTMLElement, texts: string[], color: string, select: xpath.XPathSelect) {
  //     for (const id of texts) {
  //       const element = this.findSvgElement(root, id, select)
  //       if (!element) {
  //         console.error(`The '${id}' id is not found`)
  //         break
  //       }
  //       this.updateTextElement(element, color)
  //     }
  //   }

  /**
   * 批量更新图形类元素的颜色。
   * - 根据每个 ID 查找对应 SVG 元素，并递归修改 stroke 或 fill 属性。
   * - 如果找不到某个 ID 的元素，则输出错误并终止处理。
   *
   * @param root SVG 根节点
   * @param graphics 包含图形单元格 ID 的数组
   * @param color 要设置的颜色值
   * @param select XPath 查询函数
   */
  //   private updateGraphics(root: HTMLElement, graphics: string[], color: string, select: xpath.XPathSelect) {
  //     for (const id of graphics) {
  //       const element = this.findSvgElement(root, id, select)
  //       if (!element) {
  //         console.error(`The '${id}' id is not found`)
  //         break
  //       }
  //       this.updateGraphicsElement(element, color)
  //     }
  //   }

  /**
   * 根据给定的单元格 ID，在 SVG 中查找对应的元素。
   * - 从第四层嵌套的 <g> 元素中查找 `data-cell-id` 属性匹配的节点。
   *
   * @param root SVG 根节点
   * @param id 要查找的单元格 ID
   * @param select XPath 查询函数
   * @returns 匹配的元素，若未找到则返回 null
   */
  private findSvgElement(root: HTMLElement, id: string, select: xpath.XPathSelect): Element | null {
    const groups = select('svg:g/svg:g/svg:g/svg:g', root) as Element[]

    for (const g of Array.from(groups)) {
      if (g.getAttribute('data-cell-id') === id) {
        return g
      }
    }

    return null
  }

  private parser(xml: string): ClockTree {
    const widgets: Record<string, GeometryType> = {}
    const lines: string[] = []
    const texts: string[] = []
    const graphics: string[] = []
    const dom = new DOMParser()
    const root = dom.parseFromString(xml, 'text/xml').documentElement
    const drawioRootString = root.getAttribute('content')
    if (!drawioRootString)
      throw new Error('Missing \'content\' attribute in root')
    const drawioRoot = dom.parseFromString(drawioRootString, 'text/xml').documentElement
    const svgSelect = xpath.useNamespaces({ svg: root.namespaceURI ?? '' })

    // TODO: 添加版本判断
    // const versionAttr = drawioRoot.getAttribute('version')
    const diagram = drawioRoot.getElementsByTagName('diagram')[0]

    const objectNodes = xpath.select('mxGraphModel/root/object', diagram) as Element[]
    const mxCellNodes = xpath.select('mxGraphModel/root/mxCell', diagram) as Element[]

    for (const obj of objectNodes) {
      const id = obj.getAttribute('id')
      const mxCell = obj.getElementsByTagName('mxCell')[0]
      if (!mxCell || !id) {
        console.error('The \'mxCell\' node is not found')
        break
      }
      mxCell.setAttribute('id', id)
      mxCellNodes.push(mxCell)
    }

    for (const mxCell of mxCellNodes) {
      const cell = new MxCell(mxCell)
      const id = mxCell.getAttribute('id')

      if (!id)
        continue

      if (this.isWidget(cell)) {
        const element = this.findSvgElement(root, id, svgSelect)
        if (!element) {
          console.error(`The '${id}' id is not found`)
          break
        }

        const ellipses = svgSelect('svg:g/svg:g/svg:ellipse', element) as Element[]
        const rects = svgSelect('svg:g/svg:g/svg:rect', element) as Element[]

        let x = 0
        let y = 0
        let width = 0
        let height = 0

        if (ellipses.length === 1) {
          const ellipse = ellipses[0]
          x = Number.parseFloat(ellipse.getAttribute('cx')!) - Number.parseFloat(ellipse.getAttribute('rx')!) + 0.5
          y = Number.parseFloat(ellipse.getAttribute('cy')!) - Number.parseFloat(ellipse.getAttribute('ry')!) + 0.5
          width = Number.parseFloat(ellipse.getAttribute('rx')!) * 2
          height = Number.parseFloat(ellipse.getAttribute('ry')!) * 2
        }
        else if (rects.length === 1) {
          const rect = rects[0]
          x = Number.parseFloat(rect.getAttribute('x')!)
          y = Number.parseFloat(rect.getAttribute('y')!)
          width = Number.parseFloat(rect.getAttribute('width')!) + 1
          height = Number.parseFloat(rect.getAttribute('height')!) + 1
        }
        else {
          console.warn(
            `There was a problem parsing the svg file, the default svg configuration will be used. id '${id}'`,
          )
          const mxGeometry = mxCell.getElementsByTagName('mxGeometry')[0]
          if (!mxGeometry) {
            console.error('The \'mxGeometry\' node is not found')
            break
          }
          x = Number.parseFloat(mxGeometry.getAttribute('x') ?? '0') + 1
          y = Number.parseFloat(mxGeometry.getAttribute('y') ?? '0') + 1
          width = Number.parseFloat(mxGeometry.getAttribute('width') ?? '0') + 1
          height = Number.parseFloat(mxGeometry.getAttribute('height') ?? '0') + 1
        }

        widgets[id] = { x, y, width, height }
      }
      else if (this.isLine(cell)) {
        lines.push(id)
      }
      else if (this.isText(cell)) {
        texts.push(id)
      }
      else if (this.isGraphics(cell)) {
        graphics.push(id)
      }
    }

    for (const id of Object.keys(widgets)) {
      const element = this.findSvgElement(root, id, svgSelect)
      if (!element) {
        console.error(`The '${id}' id is not found`)
        break
      }
      // TODO: 更新主题颜色
      this.updateGraphicsElement(element, 'transparent')
    }
    // this.updateLines(root, lines, 'rgb(255, 0, 0)', svgSelect)
    // this.updateTexts(root, texts, 'rgb(255, 0, 0)', svgSelect)
    // this.updateGraphics(root, graphics, 'rgb(255, 0, 0)', svgSelect)

    const serializer = new XMLSerializer()
    const xmlString = serializer.serializeToString(root)
    return new ClockTree(xmlString, widgets)
  }

  async load(vendor: string, name: string) {
    const content = await window.electron.invoke('database:getClockTree', vendor, name) as string

    const rtn = this.parser(content);

    (this._map[vendor] ??= {})[name] = rtn
  }

  get(vendor: string, name: string): ClockTree | null {
    if (this._map[vendor]?.[name]) {
      return this._map[vendor][name]
    }

    return null
  }
}

export function createClockTreeManagerPlugin() {
  const manager = new ClockTreeManager()

  return {
    value: manager,
    plugin: {
      install(app: App) {
        app.provide('database:clockTreeManager', manager)
      },
    },
  }
}

export function useClockTreeManager(): ClockTreeManager {
  return inject('database:clockTreeManager')!
}
