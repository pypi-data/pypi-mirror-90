#
#  Copyright 2020 Intellivoid Technologies
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  
 

from enum import Enum

class ZiProtoFormat(Enum):
    POSITIVE_FIXINT     = 0x00
    FIXMAP              = 0x80
    FIXARRAY            = 0x90
    FIXSTR              = 0xA0
    NIL                 = 0xC0
    FALSE               = 0xC2
    TRUE                = 0xC3
    BIN8                = 0xC4
    BIN16               = 0xC5
    BIN32               = 0xC6
    FLOAT32             = 0xCA
    FLOAT64             = 0xCB
    UINT8               = 0xCC
    UINT16              = 0xCD
    UINT32              = 0xCE
    UINT64              = 0xCF
    INT8                = 0xD0
    INT16               = 0xD1
    INT32               = 0xD2
    INT64               = 0xD3
    STR8                = 0xD9
    STR16               = 0xDA
    STR32               = 0xDB
    ARRAY16             = 0xDC
    ARRAY32             = 0xDD
    MAP16               = 0xDE
    MAP32               = 0xDF
    NEGATIVE_FIXINT     = 0xE0
