# ============================================================
# verify_bones.py  —  验证核心 MMD 骨骼是否都存在
# ============================================================
import bpy

def verify(armature_name='Armature'):
    arm = bpy.data.objects.get(armature_name)
    bones = {b.name for b in arm.data.bones}
    check = [
        '全ての親','センター','下半身','上半身','上半身2','首','頭',
        '目.L','目.R',
        '足.L','ひざ.L','足首.L','つま先.L',
        '足.R','ひざ.R','足首.R','つま先.R',
        '肩.L','腕.L','ひじ.L','手首.L',
        '肩.R','腕.R','ひじ.R','手首.R',
        '親指０.L','人指１.L','中指１.L','薬指１.L','小指１.L',
        '親指０.R','人指１.R','中指１.R','薬指１.R','小指１.R',
    ]
    all_ok = True
    for b in check:
        ok = b in bones
        print(f"  {'✅' if ok else '❌'} {b}")
        if not ok: all_ok = False
    print(f"\n{'✅ 全部通过！' if all_ok else '❌ 有骨骼缺失'}")

verify('Armature')
