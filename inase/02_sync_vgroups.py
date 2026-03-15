# ============================================================
# 02_sync_vgroups.py
# 顶点组同步 —— 补全缺失的核心顶点组
# 说明：Blender 骨骼重命名时会自动同步顶点组名
#       但部分网格原本就缺少某些骨骼的绑定，需要从相邻骨骼复制权重补全
# ============================================================
import bpy

def copy_vgroup(obj, src, dst):
    """从 src 顶点组复制权重到 dst"""
    if not obj.vertex_groups.get(src):
        print(f"  [跳过] {obj.name} 没有顶点组 '{src}'")
        return False
    if not obj.vertex_groups.get(dst):
        obj.vertex_groups.new(name=dst)
    src_vg = obj.vertex_groups[src]
    dst_vg = obj.vertex_groups[dst]
    for v in obj.data.vertices:
        try:
            w = src_vg.weight(v.index)
            dst_vg.add([v.index], w, 'REPLACE')
        except RuntimeError:
            pass
    print(f"  ✅ {obj.name}: '{src}' → '{dst}'")
    return True

def sync_vgroups():
    # 找所有绑定到 Armature 的网格
    arm = bpy.data.objects.get('Armature')
    if not arm:
        print("[错误] 找不到 Armature")
        return

    mmd_bone_names = {b.name for b in arm.data.bones}

    meshes = [obj for obj in bpy.data.objects
              if obj.type == 'MESH' and obj.find_armature()
              and obj.find_armature().name == 'Armature']

    print(f"共找到 {len(meshes)} 个网格")

    for obj in meshes:
        vg_names = {vg.name for vg in obj.vertex_groups}

        # ひざ(膝盖) 缺失时从 足(大腿) 复制
        if '足.L' in vg_names and 'ひざ.L' not in vg_names:
            copy_vgroup(obj, '足.L', 'ひざ.L')
        if '足.R' in vg_names and 'ひざ.R' not in vg_names:
            copy_vgroup(obj, '足.R', 'ひざ.R')

        # ひじ(肘) 缺失时从 腕(上臂) 复制
        if '腕.L' in vg_names and 'ひじ.L' not in vg_names:
            copy_vgroup(obj, '腕.L', 'ひじ.L')
        if '腕.R' in vg_names and 'ひじ.R' not in vg_names:
            copy_vgroup(obj, '腕.R', 'ひじ.R')

        # 頭 缺失时从 首 复制
        if '首' in vg_names and '頭' not in vg_names:
            copy_vgroup(obj, '首', '頭')

    print("\n顶点组同步完成！")

sync_vgroups()
