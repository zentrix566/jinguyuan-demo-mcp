# WiFi Password Query MCP Server

一个简单的 MCP (Model Context Protocol) 服务器，提供 `get_wifi_password` 工具来查询预设的 WiFi 密码。

## 功能

- 符合 MCP 协议规范
- 提供 `get_wifi_password` 工具
- 完善的错误处理，返回标准 MCP 错误格式
- 配置通过环境变量外部化
- 健康检查端点

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动服务器

```bash
python server.py
```

默认配置：
- 地址: `http://127.0.0.1:8000`
- 密码: `123456` (可通过环境变量修改)

### 环境变量配置

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `WIFI_PASSWORD` | WiFi 密码 | `123456` |
| `HOST` | 绑定地址 | `127.0.0.1` |
| `PORT` | 监听端口 | `8000` |

示例：
```bash
export WIFI_PASSWORD="my_wifi_password"
export HOST="0.0.0.0"
export PORT="9000"
python server.py
```

## MCP API

### `POST /mcp` - 工具发现
返回可用工具列表。

### `POST /mcp/list-tools` - 列出工具
返回所有可用工具定义。

### `POST /mcp/call-tool` - 调用工具
**请求体：**
```json
{
  "name": "get_wifi_password",
  "parameters": {
    "question": "请问WiFi密码是多少？"
  }
}
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "当前WiFi密码是: 123456"
    }
  ],
  "is_error": false
}
```

### `GET /health` - 健康检查
```json
{
  "status": "healthy"
}
```

## Claude Desktop 配置

在你的 `claude_desktop_config.json` 中添加：

```json
{
  "mcpServers": {
    "wifi-query": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## 许可证

MIT
