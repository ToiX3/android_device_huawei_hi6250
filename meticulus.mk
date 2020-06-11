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

ifeq ($(I_AM_METICULUS), true)
$(shell echo "Using Huawei Preferences" >&2)

# Recovery
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/recovery/init.recovery.meticulus.rc:root/init.recovery.meticulus.rc \
    $(LOCAL_PATH)/recovery/data-formatter.sh:install/bin/data-formatter.sh \
    $(LOCAL_PATH)/recovery/finalize.sh:install/bin/finalize.sh \
    $(LOCAL_PATH)/recovery/stock-check.sh:install/bin/stock-check.sh \

# Release Tools
TARGET_RELEASETOOLS_EXTENSIONS := device/huawei/hi6250

# Volume Input
PRODUCT_PACKAGES += \
    volumeinput

endif
