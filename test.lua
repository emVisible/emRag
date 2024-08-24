local data = [[{
  "prompt": "浙外章程第三十九条原文是什么？",
  "system_prompt": "",
  "chat_history": []
}]]

wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"
wrk.headers["Accept"] = "application/json"
wrk.body = data

local response_data = ""

-- 请求函数
function request()
    -- 打印请求信息（调试用）
    print("Sending request with body:", wrk.body)
    -- 返回构造的请求
    return wrk.format(wrk.method, "/api/rag/chat", wrk.headers, wrk.body)
end

-- 响应函数
function response(status, headers, body)
  print(body)
end

-- 测试完成后的总结
function done(summary, latency, requests)
    print("Test completed. Summary:")
    print(summary)
    print("Total Streamed Response Data:", response_data)
end