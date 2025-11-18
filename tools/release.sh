#!/bin/bash

# Licensed under the Apache License v. 2 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2025-2025 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        release.sh
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-18     xqyjlj       initial version
#

PLATFORM="$1" # linux 或 windows
REF_NAME="$2" # GitHub Actions 传入的 ref name (tag)

CSP_VERSION=$(npm pkg get version | tr -d '"')

echo "Platform: $PLATFORM"
echo "Version: $CSP_VERSION"
echo "Ref name: $REF_NAME"

# setup
if [[ "$PLATFORM" == "linux" ]]; then
    cp -v release/${CSP_VERSION}/csp-Linux-${CSP_VERSION}.AppImage csp-linux-setup-${REF_NAME}.AppImage
elif [[ "$PLATFORM" == "windows" ]]; then
    cp -v release/${CSP_VERSION}/csp-Windows-${CSP_VERSION}-Setup.exe csp-windows-setup-${REF_NAME}.exe
else
    echo "Unsupported platform: $PLATFORM"
    exit 1
fi

# portable
pushd release/${CSP_VERSION}/
if [[ "$PLATFORM" == "linux" ]]; then
    cp -rv linux-unpacked csp-linux-portable-${REF_NAME}
    tar czf csp-linux-portable-${REF_NAME}.tar.gz csp-linux-portable-${REF_NAME}
    cp -v csp-linux-portable-${REF_NAME}.tar.gz ../../
elif [[ "$PLATFORM" == "windows" ]]; then
    cp -rv win-unpacked csp-windows-portable-${REF_NAME}
    7z a csp-windows-portable-${REF_NAME}.zip csp-windows-portable-${REF_NAME}
    cp -v csp-windows-portable-${REF_NAME}.zip ../../
else
    echo "Unsupported platform: $PLATFORM"
    exit 1
fi
popd


# server
mkdir -pv csp-${PLATFORM}-server-${REF_NAME}
if [[ "$PLATFORM" == "linux" ]]; then
    cp -v build-server/csp-server csp-linux-server-${REF_NAME}/
elif [[ "$PLATFORM" == "windows" ]]; then
    cp -v build-server/csp-server.exe csp-windows-server-${REF_NAME}/
else
    echo "Unsupported platform: $PLATFORM"
    exit 1
fi
cp -rv server/public csp-${PLATFORM}-server-${REF_NAME}/
cp -rv resources csp-${PLATFORM}-server-${REF_NAME}/
find csp-${PLATFORM}-server-${REF_NAME} -type d -name "__pycache__" -exec rm -rf {} +
rm -rf csp-${PLATFORM}-server-${REF_NAME}/resources/images
if [[ "$PLATFORM" == "linux" ]]; then
    tar czf csp-linux-server-${REF_NAME}.tar.gz csp-linux-server-${REF_NAME}
elif [[ "$PLATFORM" == "windows" ]]; then
    7z a csp-windows-server-${REF_NAME}.zip csp-windows-server-${REF_NAME}
else
    echo "Unsupported platform: $PLATFORM"
    exit 1
fi
