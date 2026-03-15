# ============================================================
# SESSION_SUMMARY.md
# XPS → MMD 转换项目进度总结
# 最后更新：2026-03-15
# ============================================================

## 项目信息

- 模型：Rouffe Tigerstripe 18
- XPS 骨骼对象名：Armature（195根）
- MMD 参考模型：Rouffe Tigerstripe 18_arm（261根）
- 工作目录：~/Downloads/mywork/xps2mmd_work/c-xps2mmd/rouffe/
- Blender 文件：~/Downloads/mywork/xps2mmd_work/output/riseofeor inase/inase.blend

---

## 下次从这里开始

**当前进度：骨骼阶段已完成，下一步是 Step 2 权重处理**

运行检查脚本确认骨骼状态：
```
check_bones.py  →  应该全部显示 ✅，65根全部通过
```

然后继续做：
1. 手臂捩り骨骼（腕捩/手捩）—— 还没做
2. 物理D骨骼（ひざD/足D/足首D）—— 还没做  
3. Step 2：权重处理（02_sync_vgroups.py）—— 还没做
4. Step 3：T→A Pose（03b_tpose_to_apose.py）—— 还没做
5. 材质转换 —— 还没做
6. 导出 PMX —— 还没做

---

## 已完成的脚本

| 脚本 | 功能 | 状态 |
|------|------|------|
| 01_rename_bones.py | XPS英文骨骼名→MMD日文名（89根） | ✅ 完成 |
| 01b_add_torso_bones.py | 添加腰/上半身1，修正躯干父子关系 | ✅ 完成 |
| 01c_add_shoulder_bones.py | 添加肩P/肩C，修正肩臂父子关系 | ✅ 完成 |
| 01d_add_ik_bones.py | 添加脚部IK（足IK親/足ＩＫ/つま先ＩＫ） | ✅ 完成 |
| check_bones.py | 骨骼完整性检查（随时运行） | ✅ 工具 |
| 02_sync_vgroups.py | 权重补全和修复 | ⚠️ 待验证 |
| 03b_tpose_to_apose.py | T-Pose → A-Pose | ⚠️ 待重做 |

---

## 骨骼检查结果（check_bones.py）

最后一次运行结果：65根全部通过
- Phase 1 根/重心/躯干：✅ 9根
- Phase 2 腿部：✅ 8根
- Phase 3 脚部IK：✅ 6根
- Phase 4 肩/臂：✅ 12根
- Phase 5 手指：✅ 30根

---

## 还缺哪些骨骼（check_bones 未覆盖）

以下骨骼还没添加，下次继续：

### 手臂捩り（16根）—— 优先级高，影响手臂动作
- 腕捩.L/R, 腕捩1.L/R, 腕捩2.L/R, 腕捩3.L/R
- 手捩.L/R, 手捩1.L/R, 手捩2.L/R, 手捩3.L/R
- parent：腕捩→腕.L/R，手捩→ひじ.L/R

### 物理D骨骼（8根）—— 物理模拟用，可以最后加
- ひざD.L/R, 足D.L/R, 足首D.L/R, 足先EX.L/R

### 眼睛/手部辅助（3根）
- 両目（parent=頭）
- ダミー.L/R（parent=手首.L/R）

---

## 重要经验教训

### 骨骼操作
1. **每步操作后立刻跑 check_bones.py**，不要等到最后
2. **肩C的 tail 方向**要朝外侧（横向），不能朝 +Z，
   否则腕骨骼会自动接到 tail 上导致位置偏移
3. **添加辅助骨骼时必须设 use_connect=False**，
   防止 Blender 自动吸附子骨骼
4. **父子关系修正顺序**：先添加中间骨骼，再修正两端的父子关系
5. **XPS 常见父子关系问题**：
   - 下半身/上半身 parent 是 unused trash 17 → 应改为 腰
   - 上半身2 parent 是 上半身 → 应改为 上半身1
   - 肩.L/R parent 是 上半身2 → 应改为 肩P.L/R
   - 腕.L/R parent 是 肩.L/R → 应改为 肩C.L/R

### 权重操作（02_sync_vgroups.py 的教训）
6. **不要从大腿复制权重给膝盖**（100%重叠会互相抵消）
   正确做法：把大腿中膝盖以下的顶点权重转移给膝盖
7. **大腿权重不能超过大腿head的Z坐标**
   超出部分转移给下半身
8. **腰部区域检查**：Z=0.88~1.10 的顶点必须有躯干骨骼权重

### IK 操作
9. **膝盖骨骼 head 必须在大腿-脚踝连线的前方（-Y偏移）**
   否则 IK 会选择向后弯的解
10. **Pole Target 必须绑在全ての親**（不能绑在大腿），
    否则左右不对称

---

## 运行顺序（下次重新导入XPS时）

```
1. 导入 XPS 模型（骨骼对象名保持 Armature）
2. 01_rename_bones.py         → 骨骼重命名
3. 01b_add_torso_bones.py     → 添加躯干骨骼
4. 01c_add_shoulder_bones.py  → 添加肩部骨骼
5. 01d_add_ik_bones.py        → 添加脚部IK
6. check_bones.py             → 验证（应全部✅）
7. （下次）添加捩り骨骼
8. （下次）02_sync_vgroups.py → 权重处理
9. （下次）03b_tpose_to_apose.py → A-Pose
10.（下次）材质转换
11.（下次）导出 PMX
```
