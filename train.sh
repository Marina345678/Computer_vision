#!/bin/bash

CONFIG_FILE=$1
if [ -z "$CONFIG_FILE" ]; then
    echo "Использование: sh train.sh <путь_к_конфигу> [--gpu <id>]"
    exit 1
fi

source $CONFIG_FILE
GPU_ID=${2:-$GPU_ID}

echo "Запуск обучения для категории: $CATEGORY"

env PYTHONPATH=src python bin/run_patchcore.py \
  --gpu $GPU_ID --seed 0 --save_patchcore_model \
  $RESULTS_DIR \
  patch_core -b $BACKBONE -le $LAYERS \
  --pretrain_embed_dimension $PRETRAIN_EMBED_DIM --target_embed_dimension $TARGET_EMBED_DIM \
  --anomaly_scorer_num_nn $SCORER_NUM_NN --patchsize $PATCHSIZE \
  sampler -p $SAMPLING_RATIO approx_greedy_coreset \
  dataset --resize $RESIZE --imagesize $IMAGESIZE -d $CATEGORY mvtec $DATA_PATH
