# ============================================================
# 01d_add_ik_bones.py  —  添加脚部 IK 骨骼
# 添加：足IK親.L/R、足ＩＫ.L/R、つま先ＩＫ.L/R
# 父子关系：全ての親 → 足IK親 → 足ＩＫ → つま先ＩＫ
# ============================================================
import bpy

XPS_ARMATURE = 'Armature'

def add_ik_bones():
    arm = bpy.data.objects.get(XPS_ARMATURE)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='EDIT')
    eb = arm.data.edit_bones

    for side in ['L', 'R']:
        ankle = eb.get(f'足首.{side}')
        toe   = eb.get(f'つま先.{side}')
        root  = eb.get('全ての親')

        # 足IK親：地面(Z=0)，对齐脚踝 X 坐标，父=全ての親
        b = eb.new(f'足IK親.{side}')
        b.head = (ankle.head.x, ankle.head.y, 0.0)
        b.tail = (ankle.head.x, ankle.head.y, ankle.head.z)
        b.parent = root
        b.use_connect = False
        b.use_deform = False

        # 足ＩＫ：脚踝高度，主 IK 控制器，父=足IK親
        b = eb.new(f'足ＩＫ.{side}')
        b.head = ankle.head.copy()
        b.tail = (ankle.head.x, ankle.head.y + 0.08, ankle.head.z)
        b.parent = eb.get(f'足IK親.{side}')
        b.use_connect = False
        b.use_deform = False

        # つま先ＩＫ：脚尖位置，控制脚踝旋转，父=足ＩＫ
        b = eb.new(f'つま先ＩＫ.{side}')
        b.head = toe.head.copy()
        b.tail = (toe.head.x, toe.head.y, toe.head.z - 0.05)
        b.parent = eb.get(f'足ＩＫ.{side}')
        b.use_connect = False
        b.use_deform = False

        print(f'  ✅ {side}侧脚部IK骨骼完成')

    bpy.ops.object.mode_set(mode='OBJECT')
    print('\n✅ 脚部IK骨骼添加完成！')

add_ik_bones()
