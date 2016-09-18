# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from kafkatest.utils import kafkatest_version

from distutils.version import LooseVersion


class KafkaVersion(LooseVersion):
    """Container for kafka versions which makes versions simple to compare.

    distutils.version.LooseVersion (and StrictVersion) has robust comparison and ordering logic.

    Example:

        v10 = KafkaVersion("0.10.0")
        v9 = KafkaVersion("0.9.0.1")
        assert v10 > v9  # assertion passes!
    """
    def __init__(self, version_string):
        self.is_trunk = (version_string.lower() == "trunk")
        if self.is_trunk:
            # Since "trunk" may actually be a branch that is not trunk,
            # use kafkatest_version() for comparison purposes,
            # and track whether we're in "trunk" with a flag
            version_string = kafkatest_version()

            # Drop dev suffix if present
            dev_suffix_index = version_string.find(".dev")
            if dev_suffix_index >= 0:
                version_string = version_string[:dev_suffix_index]

        # Don't use the form super.(...).__init__(...) because
        # LooseVersion is an "old style" python class
        LooseVersion.__init__(self, version_string)

    def __str__(self):
        if self.is_trunk:
            return "trunk"
        else:
            return LooseVersion.__str__(self)


def get_version(node=None):
    """Return the version attached to the given node.
    Default to trunk if node or node.version is undefined (aka None)
    """
    if node is not None and hasattr(node, "version") and node.version is not None:
        return node.version
    else:
        return TRUNK

TRUNK = KafkaVersion("trunk")

# 0.8.2.X versions
V_0_8_2_1 = KafkaVersion("0.8.2.1")
V_0_8_2_2 = KafkaVersion("0.8.2.2")
LATEST_0_8_2 = V_0_8_2_2

# 0.9.0.X versions
V_0_9_0_0 = KafkaVersion("0.9.0.0")
V_0_9_0_1 = KafkaVersion("0.9.0.1")
LATEST_0_9 = V_0_9_0_1

# 0.10.0.X versions
V_0_10_0_0 = KafkaVersion("0.10.0.0")
LATEST_0_10 = V_0_10_0_0
