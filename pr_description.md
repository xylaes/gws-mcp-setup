# 🔒 Fix Missing URL Encoding for User Input

## 🎯 What
The CLI tool fetch URL generation logic in `bin/index.js` lacked proper URL encoding for the `--topic` (`-t`) option. The topic input was injected directly into the template literal URL without being sanitized/encoded.

## ⚠️ Risk
If a user passes a topic containing special characters, spaces, or malformed URL sequences (e.g., `sports/science`, query params, etc.), it could result in an invalid or malformed request to Google News RSS feed, potentially causing crashes or unexpected HTTP query behavior. By ensuring proper URL encoding using `encodeURIComponent`, we prevent URL injection and parsing issues.

## 🛡️ Solution
We wrapped the converted uppercase topic input in `encodeURIComponent` before inserting it into the final request URL:
```javascript
return `${baseUrl}/headlines/section/topic/${encodeURIComponent(topicLower.toUpperCase())}?${params}`;
```
This safely encodes any special characters or symbols present in the user-defined topic string.
