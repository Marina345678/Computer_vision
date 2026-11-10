import os
import shutil
import random

# --- НАСТРОЙКИ ---
SRC_BASE = '/content/drive/MyDrive/mvtec_data/VisA_partial'
DST_BASE = '/content/drive/MyDrive/mvtec_data/VisA_ready_fixed/'
TRAIN_RATIO = 0.8
CATEGORIES = ['candle', 'pcb1']
random.seed(42)

for cat in CATEGORIES:
    print(f"\n🔄 Обработка категории: {cat}")
    src_cat = os.path.join(SRC_BASE, cat)

    normal_dir = os.path.join(src_cat, 'Data', 'Images', 'Normal')
    anomaly_dir = os.path.join(src_cat, 'Data', 'Images', 'Anomaly')
    masks_dir = os.path.join(src_cat, 'Data', 'Masks', 'Anomaly')

    dst_cat = os.path.join(DST_BASE, cat)
    train_good_dir = os.path.join(dst_cat, 'train', 'good')
    test_good_dir = os.path.join(dst_cat, 'test', 'good')
    test_defect_dir = os.path.join(dst_cat, 'test', 'defect')
    gt_dir = os.path.join(dst_cat, 'ground_truth', 'defect')

    for d in [train_good_dir, test_good_dir, test_defect_dir, gt_dir]:
        os.makedirs(d, exist_ok=True)

    # 1. Обработка Normal (Train/Test)
    normal_files = [f for f in os.listdir(normal_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    random.shuffle(normal_files)

    split_idx = int(len(normal_files) * TRAIN_RATIO)
    train_files = normal_files[:split_idx]
    test_files = normal_files[split_idx:]

    for f in train_files:
        shutil.copy(os.path.join(normal_dir, f), os.path.join(train_good_dir, f))
    for f in test_files:
        shutil.copy(os.path.join(normal_dir, f), os.path.join(test_good_dir, f))

    print(f"  ✅ Normal: {len(train_files)} в train, {len(test_files)} в test/good")

    # 2. Обработка Anomaly (Test + Mask)
    anomaly_files = [f for f in os.listdir(anomaly_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    mask_dict = {os.path.splitext(f)[0]: f for f in os.listdir(masks_dir) if f.lower().endswith('.png')}

    skipped = 0
    for f in anomaly_files:
        file_base = os.path.splitext(f)[0]

        if file_base in mask_dict:
            mask_name = mask_dict[file_base]
            shutil.copy(os.path.join(anomaly_dir, f), os.path.join(test_defect_dir, f))
            new_mask_name = f"{file_base}_mask.png"
            shutil.copy(os.path.join(masks_dir, mask_name), os.path.join(gt_dir, new_mask_name))
        else:
            skipped += 1

    print(f"  ✅ Anomaly: скопировано {len(anomaly_files) - skipped} дефектов (пропущено без масок: {skipped}).")

print(f"\n🎉 Готово! Датасет переорганизован: {DST_BASE}")
