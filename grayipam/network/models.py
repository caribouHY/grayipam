from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, validate_ipv4_address
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

    def __str__(self) -> str:
        return self.ipv4_cidr

    def get_absolute_url(self):
        return reverse('network:network_detail', kwargs={'pk': self.id})

    def get_prefix(self):
        return ipaddress.IPv4Network(self.ipv4_cidr).prefixlen

    def save(self, **kwargs):
        net = ipaddress.IPv4Network(self.ipv4_cidr)
        self.ipv4_max = int(net.broadcast_address)
        self.ipv4_min = int(net.network_address)
        return super().save(**kwargs)


class Host(models.Model):
    hostname = models.CharField(
        verbose_name='ホスト名', max_length=64, null=True, blank=True)
    ipv4 = models.CharField(
        verbose_name='IPv4アドレス', max_length=15, unique=True, validators=[validate_ipv4_address])
    ipv4_number = models.IntegerField(unique=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE, related_name='host', verbose_name='ネットワーク')

    class Meta:
        ordering = ['ipv4_number']
        verbose_name = 'ホスト'

    def __str__(self) -> str:
        if self.hostname is None or self.hostname == '':
            return self.ipv4
        return '{} ({})'.format(self.hostname, self.ipv4)

    def clean(self):
        num = int(ipaddress.IPv4Address(str(self.ipv4)))
        if num <= self.network.ipv4_min or self.network.ipv4_max <= num:
            raise ValidationError('IPv4アドレスがネットワークの範囲外です。')
        return super().clean()

    def save(self, **kwargs):
        self.ipv4_number = int(ipaddress.IPv4Address(str(self.ipv4)))
        return super().save(**kwargs)

    def get_absolute_url(self):
        return reverse('network:network_detail', kwargs={'pk': self.network.id})
