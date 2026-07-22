# 航空事故致因抽取与知识图谱项目 (Aviation Accident Analysis)

本项目基于 Microsoft GraphRAG 框架，旨在自动从航空事故报告中抽取实体与因果关系，并构建符合“人-机-环-管”框架的知识图谱。

## 项目结构
- `data/`: 原始数据与地标数据。
- `input/`: GraphRAG 输入目录（清洗后的文本）。
- `output/`: GraphRAG 输出结果（Parquet, GraphML 等）。
- `prompts/`: 自定义的 GraphRAG 提取提示词。
- `src/`: 
    - `ingest.py`: PDF/DOCX 解析与文本清洗。
    - `evaluate.py`: 提取准确率与 F1 分数评测脚本。
- `run.sh`: 一键运行脚本。
- `settings.yaml`: GraphRAG 配置文件。

## 环境要求
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (推荐)

## 环境配置注意事项
- 若遇到 LLM 连接错误，请检查 `settings.yaml` 中的 `api_base` 是否配置正确。在某些 Docker 或受限环境中，建议将 `localhost` 修改为 `127.0.0.1`。
- 本项目已对 `prompts/extract_graph.txt` 中的抽取示例进行了优化，通过引入复杂场景示例，提升了在航空事故报告中的实体抽取表现。

## 运行流程
1. 将事故报告（PDF/DOCX/TXT）放入 `data/input_reports`。
2. 运行流水线：
   ```bash
   bash run.sh
   ```

## 使用 Ollama (本地 LLM)
在 `settings.yaml` 中修改 `completion_models` 和 `embedding_models`：
```yaml
completion_models:
  default_completion_model:
    model_provider: openai
    api_base: http://localhost:6006/v1
    model: llama3 # 或其他模型
    api_key: ollama # 占位符
```
注意：GraphRAG 对本地模型的支持取决于模型的遵循指令能力。

## 提取 Schema (人-机-环-管)
- **实体类型**: person (人), equipment (机), environment (环), organization (管), procedure, event, weather, violation.
- **关系类型**: leads to, limited by, violates, not executed, belongs to.

## 评测指标
- **抽取准确率**: 实体与关系的 F1-score。
- **路径质量**: 专家评分 (1-5)。
- **工程性能**: 解析成功率 (>95%), 处理速度 (<2 min/篇)。
