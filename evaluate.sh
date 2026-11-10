#!/bin/bash

MODEL_PATH="results_visa_candle/project/group/models/mvtec_candle"
DATA_PATH="/path/to/your/VisA_ready_fixed"
CATEGORY="candle"
GPU_ID=${1:-0}

echo "Запуск оценки для модели: $MODEL_PATH"

env PYTHONPATH=src python bin/load_and_evaluate_patchcore.py \
  --gpu $GPU_ID --seed 0 \
  --save_segmentation_images \
  results_evaluation_vis \
  patch_core_loader \
  -p $MODEL_PATH \
  dataset --resize 256 --imagesize 224 \
  -d $CATEGORY mvtec $DATA_PATH
