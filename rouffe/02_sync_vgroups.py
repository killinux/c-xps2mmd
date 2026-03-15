# ============================================================
# 02_sync_vgroups.py  —  顶点组补全 + 权重修复
#
# 关键修复：
# 1. XPS 大腿骨骼(足.L/R)的权重覆盖了整条腿，需要把膝盖以下的
#    权重转移到 ひざ.L/R，否则旋转膝盖时大腿也会跟着动
# 2. 手臂骨骼从手腕补全
# ============================================================
import bpy

XPS_ARMATURE = 'Armature'

def copy_vgroup(obj, src_name, dst_name):
    src = obj.vertex_groups.get(src_name)
    if not src:
        return False
    if not obj.vertex_groups.get(dst_name):
        obj.vertex_groups.new(name=dst_name)
    dst = obj.vertex_groups[dst_name]
    for v in obj.data.vertices:
        try:
            w = src.weight(v.index)
            dst.add([v.index], w, "REPLACE")
        except RuntimeError:
            pass
    return True


def clean_hip_overflow(obj, thigh_name, thigh_head_z):
    """移除大腿骨骼在腰部以上的异常权重（Z > 大腿head Z）"""
    vg = obj.vertex_groups.get(thigh_name)
    if not vg:
        return 0
    bad = [v.index for v in obj.data.vertices
           for g in v.groups if g.group == vg.index and g.weight > 0.01 and v.co.z > thigh_head_z]
    if bad:
        vg.remove(bad)
    return len(bad)

def fix_leg_weights(obj, thigh_name, knee_name, knee_z):
    """把大腿骨骼中膝盖以下的权重转移到膝盖骨骼"""
    vg_thigh = obj.vertex_groups.get(thigh_name)
    if not vg_thigh:
        return 0
    vg_knee = obj.vertex_groups.get(knee_name)
    if not vg_knee:
        vg_knee = obj.vertex_groups.new(name=knee_name)
    
    move = []
    for v in obj.data.vertices:
        for g in v.groups:
            if g.group == vg_thigh.index and g.weight > 0.01 and v.co.z < knee_z:
                move.append((v.index, g.weight))
    
    if move:
        vg_thigh.remove([idx for idx, w in move])
        for idx, w in move:
            vg_knee.add([idx], w, "REPLACE")
    return len(move)

def 
def fix_hip_region(arm, meshes):
    """
    修复腰部/屁股区域的权重问题：
    1. 大腿骨骼(足.L/R)在大腿head以上的权重转给下半身
    2. 裙子/装饰骨骼在腰部区域的权重转给下半身  
    3. 腰部区域没有躯干骨骼权重的顶点补充下半身权重
    """
    TRUNK = {"下半身", "上半身", "センター", "unused trash 17"}
    Z_LO, Z_HI = 0.88, 1.10

    thigh_z_r = arm.data.bones.get("足.R").head_local.z
    thigh_z_l = arm.data.bones.get("足.L").head_local.z

    total = 0
    for obj in meshes:
        vg_lower = obj.vertex_groups.get("下半身")
        if not vg_lower:
            continue

        # 1. 大腿以上的足.L/R权重转给下半身
        for bname, tz in [("足.R", thigh_z_r), ("足.L", thigh_z_l)]:
            vg_t = obj.vertex_groups.get(bname)
            if not vg_t: continue
            bad = [(v.index, vg_t.weight(v.index)) for v in obj.data.vertices
                   for g in v.groups if g.group == vg_t.index and g.weight > 0.01 and v.co.z > tz]
            if bad:
                vg_t.remove([i for i,w in bad])
                for i, w in bad:
                    lw = 0
                    for g in obj.data.vertices[i].groups:
                        if g.group == vg_lower.index: lw = g.weight
                    vg_lower.add([i], lw + w, "REPLACE")

        # 2. 补充腰部无躯干权重的顶点
        for v in obj.data.vertices:
            if not (Z_LO < v.co.z < Z_HI):
                continue
            total_w = trunk_w = 0
            for g in v.groups:
                bn = obj.vertex_groups[g.group].name
                if g.weight > 0.001:
                    total_w += g.weight
                    if bn in TRUNK: trunk_w += g.weight
            needed = max(0, 1.0 - total_w)
            if needed > 0.01 or (total_w > 0.01 and trunk_w < 0.1):
                cur_lw = 0
                for g in v.groups:
                    if g.group == vg_lower.index: cur_lw = g.weight
                new_lw = min(cur_lw + max(needed, 0.5 - trunk_w), 1.0)
                if new_lw > cur_lw + 0.01:
                    vg_lower.add([v.index], new_lw, "REPLACE")
                    total += 1

    print(f"  fix_hip_region: 共修复 {total} 个腰部顶点")


sync_vgroups()

# 修复屁股/腰部区域权重
arm = bpy.data.objects.get(XPS_ARMATURE)
meshes = [o for o in bpy.data.objects if o.type == "MESH" and any(m.type == "ARMATURE" and m.object == arm for m in o.modifiers)]
fix_hip_region(arm, meshes):
    arm = bpy.data.objects.get(XPS_ARMATURE)
    meshes = [o for o in bpy.data.objects if o.type == "MESH"
              and any(m.type == "ARMATURE" and m.object == arm for m in o.modifiers)]

    # 膝盖骨骼的 Z 位置（从骨骼 rest pose 读取）
    knee_z_l = arm.data.bones.get("ひざ.L").head_local.z if arm.data.bones.get("ひざ.L") else 0.556
    knee_z_r = arm.data.bones.get("ひざ.R").head_local.z if arm.data.bones.get("ひざ.R") else 0.556

    fixed = transferred = 0
    for obj in meshes:
        vg = {v.name for v in obj.vertex_groups}

        # 关键修复：把大腿骨骼中膝盖以下的权重转移到膝盖骨骼
        transferred += fix_leg_weights(obj, "足.L", "ひざ.L", knee_z_l)
        transferred += fix_leg_weights(obj, "足.R", "ひざ.R", knee_z_r)
        # 清除大腿骨骼在腰部以上的异常权重
        thigh_z_l = arm.data.bones.get("足.L").head_local.z
        thigh_z_r = arm.data.bones.get("足.R").head_local.z
        clean_hip_overflow(obj, "足.L", thigh_z_l)
        clean_hip_overflow(obj, "足.R", thigh_z_r)

        # 手臂补全：从手腕复制权重
        if "手首.L" in vg and "ひじ.L" not in vg: copy_vgroup(obj,"手首.L","ひじ.L"); fixed+=1
        if "手首.R" in vg and "ひじ.R" not in vg: copy_vgroup(obj,"手首.R","ひじ.R"); fixed+=1
        if "手首.L" in vg and "腕.L"   not in vg: copy_vgroup(obj,"手首.L","腕.L");   fixed+=1
        if "手首.R" in vg and "腕.R"   not in vg: copy_vgroup(obj,"手首.R","腕.R");   fixed+=1
        if "手首.L" in vg and "肩.L"   not in vg: copy_vgroup(obj,"手首.L","肩.L");   fixed+=1
        if "手首.R" in vg and "肩.R"   not in vg: copy_vgroup(obj,"手首.R","肩.R");   fixed+=1
        if "首" in vg and "頭" not in vg: copy_vgroup(obj,"首","頭"); fixed+=1

    print(f"✅ 腿部权重转移: {transferred}个顶点  手臂补全: {fixed}个")


def fix_hip_region(arm, meshes):
    """
    修复腰部/屁股区域的权重问题：
    1. 大腿骨骼(足.L/R)在大腿head以上的权重转给下半身
    2. 裙子/装饰骨骼在腰部区域的权重转给下半身  
    3. 腰部区域没有躯干骨骼权重的顶点补充下半身权重
    """
    TRUNK = {"下半身", "上半身", "センター", "unused trash 17"}
    Z_LO, Z_HI = 0.88, 1.10

    thigh_z_r = arm.data.bones.get("足.R").head_local.z
    thigh_z_l = arm.data.bones.get("足.L").head_local.z

    total = 0
    for obj in meshes:
        vg_lower = obj.vertex_groups.get("下半身")
        if not vg_lower:
            continue

        # 1. 大腿以上的足.L/R权重转给下半身
        for bname, tz in [("足.R", thigh_z_r), ("足.L", thigh_z_l)]:
            vg_t = obj.vertex_groups.get(bname)
            if not vg_t: continue
            bad = [(v.index, vg_t.weight(v.index)) for v in obj.data.vertices
                   for g in v.groups if g.group == vg_t.index and g.weight > 0.01 and v.co.z > tz]
            if bad:
                vg_t.remove([i for i,w in bad])
                for i, w in bad:
                    lw = 0
                    for g in obj.data.vertices[i].groups:
                        if g.group == vg_lower.index: lw = g.weight
                    vg_lower.add([i], lw + w, "REPLACE")

        # 2. 补充腰部无躯干权重的顶点
        for v in obj.data.vertices:
            if not (Z_LO < v.co.z < Z_HI):
                continue
            total_w = trunk_w = 0
            for g in v.groups:
                bn = obj.vertex_groups[g.group].name
                if g.weight > 0.001:
                    total_w += g.weight
                    if bn in TRUNK: trunk_w += g.weight
            needed = max(0, 1.0 - total_w)
            if needed > 0.01 or (total_w > 0.01 and trunk_w < 0.1):
                cur_lw = 0
                for g in v.groups:
                    if g.group == vg_lower.index: cur_lw = g.weight
                new_lw = min(cur_lw + max(needed, 0.5 - trunk_w), 1.0)
                if new_lw > cur_lw + 0.01:
                    vg_lower.add([v.index], new_lw, "REPLACE")
                    total += 1

    print(f"  fix_hip_region: 共修复 {total} 个腰部顶点")


sync_vgroups()

# 修复屁股/腰部区域权重
arm = bpy.data.objects.get(XPS_ARMATURE)
meshes = [o for o in bpy.data.objects if o.type == "MESH" and any(m.type == "ARMATURE" and m.object == arm for m in o.modifiers)]
fix_hip_region(arm, meshes)
