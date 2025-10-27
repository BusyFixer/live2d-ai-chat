# Live2d AI聊天系统

一个基于Live2D模型的简易AI虚拟角色聊天系统，集成Ollama AI对话功能和实时表情同步。
## 功能特性
- **AI对话**: 基于Ollama的智能对话系统
- **Live2D角色**: 实时渲染2D虚拟角色
- **表情同步**: 根据对话内容自动切换表情
- **语音反馈**: 对话时播放简单的背景音
## 系统要求
Windows 10/11\
Python 3.8+\
OpenGL 兼容的显卡\
Ollama 本地 AI 服务
## 注意事项
CubismNativeSamples-develop由于文件大小问题需要去
``
https://github.com/Live2D/CubismNativeSamples
``下载zip然后解压。\
确保有足够的 GPU 资源来运行 Live2D 渲染\
首次运行需要下载 Ollama 模型，请保持网络连接\
建议在性能较好的电脑上运行以获得最佳体验
## 项目结构
````
项目根目录/
│  init.py
│  inject.py
│  l2d_sdk.py
│  main.py
│  README
│  utils.py
├─2d
│  └─CubismNativeSamples-develop
│      └─Samples
│          └─Resources
│               └─[models]
└─voice
    └─[voice_files.wav]
````
***
## 安装
- 安装 Python 依赖\
``
pip install ollama pygame glfw PyOpenGL pywin32 live2d-py
``
  - 如果上面的安装不完整，可以尝试：\
  ``
  pip install opencv-python numpy
  ``
- 准备资源文件
  - 下载 Live2D 模型文件（.model3.json 和相关资源），并将整个模型文件夹放入Resources文件夹中：
  ````
    │ 2d
    │  └─CubismNativeSamples-develop
    │      └─Samples
    │          └─Resources
  ````
  - 准备音频文件（.wav 格式, 或使用默认的音频），并将其放入voice文件夹中：
  ````
  └─voice
  ````
## 开始使用
- 初始化\
``
python init.py
``\
输入你想创建的角色名称，系统将创建配置文件和记忆目录。
- 注入表情配置\
``
python inject.py
``\
自动扫描并注入模型的表情配置文件。
- 启动聊天系统\
``
python main.py
``\
~~xx,启动!~~
## 聊天命令
- `/exit` - 退出程序
- `/?` - 显示帮助菜单
## 配置文件说明
系统使用 config.json 管理所有设置：
````json
{
  "memory_name": "角色名称",
  "ask_model": "ollama模型名称",
  "history_length": "最大上下文对话记忆轮数",
  "system": "系统提示词",
  "options": {
    "temperature": 0.7,
    "top_k": 200,
    "top_p": 0.7,
    "num_predict": 300,
    "repeat_penalty": 1.2,
    "num_ctx": 4096
  },
  "voice_path": "./voice/chara.wav",
  "model3.json_path": "./path/to/model.model3.json"
}
````
你可以基于你的需要修改这些系统设置。
## 添加表情支持
- 确保模型目录中包含 .exp3.json 表情文件
- 运行 python inject.py 注入表情配置
- 在系统提示词中告诉 AI 可用的表情标记
## 贡献
这是我的第一个github项目，欢迎提交 Issue 和 Pull Request 来改进这个项目。\
_希望这个项目能为你带来愉快的体验！_
