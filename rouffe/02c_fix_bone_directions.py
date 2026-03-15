# ============================================================
# 02c_fix_bone_directions.py  —  修正关键骨骼朝向
# XPS 导入后部分骨骼朝向和 MMD 标准不一致
# 最关键的是 全ての親 需要朝 +Z（向上）
# ============================================================
import bpy

XPS_ARMATURE = 'Armature'

def fix_bone_directions():
    arm = bpy.data.objects.get(XPS_ARMATURE)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='EDIT')
    eb = arm.data.edit_bones

    fixes = {
        '全ての親': (0.0,  0.0,  0.125),   # 朝 +Z（MMD标准）
        'センター':  (0.0,  0.0,  1.125),   # 朝 +Z
        '上半身':   None,  # 由 head→tail 自动确定
        '上半身2':  None,
    }

    # 全ての親：强制朝 +Z
    b = eb.get('全ての親')
    if b:
        b.tail.x = 0.0
        b.tail.y = 0.0
        b.tail.z = 0.125
        print(f"  ✅ 全ての親: → +Z")

    # センター：朝 +Z
    b = eb.get('センター')
    if b:
        b.tail.x = b.head.x
        b.tail.y = b.head.y
        b.tail.z = b.head.z + 0.1
        print(f"  ✅ センター: → +Z")

    # 下半身：朝 -Z（向下）
    b = eb.get('下半身')
    if b:
        b.tail.x = b.head.x
        b.tail.y = b.head.y
        b.tail.z = b.head.z - 0.1
        print(f"  ✅ 下半身: → -Z")

    # 上半身/上半身2：朝 +Z
    for bname in ['上半身', '上半身2']:
        b = eb.get(bname)
        if b:
            b.tail.x = b.head.x
            b.tail.y = b.head.y
            b.tail.z = b.head.z + 0.1
            print(f"  ✅ {bname}: → +Z")

    bpy.ops.object.mode_set(mode='OBJECT')
    print("\n✅ 骨骼朝向修正完成")

fix_bone_directions()
