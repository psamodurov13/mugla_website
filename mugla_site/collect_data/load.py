# from mugla_site.wsgi import *
import os
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from mugla_site.settings import MEDIA_ROOT, MEDIA_URL

from transliterate import slugify

from companies.models import Company, Type, CompanyTags, CompanyGallery
from cities.models import City
from telegram_notifications.tg_notification import notification
from download_files import download_image
from datetime import date
from loguru import logger
from mugla_site.utils import crop_image, format_image_size


res = {
    'https://www.google.com.tr/maps/place/MEB+%C3%96zel+Marmaris+Pinokyo+Anaokulu/data=!4m7!3m6!1s0x14bfcb5142d100e1:0xdadb263b0de5686a!8m2!3d36.8569963!4d28.2629144!16s%2Fg%2F1tp1dh0b!19sChIJ4QDRQlHLvxQRamjlDTsm29o?authuser=0&hl=ru&rclk=1': {
        'address': 'Kemeraltı, '
                   '112. '
                   'Sk. '
                   'No:27, '
                   '48700 '
                   'Marmaris/Muğla ',
        'category': 'Детский '
                    'сад 2',
        'city': 'Кёйджегиз',
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
        'photos_urls': ['https://sweethomedress.ru/image/cache/catalog/supplier1/ck_cb6_0zwf91vg6xsnl1df7wa82sx1x416am01-1000x1500.webp',
                        'https://lh5.googleusercontent.com/p/AF1QipMTt4E8Cq_Ayp49rtwWZAD6qzyd_b5p0RWOLve-=s878-k-no',
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
        'tags': ['Для детей', 'Для туристов', 'Тестовая'],
        'title': 'Ozel Marmaris Pinokyo Anaokulu',
        'website': ''},
}


def load_companies(res, query, city):
    notification(f'Началась закрузка компаний по запросу "{query}" / {city}. Всего - {len(res)}')
    total = 0
    errors = 0
    for item in res:
        try:
            i = res[item]
            last_id = Company.objects.order_by('id').last().id
            slug = slugify(i['title'], language_code='ru') + str(last_id + 1)
            if Type.objects.filter(title=i['category']).exists():
                company_type = Type.objects.get(title=i['category'])
            else:
                last_id_type = Type.objects.order_by('id').last().id
                company_type = Type.objects.create(title=i['category'],
                                                   slug=slugify(i['category'],
                                                                language_code='ru') + str(last_id_type + 1))
            company = Company.objects.create(author=User.objects.get_by_natural_key('psamodurov13'),
                                             type=company_type,
                                             slug=slug)
            company.title = i['title']
            company.cities.add(City.objects.get(title=i['city']))
            # company.type = Type.objects.get(title=i['category'])
            # company.subtitle = i['subtitle']
            latitude = float(i['location'][1])
            longitude = float(i['location'][0])
            location_data = Point((latitude, longitude))
            company.location = location_data
            company.address = i['address']
            company.phone = i['phone']
            company.site = i['website']
            try:
                company.open_hours = f'ПН: {i["open_hours"]["понедельник"]}\n' \
                             f'ВТ: {i["open_hours"]["вторник"]}\n' \
                             f'СР: {i["open_hours"]["среда"]}\n' \
                             f'ЧТ: {i["open_hours"]["четверг"]}\n' \
                             f'ПТ: {i["open_hours"]["пятница"]}\n' \
                             f'СБ: {i["open_hours"]["суббота"]}\n' \
                             f'ВС: {i["open_hours"]["воскресенье"]}\n'
            except KeyError:
                company.open_hours = ''
            for tag in i['tags']:
                if CompanyTags.objects.filter(title=tag).exists():
                    company.tags.add(CompanyTags.objects.get(title=tag))
                else:
                    last_id = CompanyTags.objects.order_by('id').last().id
                    slug = slugify(tag, language_code='ru') + str(last_id + 1)
                    new_tag = CompanyTags.objects.create(title=tag, slug=slug)
                    notification(f'Создан тег - {tag}')
                    company.tags.add(new_tag)
            company.from_internet = True

            count = 1
            path = f'photo/{date.today().strftime("%Y/%m/%d")}/'
            logger.info(f'ROOT {MEDIA_ROOT}{path}')
            if len(i['photos_urls']) > 0:
                if not os.path.exists(f'{MEDIA_ROOT}/{path}'):
                    os.makedirs(f'{MEDIA_ROOT}/{path}')
            gallery_path = f'company_gallery/{date.today().strftime("%Y/%m/%d")}/'
            if len(i['photos_urls']) > 1:
                if not os.path.exists(f'{MEDIA_ROOT}/{gallery_path}'):
                    os.makedirs(f'{MEDIA_ROOT}/{gallery_path}')
            for img in i['photos_urls']:
                name = str(company.pk) + '-' + str(count)
                if count == 1:
                    logger.info(f'PATH - {path}')
                    link = path + download_image(img, name, f'{MEDIA_ROOT}/{path}')
                    logger.info(f'LINK - {link}')
                    company.photo = link
                    logger.info(f'Добавлено главное фото {link}')
                    cropping_thumb = format_image_size(f'{MEDIA_ROOT}/{link}', 4 / 3)
                    logger.info(f'CROPPING {cropping_thumb}')
                    company.cropping_thumb = cropping_thumb
                else:
                    gallery_link = gallery_path + download_image(img, name, f'{MEDIA_ROOT}/{gallery_path}')
                    CompanyGallery.objects.create(image=gallery_link,
                                                  company=company, is_published=True)
                    logger.info(f'Добавлено в галерею {gallery_link}')
                count += 1
            company.content = ''
            company.is_published = True
            company.google_link = item
            company.save()
            total += 1
        except Exception:
            logger.exception(f'Ошибка при загрузке компании {Exception}')
            errors += 1
    notification(f'Загрузка компаний по запросу "{query}" / {city} завершена.\n'
                 f'Всего - {len(res)}\nЗагружено - {total}\nОшибок - {errors}')


if __name__ == '__main__':
    load_companies(res, 'anaokulu marmaris', 'Мармарис')

