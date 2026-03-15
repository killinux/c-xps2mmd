# ============================================================
# 01b_add_torso_bones.py  —  添加躯干缺失骨骼并修正父子关系
# 添加：腰、上半身1
# 修正：下半身/上半身 parent→腰、上半身2 parent→上半身1
# ============================================================
import bpy

XPS_ARMATURE = 'Armature'

def add_torso_bones():
    arm = bpy.data.objects.get(XPS_ARMATURE)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='EDIT')
    eb = arm.data.edit_bones

    # 读取现有骨骼位置
    b_lower  = eb.get('下半身')
    b_upper  = eb.get('上半身')
    b_upper2 = eb.get('上半身2')
    b_center = eb.get('センター')

    # === 添加 腰 ===
    b_koshi = eb.new('腰')
    b_koshi.head = b_lower.head.copy()  # 和下半身 head 同位置
    b_koshi.tail = (b_koshi.head.x, b_koshi.head.y, b_koshi.head.z + 0.05)
    b_koshi.parent = b_center
    b_koshi.use_deform = True

    # === 添加 上半身1 ===
    b_upper1 = eb.new('上半身1')
    # 放在 上半身 head 和 上半身2 head 的中点
    mid_z = (b_upper.head.z + b_upper2.head.z) / 2
    b_upper1.head = (0.0, b_upper.head.y, mid_z)
    b_upper1.tail = (0.0, b_upper.head.y, b_upper2.head.z)
    b_upper1.parent = b_upper
    b_upper1.use_deform = True

    # === 修正父子关系 ===
    b_lower.parent  = eb.get('腰')   # 下半身 → 腰
    b_upper.parent  = eb.get('腰')   # 上半身 → 腰
    b_upper2.parent = eb.get('上半身1')  # 上半身2 → 上半身1

    bpy.ops.object.mode_set(mode='OBJECT')

    # 验证
    expected = [
        ('腰',     'センター'),
        ('下半身',  '腰'),
        ('上半身',  '腰'),
        ('上半身1', '上半身'),
        ('上半身2', '上半身1'),
    ]
    all_ok = True
    for child, exp_parent in expected:
        b = arm.data.bones.get(child)
        actual = b.parent.name if b and b.parent else 'ROOT'
        ok = actual == exp_parent
        if not ok: all_ok = False
        print(f"  {'✅' if ok else '❌'} {child} → {actual}")
    print(f"\n{'✅ 躯干骨骼完成！' if all_ok else '❌ 有问题'}")

add_torso_bones()
