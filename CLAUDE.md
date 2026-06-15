# python tutorial for java guy

Java 背景的我在准备一个涉及到 Python 的岗位。

我不追求cosplay python 专家，但是我希望多少有一些必要的python的认识，来体现我重视这个机会。请你告诉我至少我应该知道什么？在能在视频面试中的快问快答的刺探阶段达到我的目标？

要求：
1、我需要一个交互式的教程
2、我需要一个 complete 项目作为完整的参考答案和测试，一个对照的 intital 项目包含必要的骨架和测试，同步补全 intital项目可以最终达到 compelte项目的样子。
3、我需要完整的 unittest 覆盖。

我已经被问到过的问题:

- GIL 的前世今生
- 如何不依赖第三方库，如何 Parellel 地运行计算密集型任务。有几种做法？
- Pyhthon没有 java 中的 interface，如何实现 interface 的 Object-Oriented Design。

ref:

- [https://learnxinyminutes.com/python/]
(/docs//Learn%20Python%20in%20Y%20Minutes%20(2026_5_29%2001：19：53).html)
- [https://docs.python.org/3/download.html](/docs/python-3.14-docs-html/)

## Python 运行时环境坑点

基于 `.trae/documents/python-runtime-management-plan.md` 和本次实际落地过程，当前仓库有几个需要长期记住的环境坑点：

1. Python 版本必须显式固定，不能依赖宿主机默认解释器。
   - 项目 `pyproject.toml` 要求 `requires-python = ">=3.12"`。
   - 如果本地虚拟环境实际还是 Python 3.10，`uv`、`pytest`、editable install 和 console script 会出现不一致行为。

2. 不要假设已有 `.venv` 一定可用。
   - 曾出现过 `.venv` 中 `python.exe` 存在，但 `pyvenv.cfg` 缺失的半损坏环境。
   - 这种状态下命令表面像“卡住”或“随机报错”，本质是虚拟环境已损坏。

3. `uv venv` 在已有目录上可能触发交互确认。
   - 在自动化或沙箱环境里，这会表现为命令“卡死”。
   - 需要优先使用非交互参数，例如显式清理后重建，避免等待终端确认。

4. `uv venv` 新建环境后，不要假设 `pip` 已可直接使用。
   - 某些场景下需要先执行 `python -m ensurepip --upgrade`。
   - 否则后续 `python -m pip install ...` 会直接失败。

5. 重型依赖安装如果中途中断，容易留下半安装环境。
   - 这会导致 `dist-info` 元数据不完整，进一步让 `pytest` 插件发现或 console script 运行失败。
   - 如果怀疑环境被打断污染，优先新建干净虚拟环境，而不是在旧环境上反复修补。

6. `uv pip install -e ".[dev]"` 依赖当前解释器版本，不能混用系统 Python。
   - 如果命令实际落到 Python 3.10，但项目要求 3.12+，解析依赖会直接失败。
   - 需要明确指定目标环境，避免系统 Python 与项目虚拟环境串用。

7. console script 能否运行，不只取决于 `[project.scripts]`。
   - 这次实际踩到的问题是：即使定义了 `learn` / `summary` / `test-all`，如果 `scripts` 没有被正确打包，入口仍会报 `ModuleNotFoundError: No module named 'scripts'`。
   - 解决方式是：
     - 保证 `scripts/` 是可导入包；
     - 明确声明 setuptools 的打包配置。

8. Windows 下链接和换行要特别小心。
   - Git 会提示 `CRLF` / `LF` 转换，这通常不是功能错误，但要避免在脚本文件里反复制造无意义 diff。
   - 创建 `AGENTS.md` 之类的软链接时，优先使用 PowerShell 的显式命令，并确认链接目标正确。

## 建议的环境纪律

- 始终先确认项目解释器版本，再跑测试或安装依赖。
- 虚拟环境异常时，优先重建干净环境，不要在损坏环境上持续试错。
- 自动化命令优先使用非交互方式。
- 修改 `pyproject.toml` 的命令入口后，务必验证 console script，而不只是 `python -m ...`。
