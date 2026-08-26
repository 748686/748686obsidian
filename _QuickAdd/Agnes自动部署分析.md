```js
module.exports = {
    entry: async (params, settings) => {
        const { app } = params;

        const file = app.workspace.getActiveFile();

        if (!file) {
            new Notice("请先打开第二张图片所在的笔记");
            return;
        }

        const content = await app.vault.read(file);

        const start = content.indexOf("![[");
        const end = content.indexOf("]]", start);

        if (start === -1 || end === -1) {
            new Notice("当前笔记没有找到图片");
            return;
        }

        const imageName = content
            .substring(start + 3, end)
            .trim();

        if (!imageName) {
            new Notice("图片名称为空");
            return;
        }

        const imageFile =
            app.metadataCache.getFirstLinkpathDest(
                imageName,
                file.path
            );

        if (!imageFile) {
            new Notice("找不到图片文件：" + imageName);
            return;
        }

        new Notice("正在读取图片……");

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

        let mime = "image/png";

        if (ext === "jpg" || ext === "jpeg") {
            mime = "image/jpeg";
        } else if (ext === "webp") {
            mime = "image/webp";
        } else if (ext === "gif") {
            mime = "image/gif";
        }

        const dataUrl =
            "data:" + mime + ";base64," + base64;

        const prompt = `
你现在是 Obsidian 自动知识库部署架构师。

请仔细分析这张图片。

图片是一张 Obsidian 自动知识库插件与工具配置图。

请识别图片中的信息来源、插件、外部工具、数据流向、保存位置、自动化任务，以及需要用户手动配置的项目。

请特别识别图片中的 10 个主要模块。

请根据图片设计一个合理的 Obsidian 知识库部署方案。

建议考虑以下目录：

00_Inbox
01_Sources
02_Projects
03_Knowledge
04_Outputs
05_Review
99_Attachments

最终只返回 JSON。

不要输出解释。
不要输出 Markdown。
不要输出 JSON 代码块。

JSON 必须使用下面的结构：

{
  "system_name": "系统名称",
  "description": "系统用途",
  "folders": [
    {
      "path": "00_Inbox",
      "purpose": "用途"
    }
  ],
  "files": [
    {
      "path": "00_Inbox/README.md",
      "purpose": "用途",
      "content": "Markdown内容"
    }
  ],
  "plugins": [
    {
      "name": "插件名称",
      "purpose": "插件作用",
      "target": "保存位置",
      "setup": "配置说明"
    }
  ],
  "services": [
    {
      "name": "服务名称",
      "purpose": "用途",
      "target": "输出位置",
      "setup": "配置说明"
    }
  ],
  "manual_setup": [
    {
      "name": "需要人工配置的项目",
      "reason": "原因",
      "required": true
    }
  ],
  "automation": [
    {
      "name": "自动化任务",
      "trigger": "触发方式",
      "input": "输入来源",
      "output": "输出位置"
    }
  ]
}

所有路径使用正斜杠。

文件必须以 .md 结尾。

不要重复文件。

只返回可以被 JSON.parse 解析的 JSON。
`;

        new Notice("正在发送给 Agnes……");

        let response;

        try {
            response = await fetch(
                "https://api.agnes-ai.cn/v1/chat/completions",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization":
                            "Bearer " + settings["API Key"]
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
                        max_tokens: 12000
                    })
                }
            );
        } catch (error) {
            new Notice("Agnes 网络请求失败");

            console.error(error);
            return;
        }

        const responseText = await response.text();

        console.log("Agnes 原始返回：", responseText);

        if (!response.ok) {
            const errorFile =
                "00_Inbox/系统部署/Agnes错误返回.md";

            const folder =
                app.vault.getAbstractFileByPath(
                    "00_Inbox/系统部署"
                );

            if (!folder) {
                await app.vault.createFolder(
                    "00_Inbox/系统部署"
                );
            }

            await app.vault.create(
                errorFile,
                "# Agnes API 错误\n\n```text\n" +
                responseText +
                "\n```\n"
            );

            new Notice(
                "Agnes API 出错，已经保存错误信息"
            );

            return;
        }

        let result;

        try {
            result = JSON.parse(responseText);
        } catch (error) {
            new Notice("Agnes 返回内容不是 API JSON");
            return;
        }

        let answer =
            result &&
            result.choices &&
            result.choices[0] &&
            result.choices[0].message &&
            result.choices[0].message.content;

        if (!answer) {
            new Notice("Agnes 没有返回分析内容");
            console.log(result);
            return;
        }

        answer = String(answer).trim();

        console.log("Agnes AI 内容：", answer);

        const outputFolder =
            "00_Inbox/系统部署";

        if (!app.vault.getAbstractFileByPath(outputFolder)) {
            await app.vault.createFolder(outputFolder);
        }

        // 先保存 Agnes 的原始 AI 输出
        const rawFile =
            outputFolder + "/Agnes原始分析.md";

        const oldRaw =
            app.vault.getAbstractFileByPath(rawFile);

        if (oldRaw) {
            await app.vault.modify(
                oldRaw,
                "# Agnes 原始分析\n\n" + answer
            );
        } else {
            await app.vault.create(
                rawFile,
                "# Agnes 原始分析\n\n" + answer
            );
        }

        // 尝试从 AI 返回内容中提取 JSON
        const firstBrace =
            answer.indexOf("{");

        const lastBrace =
            answer.lastIndexOf("}");

        if (
            firstBrace === -1 ||
            lastBrace === -1 ||
            lastBrace <= firstBrace
        ) {
            new Notice(
                "Agnes 没有返回 JSON，已保存原始分析"
            );
            return;
        }

        const jsonText =
            answer.substring(
                firstBrace,
                lastBrace + 1
            );

        let data;

        try {
            data = JSON.parse(jsonText);
        } catch (error) {
            new Notice(
                "JSON 解析失败，已保存 Agnes 原始分析"
            );

            console.error(
                "JSON解析失败：",
                jsonText
            );

            return;
        }

        const outputFile =
            outputFolder + "/系统部署计划.json";

        const jsonContent =
            JSON.stringify(data, null, 2);

        const oldFile =
            app.vault.getAbstractFileByPath(
                outputFile
            );

        if (oldFile) {
            await app.vault.modify(
                oldFile,
                jsonContent
            );
        } else {
            await app.vault.create(
                outputFile,
                jsonContent
            );
        }

        new Notice(
            "系统部署计划生成成功！"
        );
    },

    settings: {
        name: "Agnes 自动部署分析",
        author: "QuickAdd",
        options: {
            "API Key": {
                type: "secret",
                id: "agnes-api-key",
                placeholder: "粘贴 Agnes API Key"
            }
        }
    }
};