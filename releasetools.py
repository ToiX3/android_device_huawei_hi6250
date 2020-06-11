#
# Copyright 2020 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# This contains the module build definitions for the hardware-specific
# components for this device.
#
# As much as possible, those components should be built unconditionally,
# with device-specific names to avoid collisions, to avoid device-specific
# bitrot and build breakages. Building a component unconditionally does
# *not* include it on all devices, so it is safe even with hardware-specific
# components.

"""Custom OTA commands for hi6250"""

import common
import os
import sys
import time

LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_DIR = os.getenv('OUT')
UTILITIES_DIR = os.path.join(TARGET_DIR, 'symbols')
ROM = os.getenv ('TARGET_PRODUCT').split("_",1)

def addFolderToZip(info, directory, basedir):
    list = os.listdir(directory)
 
    for entity in list:
        each = os.path.join(directory,entity)
 
        if os.path.isfile(each):
            print "Adding override file -> "+ os.path.join(basedir, entity)
            info.output_zip.write(each, os.path.join(basedir, entity))
        else:
            addFolderToZip(info,each,os.path.join(basedir, entity))

def FullOTA_Assertions(info):
  sys.setrecursionlimit(100000)

  if os.path.isdir(os.path.join(TARGET_DIR, "override")):
  	addFolderToZip(info, os.path.join(TARGET_DIR, "override"),"override")
  else :
	print "Warning!: no override blobs found."
	time.sleep(2)

  info.output_zip.write(os.path.join(TARGET_DIR, "install/bin/data-formatter.sh"), "install/bin/data-formatter.sh")
  info.output_zip.write(os.path.join(TARGET_DIR, "install/bin/finalize.sh"), "install/bin/finalize.sh")
  info.output_zip.write(os.path.join(TARGET_DIR, "install/bin/stock-check.sh"), "install/bin/stock-check.sh")
  info.output_zip.write(os.path.join(TARGET_DIR, "system/bin/volumeinput"), "install/bin/volumeinput")

  info.script.AppendExtra('package_extract_dir("install", "/tmp/install");')

  info.script.AppendExtra('assert(run_program("/sbin/chmod","755", "/tmp/install/bin/data-formatter.sh") == 0 || abort("Could not chmod data-formatter"););')
  info.script.AppendExtra('assert(run_program("/sbin/chmod","755", "/tmp/install/bin/finalize.sh") == 0 || abort("Could not chmod finalize"););')
  info.script.AppendExtra('assert(run_program("/sbin/chmod","755", "/tmp/install/bin/stock-check.sh") == 0 || abort("Could not chmod stock-check"););')
  info.script.AppendExtra('assert(run_program("/sbin/chmod","755", "/tmp/install/bin/volumeinput") == 0|| abort("Could not chmod volumeinput"););')

  info.script.AppendExtra('assert(run_program("/tmp/install/bin/data-formatter.sh") == 0 || abort("ERROR!: Data could not be formatted! You should reboot to recovery after installation and format /data!"););')
  info.script.AppendExtra('assert(run_program("/tmp/install/bin/stock-check.sh") == 0 || abort("stock-check failed."););')


def FullOTA_InstallEnd(info):
  info.script.AppendExtra('package_extract_dir("override", "/system");')
  info.script.AppendExtra('assert(run_program("/tmp/install/bin/finalize.sh") == 0 || abort("finalize failed but installation should be OK."););')

