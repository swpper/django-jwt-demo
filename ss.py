import base64
import json

# 假设您的JWT token如下
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

# 对header部分进行Base64URL解密
header_bytes = base64.urlsafe_b64decode(jwt_token.split('.')[0])
header_str = header_bytes.decode('utf-8')

# 解析header部分，例如JSON解析
header_data = json.loads(header_str)

print(header_data)

import base64

# 假设您的JWT token如下
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

# 对payload部分进行Base64URL解密
payload_bytes = base64.urlsafe_b64decode(jwt_token.split('.')[1])
payload_str = payload_bytes.decode('utf-8')

# 解析payload部分，例如JSON解析
payload_data = json.loads(payload_str)

print(payload_data)