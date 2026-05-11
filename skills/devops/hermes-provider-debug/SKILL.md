---
name: hermes-provider-debug
description: Debug Hermes model provider connectivity issues (403, 429, timeouts, exhausted credentials)
version: 1.0
category: devops
---

# Debug Hermes Model Provider Issues

## Trigger
When Hermes reports errors like:
- `❌ Non-retryable error (HTTP 403): Your request was blocked`
- `HTTP 429: rate limit exceeded`
- `credential pool: marking <provider> exhausted`
- `Could not detect context length for model`

## Step-by-step Debugging

### 1. Check logs for error pattern
```bash
grep -B2 -A5 "403\|blocked\|exhausted\|429\|failed" ~/.hermes/logs/agent.log | grep -v "context length" | tail -40
```
Look for: error frequency, which sessions (cron vs interactive), timing pattern.

### 2. Check current config
```bash
cat ~/.hermes/config.yaml | grep -A 10 "provider\|base_url\|api_key\|model:"
```
Also check custom providers section at bottom of config.

### 3. Check credential pool
```bash
cat ~/.hermes/auth.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
cp = d.get('credential_pool', {})
for provider, creds in cp.items():
    for c in creds:
        has_token = bool(c.get('access_token') or c.get('api_key'))
        print(f'{provider} | id:{c.get(\"id\")} | has_token:{has_token} | exhausted:{c.get(\"exhausted\",False)} | last_status:{c.get(\"last_status\")} | last_error:{c.get(\"last_error_code\")} | base_url:{c.get(\"base_url\",\"default\")}')
"
```

Key fields: `exhausted`, `last_status`, `last_error_code`, `last_error_reason`.

### 4. Test API directly with curl
```bash
# Extract access token (NOT api_key — Hermes stores it as access_token)
ACCESS_TOKEN=$(cat ~/.hermes/auth.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
cp = d.get('credential_pool', {})
for provider, creds in cp.items():
    if '<PROVIDER_NAME>' in provider:
        for c in creds:
            if c.get('access_token'):
                print(c['access_token'])
                break
        break
")

# Test 1: List models
curl -s https://<BASE_URL>/v1/models -H "Authorization: Bearer $ACCESS_TOKEN" | head -50

# Test 2: Simple chat
curl -s --max-time 30 https://<BASE_URL>/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"model":"<MODEL>","messages":[{"role":"user","content":"Say OK"}],"max_tokens":10}'

# Test 3: With long system prompt (simulates real Hermes payload)
python3 -c "
import json
payload = {
    'model': '<MODEL>',
    'messages': [
        {'role': 'system', 'content': 'You are a helpful assistant. ' * 500},
        {'role': 'user', 'content': 'Test message'}
    ],
    'max_tokens': 50
}
print(json.dumps(payload))
" | curl -s --max-time 30 https://<BASE_URL>/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" -d @-

# Test 4: With tools (full payload simulation)
python3 -c "
import json
tools = [{'type':'function','function':{'name':f'tool_{i}','description':f'Tool {i} for testing','parameters':{'type':'object','properties':{'p':{'type':'string'}}}}} for i in range(15)]
payload = {'model':'<MODEL>','messages':[{'role':'system','content':'System. '*200},{'role':'user','content':'Test'}],'max_tokens':100,'tools':tools}
print(json.dumps(payload))
" | curl -s --max-time 30 https://<BASE_URL>/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" -d @-
```

### 5. Check cron job impact
Cron jobs can trigger rate limits. Check active cron jobs:
```bash
hermes cron list 2>/dev/null
```
If cron jobs run frequently on the same provider, they may exhaust credentials.

## Common Root Causes

| Error | Cause | Fix |
|-------|-------|-----|
| `403 Your request was blocked` | Rate limit / content filter from provider | Reduce cron frequency or switch provider |
| `429 rate limit` | Too many requests in time window | Wait for reset, add fallback provider |
| `credential pool exhausted` | All API keys hit limits | Wait for reset or add more keys |
| `Could not detect context length` | Non-standard model name | Set `model.context_length` in config.yaml |

## Key Insight
Hermes credential pool uses `access_token` field (not `api_key`) in auth.json. When testing manually, use the `access_token` value as Bearer token.
