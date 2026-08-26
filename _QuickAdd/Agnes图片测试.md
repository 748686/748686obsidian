```js
module.exports = {
    entry: async (params, settings) => {
        const { app, variables } = params;

        const file = app.workspace.getActiveFile();

        if (!file) {
            new Notice("请先打开包含学习流程图片的笔记");
            return;
        }

        const content = await app.vault.read(file);

        const match = content.match(
            /!\[\[([^\]]+\.(?:png|jpg|jpeg|webp|gif))\]\]/i
        );

        if (!match) {
            new Notice("当前笔记没有找到图片");
            return;
        }

        const imageName = match[1];

        const imageFile =
            app.metadataCache.getFirstLinkpathDest(
                imageName,
                file.path
            );

        if (!imageFile) {
            new Notice("找不到图片文件");
            return;
        }

        const arrayBuffer =
            await app.vault.readBinary(imageFile);

        const bytes = new Uint8Array(arrayBuffer);

        let binary = "";
        const chunkSize = 0x8000;

        for (let i = 0; i < bytes.length; i += chunkSize) {
            binary += String.fromCharCode(
                ...bytes.subarray(i, i + chunkSize)
            );
        }

        const base64 = btoa(binary);

        const ext = imageFile.extension.toLowerCase();

        const mimeMap = {
            png: "image/png",
            jpg: "image/jpeg",
            jpeg: "image/jpeg",
            webp: "image/webp",
            gif: "image/gif"
        };

        const mime = mimeMap[ext] || "image/png";

        const dataUrl =
            `data:${mime};base64,${base64}`;

      const prompt = `
请仔细分析这张学习流程图片。

请根据图片中的课程、学习阶段、知识结构和学习流程，
设计一个完整、合理、可长期使用的 Obsidian 学习系统。

你不仅要设计：
1. 根文件夹
2. 子文件夹
3. Markdown 文件
4. 每个文件的用途

还要为每一个 Markdown 文件生成适合直接使用的初始内容。

最终只能输出有效 JSON。

严格使用以下结构：

{
  "name": "根文件夹名称",
  "folders": [
    {
      "name": "文件夹名称",
      "files": [
        {
          "name": "文件名称",
          "content": "Markdown文件内容"
        }
      ],
      "folders": []
    }
  ]
}

要求：

- 文件名不要包含 .md
- content 必须是合法 JSON 字符串
- content 使用 Markdown
- 内容应该真正有学习用途，而不是简单重复文件名
- 可以包含标题、表格、任务清单、复习记录、学习方法等
- 根据图片中的学习流程合理设计内容
- 文件之间可以使用 Obsidian 双链，例如 [[单词笔记]]
- 不要创建没有用途的文件
- 不要重复创建文件
- 每个文件夹必须有 files 和 folders
- 没有文件时使用 []
- 没有子文件夹时使用 []
- 使用双引号
- 不允许尾随逗号
- 不要输出 Markdown 代码块
- 不要输出解释
- 最终只输出 JSON
`;
        const response = await fetch(
            "https://api.agnes-ai.cn/v1/chat/completions",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${settings["API Key"]}`
                },
                body: JSON.stringify({
                    model: "agnes-2.5-flash",
                    messages: [
                        {
                            role: "user",
                            content: [
                                {
                                    type: "image_url",
                                    image_url: {
                                        url: dataUrl
                                    }
                                },
                                {
                                    type: "text",
                                    text: prompt
                                }
                            ]
                        }
                    ],
                    temperature: 0.1,
                    max_tokens: 8192
                })
            }
        );

        if (!response.ok) {
            const errorText = await response.text();

            console.error("Agnes API:", errorText);

            new Notice(
                `Agnes API 错误：${response.status}`
            );

            return;
        }

        const result = await response.json();

        let answer =
            result?.choices?.[0]?.message?.content;

        if (!answer) {
            new Notice("Agnes 没有返回内容");
            console.log(result);
            return;
        }

        // 清除可能出现的 Markdown 代码块
        answer = answer
            .replace(/^```json\s*/i, "")
            .replace(/^```\s*/i, "")
            .replace(/\s*```$/i, "")
            .trim();

        // 检查 JSON
        try {
            JSON.parse(answer);
        } catch (e) {
            console.error("Agnes 原始输出:", answer);

            new Notice("Agnes 返回的不是有效 JSON");
            return;
        }

        // 把 JSON 放入 Macro 变量
        variables.output = answer;

        new Notice("图片分析完成，JSON 已生成");
    },

    settings: {
        name: "Agnes 图片生成目录 JSON",
        author: "QuickAdd",
        options: {
            "API Key": {
                type: "secret",
                id: "agnes-api-key",
                placeholder: "粘贴 Agnes API Key",
                description: "安全保存在 Obsidian SecretStorage"
            }
        }
    }
};