from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

# ユーザーテーブル変更用Manager
class UserManager(BaseUserManager):
    use_in_migrations = True

        #ユーザー作成ファンクション
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Emailを入力して下さい')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
        # 通常ユーザー作成
    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

        # スーパーユーザー作成
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff=Trueである必要があります。')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser=Trueである必要があります。')
        return self._create_user(username, email, password, **extra_fields)

from django.db.models import Q #インポート

# Create your models here.

# ユーザーテーブル
class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_("username"), max_length=50, validators=[username_validator], blank=True)
    email = models.EmailField(_("email_address"), unique=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    insert_timestamp = models.DateTimeField(default=timezone.now)
    update_timestamp = models.DateTimeField(default=timezone.now)

    objects = UserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

# email送信用
class Activate(models.Model):
    """ 仮登録したユーザを本登録するためのModel """
  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255, unique=True)
    expiration_date = models.DateTimeField(blank=True, null=True)

# 投稿テーブル
class Post(models.Model):
    post_id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(null=True, blank=True)
    tag = models.TextField(null=True, blank=True)
    text_probrem = models.TextField(null=True, blank=True)
    text_solution = models.TextField(null=True, blank=True)
    reference_url = models.TextField(null=True, blank=True)
    insert_timestamp = models.CharField(max_length=20)
    update_timestamp = models.CharField(max_length=20)
    
    
# 投稿一時保存テーブル
class Post_Tmp(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(null=True, blank=True)
    tag = models.TextField(null=True, blank=True)
    text_probrem = models.TextField(null=True, blank=True)
    text_solution = models.TextField(null=True, blank=True)
    reference_url = models.TextField(null=True, blank=True)
    insert_timestamp = models.CharField(max_length=20)
    update_timestamp = models.CharField(max_length=20)
    already_post_fg = models.BooleanField(default=False)
    

# コメントテーブル
class Comment(models.Model):
    comment_id = models.CharField(max_length=20, primary_key=True)#投稿が増えすぎると桁数オーバーするかも。
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    insert_timestamp = models.CharField(max_length=20)
    update_timestamp = models.CharField(max_length=20)

# リアクションテーブル
class Reaction(models.Model):
    reaction_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,  null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_target = models.CharField(max_length=20, default="post")
    good = models.CharField(max_length=1)
    insert_timestamp = models.CharField(max_length=20)
    update_timestamp = models.CharField(max_length=20)

# 閲覧履歴テーブル
class History(models.Model):
    history_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insert_timestamp = models.CharField(max_length=20)

# プロフィールテーブル
class Profile(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True)#ユーザーが増えすぎると桁数オーバーするかも。
    self_introduction = models.TextField(null=True)
    icon = models.TextField(null=True)
    insert_timestamp = models.CharField(max_length=20)
    update_timestamp = models.CharField(max_length=20)
