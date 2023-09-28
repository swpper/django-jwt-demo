from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 增加想要加到token中的信息
        # token['username'] = user.username
        # token['email'] = user.email
        # token['resource_name'] = user.resource_name
        # token['scope'] = user.scope
        print(token)
        print(type(token))
        return token

        # custom jwt token
        # 使用用户请求的resource_name的resource_secret私钥加密生成jwt,资源服务器使用公钥解密
        
        
        # return {
        #     'refresh': '111111',
        #     'access_token': '22222222'
        # }
        

    
    def validate(self, attrs):
        """
        此方法为响应数据结构处理
        原有的响应数据结构无法满足需求，在这里重写结构如下：
        {
            "refresh": "xxxx.xxxxx.xxxxx",
            "access": "xxxx.xxxx.xxxx",
            "expire": Token有效期截止时间,
            "username": "用户名",
            "email": "邮箱"
        }

        :param attrs: 请求參數
        :return: 响应数据
        """
        # data是个字典
        # 其结构为：{'refresh': '用于刷新token的令牌', 'access': '用于身份验证的Token值'}
        data = super().validate(attrs)

        # 获取Token对象
        refresh = self.get_token(self.user)
        # 令牌到期时间
        data['expire'] = refresh.access_token.payload['exp']  # 有效期
        # 用户名
        data['username'] = self.user.username
        # 邮箱
        data['email'] = self.user.email
        return data
