"""Bedrock AgentClient module."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import boto3

if TYPE_CHECKING:
    from collections.abc import Generator

AGENT_RUNTIME_ARN = "arn:aws:bedrock-agentcore:ap-northeast-1:100994446770:runtime/data_analyst-JdXi8kEIuv"
S3_PATH = "s3://juv-shun.data-analyst-agent-trial/data/members.csv"


def invoke_streaming(prompt: str) -> Generator[str]:
    """ストリーミングでAgentCoreからのレスポンスを取得するジェネレータ。

    Args:
        prompt (str): ユーザーからの分析依頼テキスト

    Yields:
        str: レスポンスのテキストチャンク

    """
    if not AGENT_RUNTIME_ARN:
        yield "エラー: 環境変数 AGENT_RUNTIME_ARN が設定されていません。"
        return

    # boto3クライアントを作成 (bedrock-agentcore)
    try:
        client = boto3.client("bedrock-agentcore", region_name="ap-northeast-1")
    except Exception as e:  # noqa: BLE001
        yield f"クライアント作成エラー: {e!s}"
        return

    payload = {
        "prompt": prompt,
        "s3": S3_PATH,
    }

    try:
        response = client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_RUNTIME_ARN,
            contentType="application/json",
            payload=json.dumps(payload).encode("utf-8"),
        )

        streaming_body = response["response"]
        for chunk in streaming_body.iter_lines():
            if chunk:
                line = chunk.decode("utf-8").removeprefix("data: ")
                try:
                    data = json.loads(line)
                    if isinstance(data, dict) and "event" in data:
                        event = data["event"]
                        if "contentBlockDelta" in event:
                            text = event["contentBlockDelta"]["delta"].get("text", "")
                            if text:
                                yield text
                except (json.JSONDecodeError, TypeError, KeyError):
                    pass
    except Exception as e:  # noqa: BLE001
        yield f"実行エラー: {e!s}"
