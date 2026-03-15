# ============================================================
# 03b_tpose_to_apose.py （最终正确版）
#
# 正确流程：
#   1. Pose Mode 用 matrix 方式旋转肩部骨骼（网格跟着视觉上动）
#   2. 退出 Pose Mode
#   3. 对每个网格 Apply Armature Modifier（固化当前 A-Pose 顶点）
#   4. 重新绑定 Armature Modifier
#   5. Apply Pose as Rest Pose（固化骨骼）
#
# 关键点：步骤3必须在有 Pose 旋转的状态下执行，
#         此时网格在视觉上已经是 A-Pose，Apply 才能固化正确位置
# ============================================================
import bpy, math, mathutils

XPS_ARMATURE = 'Armature'

def tpose_to_apose():
    xps_arm = bpy.data.objects.get(XPS_ARMATURE)
    if not xps_arm:
        print(f"[错误] 找不到骨骼: {XPS_ARMATURE}")
        return

    # Step 1: Pose Mode 设置旋转
    bpy.context.view_layer.objects.active = xps_arm
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.rot_clear()
    bpy.ops.pose.loc_clear()

    ANGLE = math.radians(25)  # 手臂下倾角度

    def rotate_global_y(bone_name, angle):
        pb = xps_arm.pose.bones.get(bone_name)
        if not pb:
            print(f"  [跳过] {bone_name}")
            return
        rot = mathutils.Quaternion((0, 1, 0), angle)
        pb.matrix = rot.to_matrix().to_4x4() @ pb.bone.matrix_local.to_4x4()
        print(f"  {bone_name}: 绕全局Y轴 {math.degrees(angle):.1f}°")

    rotate_global_y('arm left shoulder 1',   ANGLE)
    rotate_global_y('arm right shoulder 1', -ANGLE)
    bpy.context.view_layer.update()

    # 验证旋转是否生效
    pb_wr = xps_arm.pose.bones.get('arm left wrist')
    pb_sh = xps_arm.pose.bones.get('arm left shoulder 1')
    wz = (xps_arm.matrix_world @ pb_wr.head).z
    sz = (xps_arm.matrix_world @ pb_sh.head).z
    print(f"  手臂下倾: {sz-wz:.3f}  {'✅' if sz-wz > 0.1 else '❌'}")

    # Step 2: 退出 Pose Mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Step 3 & 4: 对每个网格 Apply + 重新绑定
    meshes = [o for o in bpy.data.objects if o.type == 'MESH'
              and any(m.type == 'ARMATURE' and m.object == xps_arm for m in o.modifiers)]

    print(f"\n处理 {len(meshes)} 个网格...")
    for obj in meshes:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        arm_mod = next((m for m in obj.modifiers if m.type == 'ARMATURE'), None)
        if arm_mod:
            bpy.ops.object.modifier_apply(modifier=arm_mod.name)
        new_mod = obj.modifiers.new(name='Armature', type='ARMATURE')
        new_mod.object = xps_arm
        print(f"  ✅ {obj.name}")

    # Step 5: Apply Pose as Rest Pose
    bpy.ops.object.select_all(action='DESELECT')
    xps_arm.select_set(True)
    bpy.context.view_layer.objects.active = xps_arm
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.armature_apply(selected=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    # 最终验证
    b_sh = xps_arm.data.bones.get('arm left shoulder 1')
    b_wr = xps_arm.data.bones.get('arm left wrist')
    dz = b_sh.head_local.z - b_wr.head_local.z
    print(f"\n✅ A-Pose 完成！骨骼下倾量: {dz:.3f}")

tpose_to_apose()
