local data = [[{
  "prompt": "浙江外国语学院章程第五十条是什么",
  "system_prompt": "",
  "chat_history": [],
  "collection_name":"edu_c_1"
}]]

wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"
wrk.headers["Accept"] = "application/json"
wrk.body = data

local response_data = ""

-- 请求函数
function request()
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