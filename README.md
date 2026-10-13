# 迷宫老鼠寻路游戏 — 软件测试项目

> 基于 Python/Pygame 迷宫游戏的完整测试实践：测试计划 → 用例设计 → 功能测试与缺陷管理 → pytest 单元测试 → UI 冒烟自动化 → 测试总结，全流程独立完成。

## 项目简介

被测对象是课程设计作品《迷宫老鼠寻路游戏》（`mice.py`，479 行）：玩家用方向键控制像素老鼠，在 15×15 迷宫中于 60 秒内到达右下角粮仓；支持迷宫编辑、pickle 存读档、DFS 全路径与 BFS 最短路径显示。

本项目将该作业作为被测系统，按企业级测试流程完成了一次完整的测试实践，**共发现 10 个真实缺陷**（含 1 个严重游戏平衡漏洞和 1 个 pickle 反序列化安全隐患），并建立了 **100% 分支覆盖率**的可回归自动化测试集。

![正常对局：开启路径显示](screenshots/README_正常对局_路径显示.png)

## 仓库结构

```
little_mice/
├── mice.py                    # 被测程序（含可测性重构：抽取 handle_event/check_timeout）
├── requirements.txt           # 依赖清单（游戏 + 测试）
├── pytest.ini                 # 固化 pytest 运行参数与报告输出路径
├── tests/                     # pytest 自动化测试（86 条）
│   ├── conftest.py            # SDL dummy headless 设置
│   ├── test_move.py           # 移动/碰撞/越界/胜利判定
│   ├── test_paths.py          # BFS/DFS 算法（双实现校验）
│   ├── test_save_load.py      # 存读档 + 异常/篡改文件（xfail 缺陷固化）
│   ├── test_edit.py           # 迷宫编辑与保护规则
│   ├── test_events.py         # 事件判定表 + 超时边界（monkeypatch 模拟时钟）
│   ├── test_render.py         # headless 渲染 + 像素级断言
│   └── test_smoke.py          # 冒烟：通关链路/超时链路/完整玩家旅程
├── tools/
│   └── capture_bug_screenshots.py  # 无头复现缺陷场景，批量生成截图/证据文件
├── screenshots/               # 缺陷取证截图与实测数据（Bug 报告"截图取证"列引用）
├── docs/
│   ├── 01_测试计划.xlsx        # 范围/策略/环境/准入准出/风险
│   ├── 02_测试用例.xlsx        # 60 条用例 + 判定表 + 边界值分析（含执行结果回填）
│   ├── 03_Bug报告.xlsx         # 10 个缺陷：复现步骤/代码定位/修复建议/统计图
│   ├── 04_测试报告.xlsx        # 执行统计/缺陷汇总/自动化资产/结论与遗留风险
│   ├── 简历项目描述与面试准备.md
│   └── reports/               # pytest HTML 报告 + 覆盖率 HTML 报告
└── 广东医科大学-数据结构课程设计报告-….doc   # 原始需求（测试的需求基准）
```

## 测试成果一览

| 指标     | 结果                                              |
| ------ | ----------------------------------------------- |
| 黑盒测试用例 | 60 条（等价类/边界值/判定表/场景法/错误推测），执行率 100%             |
| 用例通过率  | 83.3%（失败 10 条全部与缺陷关联）                           |
| 缺陷     | 10 个（严重 1 / 一般 6 / 轻微 2 / 安全 1），全部定位到代码行并给出修复建议 |
| 自动化用例  | 86 条（84 通过 + 2 条 xfail 缺陷固化），**语句/分支覆盖率 100%**  |
| 冒烟自动化  | 5 条核心链路：事件注入沿 BFS 最短路径通关、超时判负、完整玩家旅程            |
|        |                                                 |

### 代表性缺陷

- **BUG-01（严重）**：L 键读档会重置 60 秒倒计时 → 玩家可无限"读档复活"规避超时失败，`mice.py:404`
- **BUG-08（一般）**：`load_maze` 无结构校验 → 非法存档"加载成功"后崩溃，且 pickle 反序列化存在**任意代码执行**风险（BUG-09）
- **BUG-05（一般）**：主循环渲染代码重复两次，实际帧率减半
- 完整清单见 [docs/03_Bug报告.xlsx](docs/03_Bug报告.xlsx)

## 运行与测试

```bash
# 安装依赖（游戏 + 测试）
pip install -r requirements.txt

# 运行游戏（需要本地显示环境）
python mice.py

# 运行全部自动化测试：pytest.ini 已固化参数，
# 自动执行覆盖率统计并将 HTML 报告输出到 docs/reports/（headless，无显示环境/CI 均可）
python -m pytest

# 仅运行冒烟链路
python -m pytest tests/test_smoke.py -v

# 重新生成缺陷取证截图/数据（无头，约 1.5 分钟，含两项性能实测）
python tools/capture_bug_screenshots.py
```

## 技术要点

1. **可测性重构**：将 `main()` 中的事件处理与超时判定原样抽取为 `MazeGame.handle_event()` / `check_timeout()`，行为不变（headless 冒烟验证），使 UI 逻辑可被事件注入全自动化驱动。
2. **Headless 测试**：`SDL_VIDEODRIVER=dummy` 解决模块级 `pygame.init()/set_mode()` 对显示环境的依赖，CI 可跑。
3. **像素级 UI 断言**：在 dummy 驱动下真实执行绘制逻辑，用 `surface.get_at()` 验证墙/路/奶酪/老鼠/路径线的颜色。
4. **时间边界控制**：`monkeypatch` 替换 `time.time`，精确覆盖 60/60+ε 秒超时边界与编辑暂停逻辑。
5. **缺陷固化**：未修复缺陷用 `pytest.mark.xfail` 登记，修复后自动转通过，形成回归保护。
6. **测试预言**：BFS 算法用独立参考实现做双实现步数校验，避免"自己测自己"。

## 测试结论

有条件通过：核心玩法功能正确；建议优先修复 BUG-01（计时漏洞）、BUG-08（存档校验）、BUG-09（pickle 安全，建议改 JSON）后发布。详细分析见 [docs/04_测试报告.xlsx](docs/04_测试报告.xlsx)。
