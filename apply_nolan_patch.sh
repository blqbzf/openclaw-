#!/usr/bin/env bash
set -euo pipefail
cd /tmp/openclaw-patchflow
python3 /Users/mac/wow-server/pb-core/scripts/dbc/patch_nolan_iron_steed.py \
  --source /tmp/openclaw-patchflow/patches/src/wuzitianshu/DBFilesClient/Item.dbc \
  --item-template-sql /Users/mac/wow-server/pb-core/data/sql/base/db_world/item_template.sql \
  --new-entry 910003 \
  --output /tmp/openclaw-patchflow/patches/src/wuzitianshu/DBFilesClient/Item.dbc
