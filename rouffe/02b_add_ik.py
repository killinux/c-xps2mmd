# ============================================================
# 02b_add_ik.py  —  添加脚部 IK 骨骼、约束和 Pole Target
# ============================================================
import bpy, math

XPS_ARMATURE = 'Armature'

def add_ik_bones():
    arm = bpy.data.objects.get(XPS_ARMATURE)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='EDIT')
    eb = arm.data.edit_bones

    for side in ['L', 'R']:
        ankle = eb.get(f'足首.{side}')
        toe   = eb.get(f'つま先.{side}')
        knee  = eb.get(f'ひざ.{side}')
        root  = eb.get('全ての親')

        # 足IK親
        b = eb.new(f'足IK親.{side}')
        b.head = (ankle.head.x, ankle.head.y, 0.0)
        b.tail = (ankle.head.x, ankle.head.y, ankle.head.z)
        b.parent = root
        b.use_deform = False

        # 足ＩＫ
        b = eb.new(f'足ＩＫ.{side}')
        b.head = (ankle.head.x, ankle.head.y, ankle.head.z)
        b.tail = (ankle.head.x, ankle.head.y + 0.1, ankle.head.z)
        b.parent = eb.get(f'足IK親.{side}')
        b.use_deform = False

        # つま先ＩＫ
        b = eb.new(f'つま先ＩＫ.{side}')
        b.head = (toe.head.x, toe.head.y, toe.head.z)
        b.tail = (toe.head.x, toe.head.y, toe.head.z - 0.05)
        b.parent = eb.get(f'足ＩＫ.{side}')
        b.use_deform = False

        # Pole Target：膝盖正前方（-Y方向）
        b = eb.new(f'ひざPole.{side}')
        b.head = (knee.head.x, knee.head.y - 0.3, knee.head.z)
        b.tail = (knee.head.x, knee.head.y - 0.4, knee.head.z)
        b.parent = root
        b.use_deform = False

        print(f"  ✅ {side} 脚 IK 骨骼已添加")

    bpy.ops.object.mode_set(mode='OBJECT')

def add_ik_constraints():
    arm = bpy.data.objects.get(XPS_ARMATURE)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='POSE')

    for side in ['L', 'R']:
        # ひざ：IK + Pole Target + 旋转限制
        pb = arm.pose.bones.get(f'ひざ.{side}')
        c = pb.constraints.new('IK')
        c.target        = arm
        c.subtarget     = f'足ＩＫ.{side}'
        c.pole_target   = arm
        c.pole_subtarget = f'ひざPole.{side}'
        c.pole_angle    = math.radians(90)   # 膝盖朝前（-Y方向）
        c.chain_count   = 2
        c.use_stretch   = False

        lim = pb.constraints.new('LIMIT_ROTATION')
        lim.use_limit_x = True
        lim.min_x       = 0
        lim.max_x       = math.radians(180)
        lim.owner_space = 'LOCAL'

        # 足首：IK chain=1
        pb = arm.pose.bones.get(f'足首.{side}')
        c = pb.constraints.new('IK')
        c.target      = arm
        c.subtarget   = f'つま先ＩＫ.{side}'
        c.chain_count = 1
        c.use_stretch = False

        print(f"  ✅ {side} 脚 IK 约束 + Pole Target 已添加")

    bpy.ops.object.mode_set(mode='OBJECT')

add_ik_bones()
add_ik_constraints()
print("\n✅ 脚部 IK 完成！")
