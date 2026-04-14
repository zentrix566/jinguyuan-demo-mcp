#!/usr/bin/env python3
"""
WiFi密码查询 MCP 服务器
当用户询问WiFi密码时，返回预设密码 123789
"""

import os
import logging
from typing import Any, List
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from mcp.types import Tool, TextContent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="WiFi Query MCP Server", version="0.1.0")

# 定义预设WiFi密码 - 从环境变量读取，使用默认值作为后备
WIFI_PASSWORD = os.getenv("WIFI_PASSWORD", "123789")

class CallToolRequest(BaseModel):
    name: str
    parameters: dict[str, Any]

class CallToolResponse(BaseModel):
    content: List[TextContent]
    is_error: bool = False

# 错误处理：请求验证异常
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """处理请求验证错误，返回符合MCP格式的错误响应"""
    return JSONResponse(
        content=CallToolResponse(
            content=[TextContent(type="text", text=f"请求验证失败: {str(exc)}")],
            is_error=True
        ).model_dump()
    )

# 错误处理：通用异常
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """处理所有未捕获的异常，返回符合MCP格式的错误响应"""
    logger.error(f"未处理的异常: {str(exc)}", exc_info=True)
    return JSONResponse(
        content=CallToolResponse(
            content=[TextContent(type="text", text=f"服务器内部错误: {str(exc)}")],
            is_error=True
        ).model_dump()
    )

@app.get("/")
async def root():
    return {"message": "WiFi Query MCP Server is running", "tool": "get_wifi_password"}

@app.get("/health")
async def health_check():
    """健康检查端点，用于监控"""
    return {"status": "healthy"}

@app.post("/mcp/list-tools")
async def list_tools():
    """列出可用工具"""
    return {
        "tools": [
            Tool(
                name="get_wifi_password",
                description="获取WiFi密码，当用户询问WiFi密码时调用此工具",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "用户关于WiFi密码的问题"
                        }
                    },
                    "required": ["question"]
                }
            ).model_dump()
        ]
    }

@app.post("/mcp/call-tool")
async def call_tool(request: CallToolRequest):
    """调用工具"""
    if request.name != "get_wifi_password":
        return CallToolResponse(
            content=[TextContent(type="text", text=f"未知工具: {request.name}")],
            is_error=True
        ).model_dump()

    question = request.parameters.get("question", "").strip()
    logger.info(f"收到问题: {question}")

    # 返回预设密码
    return CallToolResponse(
        content=[
            TextContent(
                type="text",
                text=f"当前WiFi密码是: {WIFI_PASSWORD}"
            )
        ],
        is_error=False
    ).model_dump()

@app.post("/mcp")
async def mcp_endpoint():
    """MCP主端点，支持标准MCP发现"""
    return await list_tools()

if __name__ == "__main__":
    # 绑定到 127.0.0.1 仅本地访问，避免公网泄露信息
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
