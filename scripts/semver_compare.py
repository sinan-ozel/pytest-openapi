import sys
from packaging.version import Version

if len(sys.argv) != 3:
    print("Usage: semver_compare.py <version1> <version2>")
    sys.exit(2)

v1 = Version(sys.argv[1])
v2 = Version(sys.argv[2])

if v1 >= v2:
    sys.exit(0)
else:
    sys.exit(1)
