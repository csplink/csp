/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        contributors.ts
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
 *  2025-04-27     xqyjlj       initial version
 */

import type { AxiosResponse } from 'axios'
import { Buffer } from 'node:buffer'
import fs from 'node:fs'
import path from 'node:path'
import axios from 'axios'

export interface ContributorType {
  avatar: string
  contributions: number
  htmlUrl: string
  name: string
}

interface UserApiContextType {
  login: string
  id: number
  avatar_url: string
  html_url: string
}

interface ContributorApiContextType {
  login: string
  id: number
  avatar_url: string
  html_url: string
  contributions: number
}

async function getUserFromApi(username: string): Promise<UserApiContextType> {
  const url = `https://api.github.com/users/${username}`
  const resp: AxiosResponse<UserApiContextType> = await axios.get(url)
  return resp.data
}

async function getContributorsFromApi(owner: string, repo: string, token: string): Promise<ContributorApiContextType[]> {
  const headers = { Authorization: `token ${token}` }
  const perPage = 30
  let page = 1
  let contributors: ContributorApiContextType[] = []

  while (true) {
    const url = `https://api.github.com/repos/${owner}/${repo}/contributors?per_page=${perPage}&page=${page}`
    const resp: AxiosResponse<ContributorApiContextType[]> = await axios.get(url, { headers })
    const data = resp.data

    if (data.length === 0)
      break

    contributors = contributors.concat(data)
    page++
  }

  const names = contributors.map(c => c.login)
  if (!names.includes('HalfSweet')) {
    const user = await getUserFromApi('HalfSweet')
    contributors.push({
      login: user.login,
      avatar_url: user.avatar_url,
      html_url: user.html_url,
      id: user.id,
      contributions: 1,
    })
  }

  return contributors.sort((a, b) => b.contributions - a.contributions)
}

export async function generateContributors(root: string, owner: string, repo: string, token: string): Promise<void> {
  const contributors = await getContributorsFromApi(owner, repo, token)
  const avatarFolder = path.join(root, 'resources', 'contributors', 'avatar')

  if (fs.existsSync(avatarFolder)) {
    fs.rmSync(avatarFolder, { recursive: true })
  }
  fs.mkdirSync(avatarFolder, { recursive: true })

  const contributorList: ContributorType[] = []

  for (const contributor of contributors) {
    const response = await axios.get(contributor.avatar_url, { responseType: 'arraybuffer' })
    const buffer = Buffer.from(response.data)
    const filePath = path.join(avatarFolder, contributor.id.toString())
    fs.writeFileSync(filePath, buffer)

    // eslint-disable-next-line no-console
    console.info(`Author: ${contributor.login}, Contributions: ${contributor.contributions}`)

    contributorList.push({
      name: contributor.login,
      avatar: `avatar/${path.basename(filePath)}`,
      htmlUrl: contributor.html_url,
      contributions: contributor.contributions,
    })
  }

  const outputPath = path.join(path.dirname(avatarFolder), 'contributors')
  fs.writeFileSync(outputPath, JSON.stringify(contributorList, null, 2), 'utf8')
}
