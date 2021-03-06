# coding=utf-8
import re
import random

from django import template
from django.core.urlresolvers import reverse, NoReverseMatch

from utils import vkontakte, formatters, facebook


register = template.Library()

@register.simple_tag
def random_choice(*args):
    return random.choice(args)


# Определяет активный пункт меню
@register.simple_tag(takes_context=True)
def active(context, urlname):
    try:
        pattern = '^' + reverse(urlname)
    except NoReverseMatch:
        pattern = urlname
    path = context.get('request').path
    if re.search(pattern, path):
        return 'active'
    return ''


@register.simple_tag
def vkontakte_auth_link(redirect_uri):
    return vkontakte.build_login_link(redirect_uri)


@register.simple_tag
def vkontakte_profile_link(vkuserid):
    vkuserid = str(vkuserid)
    return 'http://vk.com/' + 'id' * vkuserid.isdigit() + vkuserid

@register.simple_tag
def facebook_auth_link(redirect_uri):
    return facebook.build_login_link(redirect_uri)


@register.simple_tag
def facebook_profile_link(fbuserid):
    fbuserid = str(fbuserid)
    return 'https://www.facebook.com/' + fbuserid


@register.inclusion_tag('tagtemplates/avatar.html')
def avatar(avatar_img, height='', width='', circle=False, sex='m', thumbnail=False):
    height = str(height)
    width = str(width)
    return {'avatar': avatar_img, 'circle': circle, 'width': width, 'height': height, 'sex': sex, 'thumbnail': thumbnail}


@register.inclusion_tag('tagtemplates/image.html')
def image(img, height='', width='', thumbnail=False):
    height = str(height)
    width = str(width)
    return {'image': img, 'width': width, 'height': height, 'thumbnail': thumbnail}


@register.filter(name='beauty_phone')
def beauty_phone(value):
    phone = value.__str__()
    return phone[:2] + ' (' + phone[2:5] + ') ' + phone[5:8] + '-' + phone[8:10] + '-' + phone[10:12]


@register.filter(name='beauty_age')
def beauty_age(value):
    return formatters.show_years(value)