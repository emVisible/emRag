local data = [[{
  "prompt": "介绍一下浙外",
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
    -- 返回构造的请求
    return wrk.format(wrk.method, "/api/llm/chat", wrk.headers, wrk.body)
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