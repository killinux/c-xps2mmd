# ============================================================
# 01c_add_shoulder_bones.py  —  添加肩部辅助骨骼
# 添加：肩P.L/R（parent=上半身2）、肩C.L/R（parent=肩.L/R）
# 修正：肩.L/R parent→肩P、腕.L/R parent→肩C
#
# 注意：肩C.tail 朝 +Z，腕必须设 use_connect=False
#       否则腕 head 会自动吸附到肩C tail，造成位置偏移
# ============================================================
import bpy

XPS_ARMATURE = 'Armature'

def add_shoulder_bones():
    arm = bpy.data.objects.get(XPS_ARMATURE)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='EDIT')
    eb = arm.data.edit_bones

    for side in ['L', 'R']:
        b_shoulder = eb.get(f'肩.{side}')
        b_arm      = eb.get(f'腕.{side}')
        b_upper2   = eb.get('上半身2')

        # 肩P：肩 head と同位置，+Z方向，辅助骨骼
        bp = eb.new(f'肩P.{side}')
        bp.head = b_shoulder.head.copy()
        bp.tail = (bp.head.x, bp.head.y, bp.head.z + 0.05)
        bp.parent = b_upper2
        bp.use_connect = False
        bp.use_deform = False

        # 肩C：腕 head と同位置，+Z方向，辅助骨骼
        bc = eb.new(f'肩C.{side}')
        bc.head = b_arm.head.copy()
        bc.tail = (bc.head.x, bc.head.y, bc.head.z + 0.05)
        bc.parent = b_shoulder
        bc.use_connect = False
        bc.use_deform = False

        # 修正父子関係
        b_shoulder.parent = eb.get(f'肩P.{side}')
        b_shoulder.use_connect = False

        b_arm.parent = eb.get(f'肩C.{side}')
        b_arm.use_connect = False  # 重要：自動接続を防ぐ

        print(f'  ✅ {side}側 肩部骨骼完成')

    bpy.ops.object.mode_set(mode='OBJECT')
    print('\n✅ 肩部骨骼添加完成！')

add_shoulder_bones()
