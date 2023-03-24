# from django.conf import settings
#
# settings.configure()
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mugla_site.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.contrib.auth.models import User
from django.contrib.gis.db import models as models_loc
from django.contrib.gis.geos import Point

from transliterate import slugify

from companies.models import Company, Type


res = {
    'https://www.google.com.tr/maps/place/MEB+%C3%96zel+Marmaris+Pinokyo+Anaokulu/data=!4m7!3m6!1s0x14bfcb5142d100e1:0xdadb263b0de5686a!8m2!3d36.8569963!4d28.2629144!16s%2Fg%2F1tp1dh0b!19sChIJ4QDRQlHLvxQRamjlDTsm29o?authuser=0&hl=ru&rclk=1': {
        'address': 'Kemeraltı, '
                   '112. '
                   'Sk. '
                   'No:27, '
                   '48700 '
                   'Marmaris/Muğla ',
        'category': 'Детский '
                    'сад',
        'location': ['36.8569963',
                     '28.2629144'],
        'open_hours': {'воскресенье': 'Закрыто',
                       'вторник': '07:30–17:30',
                       'понедельник': '07:30–17:30',
                       'пятница': '07:30–17:30',
                       'среда': '07:30–17:30',
                       'суббота': 'Закрыто',
                       'четверг': '07:30–17:30'},
        'phone': '05321709812',
        'photos_urls': ['https://lh5.googleusercontent.com/p/AF1QipMTt4E8Cq_Ayp49rtwWZAD6qzyd_b5p0RWOLve-=s878-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipNKy568pJTq6wsm5iR3jsSNDOJkISnPhGRRwsyu=s1105-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipOZ_LreYSc8g5vYNQGXMD1337nuCB-Hywrx6dEV=s1031-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipMFcWSL7XWnhZ-EY48V8lrhxg8cmfH6ctFY94HB=s1031-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipPQOOKlYFqm4mHMoypoAdSeAksRuE-pfG0A_igh=s871-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipM49L29UVUoNzwFU4BrYmwu3NAmu5vkz_kT3IfF=s1031-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipNI-FasHjTouoELght88BJLXVRgihc-dcGIWuum=s1031-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipMlmSM29f6hGP-kvvUsL8KDeltxrYJ7Mh7JIed3=s873-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipM91pGysY_1oZb2Rg5NE5qPk9myO2-Nfuevr9qy=s1031-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipN4sa3YWfhABKgnV1-9KaIkXFOtC7NtLiKnj66D=s1031-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipMr-GGfCVVIkPQw2OYmZ2QW5omxgkVc0qp-AnsN=s1031-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipOdmPKtOvFAB7d8D7RzXd2wTFoTwHyjW2CqLbHm=s1022-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipNjFz3mHOXor7tN3Trey8MjvsQ5ZqerL-ztGuAx=s869-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipPb-tu2c0hi1yBAC7UoGiTSfSuZHl0pKXdwmSvA=s1031-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipMSqfWtFJBbhI-W6tx76-DbM3Yto7JnLxEI1Txu=s1013-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipPO8_d1RnicTeDe1emhgw1PcHQUD7jIdtqcNHuA=s1031-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipO0azADVyz1W4cMFFvFRUAkmYEnZQlv2UMyVx45=s869-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipPbGGvTuocx-cJoOjobU6KaawU6qSqjXelDcft0=s812-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipPs3htz1tk6SNB9fRWoFp4oKujaANc84C5Y-A_9=s869-k-no',
                        'https://lh5.googleusercontent.com/p/AF1QipP6J6l2fPuoTztXUB31Hq98i3-c_u_aLn-u_lrn=s1354-k-no'],
        'subtitle': 'MEB '
                    'Özel '
                    'Marmaris '
                    'Pinokyo '
                    'Anaokulu',
        'tags': [],
        'title': 'Ozel Marmaris Pinokyo Anaokulu',
        'website': ''},
}


def load_companies(res):
    for i in res.values():
        last_id = Company.objects.order_by('id').last().id
        slug = slugify(i['title'], language_code='ru') + str(last_id + 1)

        company = Company.objects.create(author=User.objects.get_by_natural_key('psamodurov13'),
                                         type=Type.objects.get(title='Образование'),
                                         slug=slug)
        company.title = i['title']
        # company.type = Type.objects.get(title=i['category'])
        # company.subtitle = i['subtitle']
        latitude = float(i['location'][1])
        longitude = float(i['location'][0])
        location_data = Point((latitude, longitude))
        company.location = location_data
        # company.type = 1
        company.content = ''
        # company.author = User.objects.get_by_natural_key('psamodurov13')
        company.save()


if __name__ == '__main__':
    load_companies(res)

