# Конфигурация для обучения на категории "bottle" из MVTec AD
DATA_PATH="/path/to/your/MVTec_AD"
CATEGORY="bottle"
RESULTS_DIR="results_mvtec_bottle"
GPU_ID=${2:-0}

BACKBONE="wideresnet50"
LAYERS="layer2 layer3"
PRETRAIN_EMBED_DIM=1024
TARGET_EMBED_DIM=1024
SCORER_NUM_NN=1
PATCHSIZE=3
SAMPLING_RATIO=0.1
RESIZE=256
IMAGESIZE=224
