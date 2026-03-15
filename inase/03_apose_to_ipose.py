# ============================================================
# 03_apose_to_ipose.py
# T-Pose → MMD I-Pose 手臂姿态修正
# 原理：
#   1. Pose Mode 旋转上臂使其下倾25°（对照MMD参考模型测量）
#   2. 肘部反向补偿，保持前臂相对方向不变
#   3. Apply Pose as Rest Pose 烘焙成新 rest pose
# ============================================================
import bpy, math

def apose_to_ipose(armature_name='Armature'):
    arm = bpy.data.objects.get(armature_name)
    if not arm:
        print(f"[错误] 找不到骨骼: {armature_name}")
        return

    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='POSE')

    # 重置所有姿态
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.rot_clear()
    bpy.ops.pose.loc_clear()

    ARM_ANGLE = math.radians(25)  # 上臂下倾角度，对照MMD参考模型

    for side, sign in [('L', -1), ('R', 1)]:
        # 上臂下倾
        pb = arm.pose.bones.get(f'腕.{side}')
        if pb:
            pb.rotation_mode = 'XYZ'
            pb.rotation_euler[2] = sign * ARM_ANGLE
            print(f"  腕.{side}: Z旋转 {math.degrees(sign * ARM_ANGLE):.1f}°")

        # 肘部反向补偿
        pb = arm.pose.bones.get(f'ひじ.{side}')
        if pb:
            pb.rotation_mode = 'XYZ'
            pb.rotation_euler[2] = -sign * ARM_ANGLE

    bpy.context.view_layer.update()

    # Apply Pose as Rest Pose
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.armature_apply(selected=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    print("\n✅ T-Pose → I-Pose 完成！手臂姿态已烘焙为 rest pose")

apose_to_ipose('Armature')
