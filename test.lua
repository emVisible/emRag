local data = [[{
  "prompt": "介绍一下杭州, 详细介绍当地景色",
  "system_prompt": "",
  "chat_history": []
}]]

wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"
wrk.headers["Accept"] = "application/json"
wrk.body = data

function request()
  return wrk.format(nil, url)
end