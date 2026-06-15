## Summary

目标是评估是否能把当前 `py-tuto-4-java-guy` 改造成接近 `learning-cxx` 的学习交互方式，并重点满足两项目标：

- 每个小题都有唯一 ID，方便练习时讨论、定位和验收。
- 支持批量验证并输出清晰的单机进度对比结果。

结论：**可以施行，且与当前仓库结构较为兼容；但建议做“Python 原生等价交互”，而不是机械照搬 `xmake run learn <id>`。** 当前仓库已经具备按模块运行、按全部模块汇总的雏形，主要缺失的是“小题级元数据”和“统一汇总视图”。

## Status

- 状态：**已完成**
- 完成时间：2026-06-16
- 完成结果：
  - 已新增根目录题号注册表 `scripts/exercise_registry.py`
  - 已新增根目录命令 `learn` 与 `summary`
  - 已在 `pyproject.toml` 注册 `test-all` / `learn` / `summary` 入口
  - 已更新 `README.md`，将根目录题号学习与进度汇总写为推荐主路径
  - 已保留模块内兼容路径 `python run_test.py initial|complete|diff`
  - 已补充 `scripts/__init__.py` 与 setuptools 打包声明，确保 console script 可正确导入 `scripts.*`

## Completion Notes

- 本次实现相对原计划有两处必要补充：
  - 新增 `scripts/__init__.py`
  - 在 `pyproject.toml` 中新增 `build-system` 与 `[tool.setuptools] packages = ["scripts"]`
- 原因：
  - 若没有这两处补充，`learn.exe`、`summary.exe` 与 `test-all.exe` 会因 `ModuleNotFoundError: No module named 'scripts'` 无法运行。
- 该补充不改变原始目标，只是为保证计划中定义的命令入口真正可用。

## Current State Analysis

### 现有入口与能力

- `d:\ml\cc-playground\py-tuto-4-java-guy\README.md`
  - 当前文档入口是“进入某个模块目录后运行 `python run_test.py initial|complete`”。
  - “Run all tests” 只展示了按模块批量执行参考答案测试的方法。
- `d:\ml\cc-playground\py-tuto-4-java-guy\pyproject.toml`
  - 已存在统一脚本入口 `test-all = "scripts.run_all:main"`。
  - 说明项目已经接受“根目录统一命令入口”的交互模式。
- `d:\ml\cc-playground\py-tuto-4-java-guy\scripts\run_all.py`
  - 已经能扫描 `modules/*/run_test.py` 并逐模块运行 `complete`。
  - 但输出粒度只到“模块是否失败”，没有小题明细，也没有学习者视角的完成度表格。
- `d:\ml\cc-playground\py-tuto-4-java-guy\modules\01-basics-and-types\run_test.py`
  - 已具备跨平台单模块运行器。
  - 当前只支持 `initial|complete|diff`，不支持“按小题 ID 运行”。
- `d:\ml\cc-playground\py-tuto-4-java-guy\modules\01-basics-and-types\conftest.py`
  - 已通过 `PRACTICE_TARGET` 在同一份测试中切换 `initial/complete` 实现。
  - 这为后续做“同一小题在不同目标实现上复用测试”提供了稳定基础。

### 现有题目组织方式

- 每个模块目录都包含 `initial/practice.py`、`complete/practice.py`、`test_practice.py`、`run_test.py`、`tutorial.ipynb`。
- 当前仓库共有 9 个模块，测试总量 147 个 `test_...` 用例，约 45 个 `Test...` 题组。
- 从结构上看，“小题”最自然的边界不是单个断言，而是：
  - `initial/practice.py` 中的一个顶层函数或类；
  - 与之对应的 `test_practice.py` 中的一个 `Test...` 类。
- 例如：
  - `modules/01-basics-and-types/initial/practice.py` 中的 `classify_number`、`safe_divide`、`format_table` 等顶层函数，天然就是可编号的小题。
  - `modules/01-basics-and-types/test_practice.py` 中的 `TestClassifyNumber`、`TestSafeDivide` 等类，与上述小题基本一一对应。

### 与 `learning-cxx` 目标交互的差距

`learning-cxx` 的核心交互是：

- 一个统一入口命令；
- 按编号运行单个练习；
- 统一汇总所有练习状态。

当前仓库的差距主要有 4 点：

- 没有根目录级“learn”命令，用户必须先进入模块目录。
- 没有稳定的小题编号体系。
- 没有“按小题”筛选运行能力，当前只能按整个模块运行。
- 没有学习者友好的汇总视图，只有模块级失败计数。

## Proposed Changes

### 方案总原则

采用“**保留现有 pytest 体系，增加统一编排层**”的方案，而不是重写练习系统。

原因：

- 现有 `run_test.py + conftest.py + pytest` 已经稳定且跨平台。
- 题目边界已经隐含存在于 `initial/practice.py` 和 `test_practice.py` 中。
- 增量编排比重构测试体系风险小、成本低、可逐步落地。

### 需要改造的文件与方式

#### 1. `README.md`

做什么：

- 把当前“进入模块目录运行”的说明升级为“根目录统一入口”。
- 新增“按题号学习”和“汇总进度”的使用说明。

为什么：

- 这是用户感知最强的入口，当前交互方式与目标模式差异主要体现在文档层。

怎么做：

- 保留现有模块内运行方式作为底层或兼容模式。
- 新增推荐命令示例，例如未来可采用的：
  - `uv run learn M01-Q01`
  - `uv run summary`

#### 2. `pyproject.toml`

做什么：

- 新增统一 CLI 脚本入口，而不只是 `test-all`。

为什么：

- 当前项目已经通过 `[project.scripts]` 暴露命令，这是最自然的 Python 原生入口，等价于 `xmake run ...` 的“项目内统一命令体验”。

怎么做：

- 保留 `test-all`。
- 后续新增例如：
  - `learn = "scripts.learn:main"`
  - `summary = "scripts.summary:main"`

#### 3. `scripts/run_all.py`

做什么：

- **首版不修改**，继续保留为“维护者验证 `complete` 参考答案是否全部通过”的作者向命令。

为什么：

- 当前文件已经稳定承担 `test-all` 角色。
- 用户要的“学习者单题练习”和“学习进度汇总”可以通过新增根目录脚本完成，不必侵入现有参考答案验证链路。

怎么做：

- `test-all` 保持现状。
- 新的学习交互全部由新增脚本实现。

#### 4. 新增 `scripts/exercise_registry.py`

做什么：

- 新增一份**唯一题号真源**，集中声明所有小题的 ID、所属模块、符号名和 pytest 选择器。

为什么：

- 这是“讨论、验收、汇总”三件事的共同锚点。
- 用中心注册表比改 9 个模块、45 个题组测试更小、更稳，也更容易审查。

怎么做：

- 声明 `ExerciseSpec` 数据结构。
- 用 `EXERCISES` 常量显式列出全部 45 道小题。
- 根目录 `learn` 和 `summary` 命令都只依赖这份注册表。

#### 5. 新增 `scripts/learn.py`

做什么：

- 提供根目录单题运行入口，对应目标交互里的 `learn <exercise-id>`。

为什么：

- 用户无需 `cd modules/...`，可以直接在仓库根目录按题号进入练习。

怎么做：

- 解析题号。
- 从注册表查到模块目录和 pytest 节点。
- 以 `PRACTICE_TARGET=initial` 为默认目标，直接调用单题 pytest。

#### 6. 新增 `scripts/summary.py`

做什么：

- 提供根目录批量汇总入口，对应目标交互里的 `summary`。

为什么：

- 需要给学习者一个可比较的、题目级清晰进度面板。

怎么做：

- 遍历注册表里的 45 道题。
- 逐题运行对应 pytest 节点。
- 输出题目级明细和模块级汇总。

#### 7. `modules/*/run_test.py`

做什么：

- **首版不修改**。

为什么：

- 现有模块内工作流 `python run_test.py initial|complete|diff` 已可继续作为兼容路径。
- 根目录统一编排层可以直接调用 pytest 节点，不必改动每个模块的 runner。

怎么做：

- 文档中将其降级为“模块内兼容用法”，不再作为推荐主入口。

#### 8. `modules/*/test_practice.py`

做什么：

- **首版不修改**。

为什么：

- 当前 `Test...` 类命名已经足够稳定，根目录脚本可以直接通过 pytest 节点选择器命中对应题组。
- 这能避免在所有模块测试文件里大面积补 marker 或元数据。

怎么做：

- 以 `test_practice.py::TestXxx` 作为首版选择器。
- 若未来出现重命名频繁或一题多测试文件，再考虑把 ID 下沉到测试元数据。

#### 9. `modules/*/initial/practice.py` 与 `modules/*/complete/practice.py`

做什么：

- **首版不修改**。

为什么：

- 题号系统应停留在“编排与文档层”，不应侵入练习实现本身。
- 这样不会污染教学代码，也不会增加学习者理解负担。

怎么做：

- 未来如需增强 IDE 内可见性，再考虑仅补充注释，不改业务逻辑。

### 推荐的交互映射

不建议机械复刻：

- `xmake run learn <exercise number>`
- `xmake run summary`

建议改成 Python 项目更自然的等价交互：

- `uv run learn <question-id>`
- `uv run summary`

原因：

- 本项目当前构建与运行体系围绕 `uv + pyproject.toml + pytest`，不是 C/C++ 的构建型项目。
- 用 `uv run` 调用 `[project.scripts]` 能达到几乎相同的用户体验，同时不引入额外构建工具。

### 推荐的数据模型

基于你的偏好，建议采用“**现算汇总，不做本地持久化**”：

- summary 每次运行时扫描全部题目。
- 对每个小题输出：
  - 题目 ID
  - 所属模块
  - 练习符号名
  - 当前状态（`PASS` / `FAIL`）
- 最后再按模块汇总通过率，供学习者比较当前进度。

这种方式的优点：

- 无状态，不会出现进度文件与实际代码不一致。
- 多人对比时，只需比较同一版本仓库上跑出来的 summary 输出。
- 与现有测试体系兼容最好。

## Detailed Spec

### 命令契约

最终对外命令声明如下：

- `uv run learn <question-id>`
- `uv run learn <question-id> --target complete`
- `uv run summary`
- `uv run summary --target complete`

其中：

- `question-id` 采用固定格式 `Mxx-Qyy`，例如 `M01-Q01`。
- `learn` 默认面向学习者，默认 `--target initial`。
- `summary` 默认面向学习者进度统计，默认 `--target initial`。
- `--target complete` 仅作为作者/验收辅助模式，用于验证参考答案侧。

### 精确文件改动声明

#### 1. `pyproject.toml`

新增脚本声明：

```toml
[project.scripts]
test-all = "scripts.run_all:main"
learn = "scripts.learn:main"
summary = "scripts.summary:main"
```

不改动现有依赖声明，不新增第三方库。

#### 2. 新增 `scripts/exercise_registry.py`

声明如下：

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExerciseSpec:
    question_id: str
    module_id: str
    module_dir: str
    symbol_name: str
    pytest_class_name: str


EXERCISES: tuple[ExerciseSpec, ...] = (...)


def list_exercises() -> tuple[ExerciseSpec, ...]:
    ...


def get_exercise(question_id: str) -> ExerciseSpec:
    ...
```

实现约束：

- `module_dir` 使用相对仓库根目录的字符串，例如 `modules/01-basics-and-types`。
- `pytest_class_name` 使用当前测试文件中的 `Test...` 类名。
- `get_exercise()` 在未知题号时抛出 `KeyError`，由 CLI 层转成用户友好的报错。

#### 3. 新增 `scripts/learn.py`

声明如下：

```python
def main() -> int:
    ...
```

行为契约：

- 参数：
  - 位置参数 `question_id`
  - 可选参数 `--target`，取值仅允许 `initial` 或 `complete`，默认 `initial`
- 运行步骤：
  - 调用 `get_exercise(question_id)`
  - 计算 pytest 节点：`<module_dir>/test_practice.py::<pytest_class_name>`
  - 设置环境变量 `PRACTICE_TARGET=<target>`
  - 在对应 `module_dir` 下执行：

```bash
python -m pytest test_practice.py::TestXxx -v
```

- 标准输出先打印题目头：

```text
[M01-Q01] 01-basics-and-types :: classify_number
```

- 退出码直接透传 pytest 子进程退出码。

#### 4. 新增 `scripts/summary.py`

声明如下：

```python
def main() -> int:
    ...
```

行为契约：

- 参数：
  - 可选参数 `--target`，取值仅允许 `initial` 或 `complete`，默认 `initial`
- 运行步骤：
  - 遍历 `EXERCISES`
  - 对每个题目调用与 `learn` 相同的 pytest 节点执行逻辑
  - 捕获单题是否通过
- 输出分两段：
  - 题目级明细表
  - 模块级汇总表

题目级明细表列固定为：

- `Question ID`
- `Module`
- `Symbol`
- `Status`

模块级汇总表列固定为：

- `Module`
- `Passed`
- `Total`
- `Progress`

状态值只允许：

- `PASS`
- `FAIL`

退出码规则：

- 全部通过返回 `0`
- 只要存在失败，返回失败题目数

#### 5. `README.md`

文档改动精确到 3 处：

- 把“Work through a module”从主路径降级为“兼容/进阶用法”。
- 新增“Learn by question ID”章节，示例固定为：

```bash
uv run learn M01-Q01
```

- 新增“Summarize progress”章节，示例固定为：

```bash
uv run summary
```

#### 6. 不改动文件清单

首版明确**不修改**以下文件：

- `scripts/run_all.py`
- `modules/*/run_test.py`
- `modules/*/test_practice.py`
- `modules/*/initial/practice.py`
- `modules/*/complete/practice.py`

### 题号注册表精确定义

首版题号总数固定为 **45**，不是 46。

说明：

- `modules/04-interfaces-and-abstraction` 中的 `DataStore` 不单列题号。
- 原因是它没有独立 `TestDataStore` 题组，当前只作为 `DictStore` 与 `LRUStore` 的共享契约出现。

注册表应精确声明为以下 45 项：

- `M01-Q01` -> `modules/01-basics-and-types` -> `classify_number` -> `TestClassifyNumber`
- `M01-Q02` -> `modules/01-basics-and-types` -> `safe_divide` -> `TestSafeDivide`
- `M01-Q03` -> `modules/01-basics-and-types` -> `format_table` -> `TestFormatTable`
- `M01-Q04` -> `modules/01-basics-and-types` -> `is_palindrome` -> `TestIsPalindrome`
- `M01-Q05` -> `modules/01-basics-and-types` -> `flatten_nested` -> `TestFlattenNested`
- `M01-Q06` -> `modules/01-basics-and-types` -> `merge_defaults` -> `TestMergeDefaults`
- `M01-Q07` -> `modules/01-basics-and-types` -> `parse_command` -> `TestParseCommand`
- `M01-Q08` -> `modules/01-basics-and-types` -> `describe_shape` -> `TestDescribeShape`
- `M02-Q01` -> `modules/02-functional-features` -> `select_and_transform` -> `TestSelectAndTransform`
- `M02-Q02` -> `modules/02-functional-features` -> `word_frequencies` -> `TestWordFrequencies`
- `M02-Q03` -> `modules/02-functional-features` -> `fibonacci` -> `TestFibonacci`
- `M02-Q04` -> `modules/02-functional-features` -> `group_by` -> `TestGroupBy`
- `M02-Q05` -> `modules/02-functional-features` -> `running_average` -> `TestRunningAverage`
- `M02-Q06` -> `modules/02-functional-features` -> `interleave` -> `TestInterleave`
- `M02-Q07` -> `modules/02-functional-features` -> `create_counter` -> `TestCreateCounter`
- `M03-Q01` -> `modules/03-oop` -> `Vector2D` -> `TestVector2D`
- `M03-Q02` -> `modules/03-oop` -> `BetterDict` -> `TestBetterDict`
- `M03-Q03` -> `modules/03-oop` -> `Temperature` -> `TestTemperature`
- `M03-Q04` -> `modules/03-oop` -> `ImmutableConfig` -> `TestImmutableConfig`
- `M03-Q05` -> `modules/03-oop` -> `ConfigRecord` -> `TestConfigRecord`
- `M04-Q01` -> `modules/04-interfaces-and-abstraction` -> `DictStore` -> `TestDictStore`
- `M04-Q02` -> `modules/04-interfaces-and-abstraction` -> `LRUStore` -> `TestLRUStore`
- `M04-Q03` -> `modules/04-interfaces-and-abstraction` -> `save_to_file` -> `TestSaveToFile`
- `M05-Q01` -> `modules/05-modules-and-packages` -> `import_from_path` -> `TestImportFromPath`
- `M05-Q02` -> `modules/05-modules-and-packages` -> `validate_package_structure` -> `TestValidatePackageStructure`
- `M05-Q03` -> `modules/05-modules-and-packages` -> `detect_circular_imports` -> `TestDetectCircularImports`
- `M05-Q04` -> `modules/05-modules-and-packages` -> `create_init_reexport` -> `TestCreateInitReexport`
- `M05-Q05` -> `modules/05-modules-and-packages` -> `filter_imports` -> `TestFilterImports`
- `M06-Q01` -> `modules/06-decorators-and-context-managers` -> `timer` -> `TestTimer`
- `M06-Q02` -> `modules/06-decorators-and-context-managers` -> `retry` -> `TestRetry`
- `M06-Q03` -> `modules/06-decorators-and-context-managers` -> `memoize` -> `TestMemoize`
- `M06-Q04` -> `modules/06-decorators-and-context-managers` -> `TimedOpen` -> `TestTimedOpen`
- `M06-Q05` -> `modules/06-decorators-and-context-managers` -> `validate_types` -> `TestValidateTypes`
- `M07-Q01` -> `modules/07-type-hints` -> `Stack` -> `TestStack`
- `M07-Q02` -> `modules/07-type-hints` -> `first` -> `TestFirst`
- `M07-Q03` -> `modules/07-type-hints` -> `typed_deserialize` -> `TestTypedDeserialize`
- `M08-Q01` -> `modules/08-concurrency-and-parallelism` -> `sequential_sum` -> `TestSequentialSum`
- `M08-Q02` -> `modules/08-concurrency-and-parallelism` -> `threaded_sum` -> `TestThreadedSum`
- `M08-Q03` -> `modules/08-concurrency-and-parallelism` -> `process_sum` -> `TestProcessSum`
- `M08-Q04` -> `modules/08-concurrency-and-parallelism` -> `gil_demonstration` -> `TestGILDemonstration`
- `M08-Q05` -> `modules/08-concurrency-and-parallelism` -> `countdown` -> `TestCountdown`
- `M09-Q01` -> `modules/09-asyncio` -> `async_fetch_all` -> `TestAsyncFetchAll`
- `M09-Q02` -> `modules/09-asyncio` -> `async_countdown` -> `TestAsyncCountdown`
- `M09-Q03` -> `modules/09-asyncio` -> `run_concurrently` -> `TestRunConcurrently`
- `M09-Q04` -> `modules/09-asyncio` -> `async_timer` -> `TestAsyncTimer`

### 输出样例契约

`uv run summary` 的首版输出格式建议固定为：

```text
Question ID | Module                         | Symbol               | Status
M01-Q01     | 01-basics-and-types           | classify_number      | PASS
M01-Q02     | 01-basics-and-types           | safe_divide          | FAIL
...

Module                         | Passed | Total | Progress
01-basics-and-types           | 6      | 8     | 75%
02-functional-features        | 4      | 7     | 57%
...
TOTAL                         | 31     | 45    | 68%
```

### 取舍结论

明确放弃以下首版方案：

- 不把题号写进 `practice.py` 业务实现。
- 不为 45 个题组额外增加 pytest marker。
- 不改造 9 个 `run_test.py` 去支持题号参数。
- 不做本地进度文件、数据库或 leaderboard。
- 不引入 `xmake`、`invoke`、`typer`、`click` 等额外工具。

## Assumptions & Decisions

- 决策：唯一 ID 采用**小题级**，而不是仅模块级。
- 决策：进度比较场景以**个人单机进度**为主，不要求集中式多人平台。
- 决策：进度呈现采用**现算汇总**，不额外做本地持久化。
- 决策：采用 **Python 原生统一 CLI**，不引入 `xmake` 之类额外构建层。
- 决策：首版以 `scripts/exercise_registry.py` 为唯一题号真源。
- 假设：当前 `Test...` 类名在短期内保持稳定，因此可以作为 pytest 节点选择器。
- 假设：讨论与验收场景更关心“题组是否通过”，而不是单个 `test_...` 用例编号。

## Feasibility Judgment

### 可行项

- **统一入口可行**：已有 `pyproject.toml` 脚本入口模式。
- **按题号运行可行**：现有测试已按题组组织，可在 pytest 筛选层扩展。
- **批量汇总可行**：已有 `scripts/run_all.py` 的模块扫描与批跑基础。
- **唯一 ID 可行**：现有题目边界清晰，适合补充稳定元数据。

### 主要阻力

- **需要维护中心注册表**：后续若增删题目，必须同步更新 `scripts/exercise_registry.py`。
- **当前粒度仍是模块内习惯**：需要通过 `README.md` 明确把根目录命令提升为推荐主路径。
- **summary 成本高于模块级批跑**：题目级汇总会执行 45 次 pytest 节点，速度会慢于现有按模块粗粒度汇总。

### 总体判断

这次改造**适合施行**，而且属于**低侵入的统一编排增强**：

1. 只需新增 3 个根目录脚本文件与 1 处 `pyproject.toml` 入口声明。
2. 不需要改动现有 9 个模块的练习实现、测试文件和模块内 runner。
3. 能直接满足“唯一题号、单题练习、批量汇总、进度比较”四个核心诉求。

因此，如果后续进入实现阶段，建议按本 spec 一次性落地，而不再拆成“先 summary、后 learn”的两阶段方案。

## Verification Steps

本次为只读研究，未执行任何改动。后续若进入实现阶段，建议按以下标准验证：

- 验证 `README.md` 中的新命令能在根目录直接完成单题学习与汇总。
- 验证每个小题都有唯一且稳定的 ID，且 ID 可从测试输出中直接看到。
- 验证 `summary` 会覆盖全部模块并给出题目级与模块级进度。
- 验证同一仓库状态下，不同学习者运行 `summary` 的输出可直接比较。
- 验证现有模块内 `python run_test.py initial|complete|diff` 兼容路径不被破坏。

## Verification Result

- 已验证 `learn.exe M01-Q01 --target complete` 可正确运行单题并返回通过。
- 已验证 `summary.exe --target complete` 可输出 45 道题的题目级明细与模块级汇总，结果为 `45 / 45` 通过。
- 已验证 `test-all.exe` 仍输出 `All modules passed`，说明原有批量参考答案验证路径未回归。
- 已验证默认学习者路径 `learn.exe M01-Q01` 会对 `initial/` 实现执行并失败，行为符合预期。
- 已通过代码审查复核当前版本，未发现阻塞本轮目标验收的隐藏功能性问题。
