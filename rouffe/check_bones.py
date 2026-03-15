# ============================================================
# check_bones.py  —  XPS→MMD 骨骼完整性检查
#
# 经验总结：
# 1. XPS 导入后骨骼名是英文，需要先跑 01_rename_bones.py
# 2. XPS 缺少 MMD 标准骨骼，需要手动添加
# 3. 父子关系也可能不对，需要一并检查
# 4. 每次操作后立刻运行本脚本验证，不要等到最后
# ============================================================
import bpy

XPS_ARMATURE = 'Armature'

# ============================================================
# MMD 标准骨骼定义
# 格式：骨骼名 → 期望的父骨骼名
# ============================================================
MMD_STANDARD = {
    # --- 根/重心 ---
    '全ての親':  'ROOT',
    'センター':  '全ての親',

    # --- 躯干主链（最容易出问题的部分）---
    '腰':        'センター',    # XPS 没有，需要手动添加
    '上半身':    '腰',          # XPS 原本 parent=下半身，需要修正
    '上半身1':   '上半身',      # XPS 没有，需要手动添加
    '上半身2':   '上半身1',     # XPS 原本 parent=上半身，需要修正
    '下半身':    '腰',          # XPS 原本 parent=unused trash 17，需要修正
    '首':        '上半身2',
    '頭':        '首',

    # --- 眼睛 ---
    '目.L':      '頭',
    '目.R':      '頭',

    # --- 左腿 ---
    '足.L':      'センター',
    'ひざ.L':    '足.L',
    '足首.L':    'ひざ.L',
    'つま先.L':  '足首.L',

    # --- 右腿 ---
    '足.R':      'センター',
    'ひざ.R':    '足.R',
    '足首.R':    'ひざ.R',
    'つま先.R':  '足首.R',

    # --- 脚部IK ---
    '足IK親.L':   '全ての親',
    '足ＩＫ.L':   '足IK親.L',
    'つま先ＩＫ.L': '足ＩＫ.L',
    '足IK親.R':   '全ての親',
    '足ＩＫ.R':   '足IK親.R',
    'つま先ＩＫ.R': '足ＩＫ.R',

    # --- 肩/臂 ---
    '肩P.L':     '上半身2',
    '肩.L':      '肩P.L',
    '肩C.L':     '肩.L',
    '腕.L':      '肩C.L',
    'ひじ.L':    '腕.L',
    '手首.L':    'ひじ.L',

    '肩P.R':     '上半身2',
    '肩.R':      '肩P.R',
    '肩C.R':     '肩.R',
    '腕.R':      '肩C.R',
    'ひじ.R':    '腕.R',
    '手首.R':    'ひじ.R',

    # --- 手指 ---
    '親指０.L':  '手首.L', '親指１.L':  '親指０.L', '親指２.L':  '親指１.L',
    '人指１.L':  '手首.L', '人指２.L':  '人指１.L', '人指３.L':  '人指２.L',
    '中指１.L':  '手首.L', '中指２.L':  '中指１.L', '中指３.L':  '中指２.L',
    '薬指１.L':  '手首.L', '薬指２.L':  '薬指１.L', '薬指３.L':  '薬指２.L',
    '小指１.L':  '手首.L', '小指２.L':  '小指１.L', '小指３.L':  '小指２.L',

    '親指０.R':  '手首.R', '親指１.R':  '親指０.R', '親指２.R':  '親指１.R',
    '人指１.R':  '手首.R', '人指２.R':  '人指１.R', '人指３.R':  '人指２.R',
    '中指１.R':  '手首.R', '中指２.R':  '中指１.R', '中指３.R':  '中指２.R',
    '薬指１.R':  '手首.R', '薬指２.R':  '薬指１.R', '薬指３.R':  '薬指２.R',
    '小指１.R':  '手首.R', '小指２.R':  '小指１.R', '小指３.R':  '小指２.R',
}

# ============================================================
# 分阶段检查：按转换步骤分组
# ============================================================
PHASES = {
    'Phase 1 - 根/重心/躯干（最关键）': [
        '全ての親', 'センター', '腰',
        '下半身',
        '上半身', '上半身1', '上半身2',
        '首', '頭',
    ],
    'Phase 2 - 腿部': [
        '足.L', 'ひざ.L', '足首.L', 'つま先.L',
        '足.R', 'ひざ.R', '足首.R', 'つま先.R',
    ],
    'Phase 3 - 脚部IK': [
        '足IK親.L', '足ＩＫ.L', 'つま先ＩＫ.L',
        '足IK親.R', '足ＩＫ.R', 'つま先ＩＫ.R',
    ],
    'Phase 4 - 肩/臂': [
        '肩P.L', '肩.L', '肩C.L', '腕.L', 'ひじ.L', '手首.L',
        '肩P.R', '肩.R', '肩C.R', '腕.R', 'ひじ.R', '手首.R',
    ],
    'Phase 5 - 手指': [
        '親指０.L', '親指１.L', '親指２.L',
        '人指１.L', '人指２.L', '人指３.L',
        '中指１.L', '中指２.L', '中指３.L',
        '薬指１.L', '薬指２.L', '薬指３.L',
        '小指１.L', '小指２.L', '小指３.L',
        '親指０.R', '親指１.R', '親指２.R',
        '人指１.R', '人指２.R', '人指３.R',
        '中指１.R', '中指２.R', '中指３.R',
        '薬指１.R', '薬指２.R', '薬指３.R',
        '小指１.R', '小指２.R', '小指３.R',
    ],
}

def check_bones(armature_name=XPS_ARMATURE):
    arm = bpy.data.objects.get(armature_name)
    if not arm:
        print(f"[错误] 找不到骨骼对象: {armature_name}")
        return

    bones = {b.name: b for b in arm.data.bones}
    total_ok = total_missing = total_wrong_parent = 0

    for phase, bone_list in PHASES.items():
        print(f"\n{'='*50}")
        print(f"  {phase}")
        print(f"{'='*50}")

        for bname in bone_list:
            expected_parent = MMD_STANDARD.get(bname, '?')
            b = bones.get(bname)

            if b is None:
                print(f"  ❌ {bname:<20} 缺失！（应 parent={expected_parent}）")
                total_missing += 1
            else:
                actual_parent = b.parent.name if b.parent else 'ROOT'
                parent_ok = (actual_parent == expected_parent)
                if parent_ok:
                    print(f"  ✅ {bname:<20} parent={actual_parent}")
                    total_ok += 1
                else:
                    print(f"  ⚠️  {bname:<20} parent={actual_parent}  （期望: {expected_parent}）")
                    total_wrong_parent += 1

    print(f"\n{'='*50}")
    print(f"  汇总")
    print(f"{'='*50}")
    print(f"  ✅ 正确:       {total_ok}")
    print(f"  ❌ 缺失:       {total_missing}")
    print(f"  ⚠️  父子关系错: {total_wrong_parent}")

    if total_missing == 0 and total_wrong_parent == 0:
        print(f"\n  🎉 全部通过！")
    else:
        print(f"\n  需要修复后继续")

check_bones()
