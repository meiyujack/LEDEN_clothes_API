import random
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class SupplyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tel = models.CharField("电话", max_length=12, unique=True, default="")

    def __str__(self):
        return self.user

class Material(models.Model):
    name=models.CharField("材质名称", max_length=15, unique=True)
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField("颜色名称", max_length=5, unique=True)
    code = models.CharField("颜色代码", max_length=10, default="")

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField("尺码规格", max_length=5)

    def __str__(self):
        return self.name


class Status(models.Model):
    id = models.SmallIntegerField("状态ID", primary_key=True)
    name = models.CharField("状态名称", max_length=5)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField("衣服类别", max_length=20, unique=True)
    image = models.ImageField("图片", max_length=1000, null=True)
    comments = models.CharField("说明", max_length=50, null=True,blank=True)

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    name = models.CharField("仓库名称", max_length=50, unique=True)
    address = models.CharField("仓库地址", max_length=100)
    coord = models.JSONField("经纬度坐标", max_length=100, default=dict)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name="归属人"
    )

    def __str__(self):
        return self.name


class Clothes(models.Model):
    id = models.IntegerField("id", primary_key=True)
    rfid = models.IntegerField("RFID", unique=True, null=True)
    name = models.CharField("衣服名称", max_length=30)
    price = models.SmallIntegerField(verbose_name="进货价格")
    color = models.ForeignKey(Color, on_delete=models.SET_NULL,null=True,verbose_name="颜色")
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, verbose_name="材质")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name="尺码")
    is_printed = models.BooleanField("是否有效", default=False)
    is_reprinted = models.BooleanField("是否重打", default=False)
    status = models.ForeignKey(
        Status, on_delete=models.SET_NULL, null=True, verbose_name="状态"
    )
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="种类")
    indate = models.DateField("入库日期", default=timezone.datetime.today)
    created = models.DateTimeField("创建时间", default=timezone.datetime.now)
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.SET_NULL, null=True, verbose_name="仓库名称"
    )
    comments = models.CharField("备注", max_length=200)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.name

    @staticmethod
    def generate_unique(num: int) -> int:
        """生成唯一标识符，可当任何model的主键，int类型。"""
        answer = ""
        uid = str(uuid.uuid4())
        while len(answer) != num:
            r = random.choice(uid)
            if r.isdigit() and r != "0":
                answer += r
        return answer


class Reprint(models.Model):
    cid = models.ForeignKey(Clothes, on_delete=models.CASCADE, verbose_name="衣服id")
    rfid = models.IntegerField("RFID", unique=True)
    reason = models.CharField("补打原因", max_length=100)
    image = models.ImageField("上传图片", max_length=1000, null=True)
    reprint_time = models.DateTimeField("补打时间", default=timezone.datetime.now)

    def __str__(self):
        return self.cid


class Batch(models.Model):
    cname = models.CharField("批量名称", max_length=50, unique=True)
    cid = models.ForeignKey(Clothes, on_delete=models.CASCADE, verbose_name="衣服id")
    name = models.CharField("衣服名称", max_length=30)
    color = models.CharField("衣服颜色", max_length=5)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name="尺码")
    material = models.CharField("材质", max_length=15, default="全棉")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="归属人")

    def __str__(self):
        return self.cname


class Template(models.Model):
    name = models.CharField("打印模板名称", max_length=20, default="吊牌", unique=True)
    body = models.TextField("主体内容")
    users = models.ManyToManyField(to=User)

    def __str__(self):
        return self.name


class Return(models.Model):
    clothes = models.ForeignKey(
        Clothes, on_delete=models.CASCADE, verbose_name="衣服id"
    )
    price = models.SmallIntegerField("销售价格")
    reason = models.CharField("退货原因", max_length=100)
    image = models.ImageField("上传图片", max_length=1000, null=True)
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.SET_NULL, verbose_name="退货仓库", null=True
    )
    return_time = models.DateTimeField("退货时间", auto_now_add=True)
    handled = models.CharField("经手人", max_length=8)

    def __str__(self):
        return self.clothes
