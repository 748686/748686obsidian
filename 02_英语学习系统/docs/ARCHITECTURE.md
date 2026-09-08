# 架构

1. 输入：`input/YYYY-MM-DD.md`。
2. `input_parser.py` 读取文本词汇与 Markdown 图片。
3. `vision_extract.py` 负责图片词汇识别接口。
4. `agnes_generate.py` 生成结构化短文。
5. `validate.py` 做确定性校验。
6. `render_markdown.py` 固定渲染两栏注记。
7. `exam_generate.py` 生成100分试卷。
8. `image_generate.py` 与 `tts_generate.py` 为多媒体接口模块。
9. `main.py` 编排全流程。
