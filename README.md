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

## Prompt 优化与评估记录 (2026-07-24)

### 优化策略
针对航空事故报告的复杂性，对 `prompts/extract_graph.txt` 进行了多轮手动迭代优化：
1. **实体原子化**：强制拆分复杂短语（如“燃油管路破裂”拆分为实体“燃油管路”与关系“破裂导致”），提升知识图谱的结构化程度。
2. **严格去噪**：建立了否定约束，排除通用职衔（如单独的“机长”）和指示代词（如“该部件”），提升精确率。
3. **少样本增强**：集成了 `few_shot_data.csv` 中的高质量航空事故致因链示例，引导模型识别长程因果关系。
4. **因果链强制构建**：明确 `[因素] -> [事件] -> [结果]` 的链条要求。

### 评估结果 (Fuzzy Match)
通过 `scripts/run_automated_evaluation.py` 运行自动化评估，对比 `data/ground_truth.json` 得到以下指标：

| 指标 | 实体 (Entities) | 关系 (Relationships) |
| :--- | :--- | :--- |
| **精确率 (Precision)** | 0.4348 | 0.0556 |
| **召回率 (Recall)** | 0.7143 | 0.0909 |
| **F1 分数 (F1 Score)** | **0.5405** | 0.0690 |

**结论**：实体抽取的精确率和 F1 分数相比基准版本有显著提升。关系抽取受限于本地模型的指令遵循能力，仍有优化空间。

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

## Neo4j 知识图谱导入
- 本项目支持将 GraphRAG 提取的实体与关系导入 Neo4j 图数据库。
- 使用 `src/export_to_neo4j.py` 脚本完成导入。
- 已配置 Docker 容器运行 Neo4j 实例，确保能够正常连接。
