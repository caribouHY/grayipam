from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
import ipaddress


def validate_network_ipv4(value):
    print('validate IPv4')
    try:
        net = ipaddress.IPv4Network(value)
        if net.is_private is True:
            if net.prefixlen <= 30:
                max = int(net.broadcast_address)
                min = int(net.network_address)
                c = Network.objects.filter(
                    Q(ipv4_min__range=(min, max)) | Q(ipv4_min__lte=min, ipv4_max__gte=max)).count()
                if c != 0:
                    raise ValidationError('指定されたネットワークは既に存在しています。')
            else:
                raise ValidationError('サブネット長は30以下を入力してください。')
        else:
            raise ValidationError('ローカルアドレスを入力してください。')
    except ipaddress.AddressValueError:
        raise ValidationError('有効なIPv4アドレスを入力してください。')
    except ipaddress.NetmaskValueError:
        raise ValidationError('有効なネットマスクを入力してください。')
    except ValueError:
        raise ValidationError('アドレスのホスト部を0にしてください。')


class Network(models.Model):

    name = models.CharField(
        verbose_name='名称', max_length=32, null=True, blank=True)
    ipv4_cidr = models.CharField(
        verbose_name='IPv4 CIDR', max_length=18, validators=[validate_network_ipv4])
    ipv4_max = models.IntegerField()
    ipv4_min = models.IntegerField()
    vid = models.IntegerField(verbose_name='VLAN ID', default=0, validators=[
                              MinValueValidator(0), MaxValueValidator(0xfff)])
    note = models.CharField(
        verbose_name='メモ', max_length=64, null=True, blank=True)

    class Meta:
        ordering = ['ipv4_min']

    def save(self, **kwargs):
        net = ipaddress.IPv4Network(self.ipv4_cidr)
        self.ipv4_max = int(net.broadcast_address)
        self.ipv4_min = int(net.network_address)
        return super().save(**kwargs)
