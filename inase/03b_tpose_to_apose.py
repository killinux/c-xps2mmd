# ============================================================
# 03b_tpose_to_apose.py
# T-Pose → A-Pose 转换（正确版）
#
# 关键点：必须同时处理骨骼和网格，缺一不可：
#   1. Pose Mode 设置手臂旋转
#   2. 对每个网格 Apply Armature Modifier（把形变烘焙进顶点）
#   3. 重新给每个网格绑定 Armature Modifier
#   4. Apply Pose as Rest Pose（固定骨骼 rest pose）
#
# 特别说明：此模型 肩.L/R 骨骼朝向为 Y 轴，
#           绕 X 轴旋转才能让手臂上下移动
#           左臂 X 轴 -1（向下），右臂 X 轴 +1（向下）
# ============================================================
import bpy, math

def tpose_to_apose(armature_name='Armature'):
    arm = bpy.data.objects.get(armature_name)
    if not arm:
        print(f"[错误] 找不到骨骼: {armature_name}")
        return

    # Step 1: Pose Mode 设置 A-Pose 旋转
    bpy.ops.object.select_all(action='DESELECT')
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.rot_clear()
    bpy.ops.pose.loc_clear()

    A_ANGLE = math.radians(45)
    for side, sign in [('L', -1), ('R', 1)]:
        pb = arm.pose.bones.get(f'肩.{side}')
        if pb:
            pb.rotation_mode = 'XYZ'
            pb.rotation_euler[0] = sign * A_ANGLE
            print(f"  肩.{side}: X旋转 {math.degrees(sign * A_ANGLE):.1f}°")

    bpy.context.view_layer.update()
    bpy.ops.object.mode_set(mode='OBJECT')

    # Step 2: 对每个网格 Apply Armature Modifier + 重新绑定
    meshes = [o for o in bpy.data.objects
              if o.type == 'MESH' and o.find_armature()
              and o.find_armature().name == armature_name]

    print(f"\n处理 {len(meshes)} 个网格...")
    for obj in meshes:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # 找 Armature modifier
        arm_mod = next((m for m in obj.modifiers if m.type == 'ARMATURE'), None)
        if arm_mod:
            bpy.ops.object.modifier_apply(modifier=arm_mod.name)

        # 重新添加 Armature modifier
        new_mod = obj.modifiers.new(name='Armature', type='ARMATURE')
        new_mod.object = arm
        print(f"  ✅ {obj.name}")

    # Step 3: Apply Pose as Rest Pose
    bpy.ops.object.select_all(action='DESELECT')
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.armature_apply(selected=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    # 验证
    shoulder = arm.data.bones.get('肩.L')
    wrist    = arm.data.bones.get('手首.L')
    if shoulder and wrist:
        dz = shoulder.head_local.z - wrist.head_local.z
        print(f"\n  骨骼下倾量: {dz:.3f} {'✅' if dz > 0.1 else '❌'}")

    # 验证网格顶点
    obj = bpy.data.objects.get('24_Object003_1_16_16')
    if obj:
        vg = obj.vertex_groups.get('腕.L')
        if vg:
            verts_z = []
            for v in obj.data.vertices:
                for g in v.groups:
                    if g.group == vg.index and g.weight > 0.5:
                        verts_z.append(v.co.z)
            if verts_z:
                avg_z = sum(verts_z) / len(verts_z)
                print(f"  网格顶点平均Z: {avg_z:.3f} {'✅' if avg_z < 1.35 else '❌ 网格未更新'}")

    print("\n✅ T-Pose → A-Pose 完成！")

tpose_to_apose('Armature')
