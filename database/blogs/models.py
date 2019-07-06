from django.db import models
from django.core import validators


# 用户表
class UserModel(models.Model):
    # 账户名
    username = models.CharField(max_length=11, validators=[validators.MinLengthValidator(6, '账户长度最小为6'),
                                                           validators.RegexValidator('^\w{6,11}$', '账户格式错误'),
                                                           validators.MaxLengthValidator(11, '账户长度最大为11')])
    # 账户密码
    password = models.CharField(max_length=16, validators=[validators.MinLengthValidator(6, '密码长度最小为6'),
                                                           validators.MaxLengthValidator(16, '密码长度最大为16')])

    # 用户昵称
    name = models.CharField(max_length=100)
    # 用户年龄
    age = models.IntegerField()
    # 用户头像
    head = models.FileField(upload_to='head', null=True, validators=[
        validators.FileExtensionValidator(['jpg', 'png'], '格式错误')
    ])
    # 个性签名
    sign = models.CharField(max_length=100)
    # 性别
    sex = models.CharField(max_length=2)
    # 用户组
    this_g = models.ForeignKey('Groups', on_delete=models.CASCADE)
    # 关注人数
    att_num = models.IntegerField(default=0)
    # 粉丝人数
    bean_num = models.IntegerField(default=0)
    # 发表文章数
    art_num = models.IntegerField(default=0)
    # 电话号
    phone = models.CharField(max_length=11, null=True, validators=[validators.MinLengthValidator(11, '电话号长度为11位'),
                                                                   validators.MaxLengthValidator(11, '电话号长度为11位')])


# 关注表
class Attention(models.Model):
    att_u1 = models.ForeignKey(UserModel, related_name='user_att', on_delete=models.CASCADE)  # 关注人id
    att_u2 = models.ForeignKey(UserModel, on_delete=models.CASCADE)  # 被关注人id


# 文章表
class ArticleModel(models.Model):
    title = models.CharField(max_length=30)  # 文章名
    content = models.TextField()  # 文章内容
    user_s = models.ForeignKey(UserModel, on_delete=models.CASCADE)  # 用户外键
    publish_date = models.DateTimeField(auto_now_add=True)  # 发表时间
    level = models.IntegerField(null=True)  # 文章级别
    date = models.DateTimeField(auto_now_add=True)  # 文章发布时间
    file = models.FileField(upload_to='files', null=True)  # 上传文件
    com_num = models.IntegerField(default=0)  # 评论数
    thu_num = models.IntegerField(default=0)  # 点赞数


# 评论表
class CommentModel(models.Model):
    content = models.TextField()  # 评论内容
    this_a = models.ForeignKey(ArticleModel, on_delete=models.CASCADE)  # 和文章的关系
    this_u = models.ForeignKey(UserModel, on_delete=models.CASCADE)  # 和用户的关系
    this_c = models.ForeignKey("CommentModel", on_delete=models.CASCADE, null=True)  # 和评论之间的关系
    date = models.DateTimeField(auto_now_add=True)  # 评论时间


# 点赞表
class ThumbsUp(models.Model):
    this_u = models.ForeignKey(UserModel, on_delete=models.CASCADE)  # 和用户之间的关系
    this_a = models.ForeignKey(ArticleModel, on_delete=models.CASCADE)  # 和文章之间的关系
    date = models.DateTimeField(auto_now_add=True)  # 点赞的时间


# 用户组
class Groups(models.Model):
    name = models.CharField(max_length=10)
