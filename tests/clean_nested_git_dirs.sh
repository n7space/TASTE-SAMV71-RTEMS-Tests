#~/bin/bash

set -euo pipefail

find . -name .git -type d | while read git_dir; do echo "Removing dir ${git_dir}"; rm -rf $git_dir; done
