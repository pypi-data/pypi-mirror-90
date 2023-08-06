============
Aparnik
============

Aparnik is a simple Django app to help about some common problems. For each
question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Use your custom module.

2. Add dependency:

    INSTALLED_APPS = [
    
        'azbankgateways',
        
        's3direct',

        'polymorphic',

        'fcm_django',

        'rest_framework',

        'jalali_date',

        'dynamic_raw_id',

        'django_filters',

        'ckeditor',

        'ckeditor_uploader',

        'tagulous',

        'colorfield',

        # app
        'aparnik',

        'aparnik.contrib.suit',

        'aparnik.contrib.users',
        
        'aparnik.contrib.audits',

        'aparnik.contrib.addresses',

        'aparnik.contrib.bankaccounts',

        'aparnik.contrib.managements',

        'aparnik.contrib.aboutus',

        'aparnik.contrib.contactus',

        'aparnik.contrib.province',

        'aparnik.contrib.invitations',

        'aparnik.contrib.basemodels',

        'aparnik.contrib.filefields',

        'aparnik.contrib.bookmarks',

        'aparnik.contrib.reviews',

        'aparnik.contrib.questionanswers',

        'aparnik.contrib.socials',

        'aparnik.contrib.sliders',

        'aparnik.contrib.settings',

        'aparnik.contrib.counters',

        'aparnik.contrib.notifications',
        
        'aparnik.contrib.messaging',
        
        'aparnik.contrib.chats',

        'aparnik.contrib.notifiesme',

        'aparnik.contrib.shortblogs',

        'aparnik.contrib.supports',

        'aparnik.contrib.faq',

        'aparnik.contrib.termsandconditions',

        'aparnik.contrib.segments',

        'aparnik.contrib.buttons',

        'aparnik.contrib.categories',

        'aparnik.contrib.pages',

        'aparnik.packages.shops.products',

        'aparnik.packages.shops.productssharing',

        'aparnik.packages.bankgateways.zarinpals',

        'aparnik.packages.shops.payments',

        'aparnik.packages.shops.subscriptions',

        'aparnik.packages.shops.orders',

        'aparnik.packages.shops.coupons',

        'aparnik.packages.shops.cosales',

        'aparnik.packages.shops.vouchers',

        'aparnik.packages.shops.files',

        'aparnik.packages.educations.books',

        'aparnik.packages.educations.educations',

        'aparnik.packages.educations.teachers',

        'aparnik.packages.educations.courses',

        'aparnik.packages.educations.progresses',

        'aparnik.packages.news',
        ]

3. Add config to settings if you want:
```
    APARNIK = {

        'API_PRODUCT_MODE': True,
        'AWS_ACTIVE': True,
        'BANK_ACTIVE': True,
    }

    CKEDITOR_CONFIGS = {
        'basic': {
            'toolbar': 'Basic',
        },
    }

    CKEDITOR_UPLOAD_PATH = "/"

    FCM_DJANGO_SETTINGS = {
        'FCM_SERVER_KEY': NOTIFICATION_API_KEY,
         # true if you want to have only one active device per registered user at a time
         # default: False
        'ONE_DEVICE_PER_USER': False,
         # devices to which notifications cannot be sent,
         # are deleted upon receiving error response from FCM
         # default: False
        'DELETE_INACTIVE_DEVICES': False,
    }


    # Amazon
    AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
            'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
            'Cache-Control': 'max-age=94608000',
    }

    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    if not AWS_SECRET_ACCESS_KEY or not AWS_ACCESS_KEY_ID or not AWS_STORAGE_BUCKET_NAME:
            raise ValueError('AWS KEY does not set')

    S3DIRECT_REGION = os.environ.get('S3DIRECT_REGION', 'us-east-1')


    # Tell django-storages that when coming up with the URL for an item in S3 storage, keep
    # it simple - just use this domain plus the path. (If this isn't set, things get complicated).
    # This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
    # We also use it in the next setting.
    # AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_CUSTOM_DOMAIN = 's3-%s.amazonaws.com/%s' % (S3DIRECT_REGION, AWS_STORAGE_BUCKET_NAME)
    # This is used by the `static` template tag from `static`, if you're using that. Or if anything else
    # refers directly to STATIC_URL. So it's safest to always set it.
    # #
    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
    # #
    # STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # STATIC_URL = '/static/'

    # MEDIA
    MEDIAFILES_LOCATION = 'media'
    MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

    def create_filename(filename):
        import uuid
        ext = filename.split('.')[-1]
        filename = '%s.%s' % (uuid.uuid4().hex, ext)
        return os.path.join('files', filename)

    def create_file_filename(filename):
        import uuid
        ext = filename.split('.')[-1]
        filename = '%s.%s' % (uuid.uuid4().hex, ext)
        return os.path.join('file', filename)


    S3DIRECT_DESTINATIONS = {
        # Allow anybody to upload any MIME type
        # 'misc': {
        #     'key': '/'
        # },

        # Allow staff users to upload any MIME type
        # 'pdfs': {
        #     'key': 'uploads/pdfs',
        #     'auth': lambda u: u.is_staff
        # },

        # Allow anybody to upload jpeg's and png's. Limit sizes to 500b - 4mb
        'images': {
            # 'key': 'uploads/images',
            'key': create_filename,
            'auth': lambda u: u.is_authenticated,
            'allowed': [
                'image/jpeg',
                'image/png'
            ],
            'content_length_range': (500, 4000000),
        },

        # Allow authenticated users to upload mp4's
        'videos': {
            # 'key': 'uploads/videos',
            'key': create_filename,
            'auth': lambda u: u.is_authenticated,
            'allowed': ['video/mp4']
        },

        'file': {
            # 'key': 'uploads/videos',
            'key': create_file_filename,
            'auth': lambda u: u.is_authenticated,
            # TODO: add mime type
            # 'allowed': ['application/octet-stream ipa']
        },
        # Allow anybody to upload any MIME type with a custom name function
        # 'custom_filename': {
        #     'key': create_filename
        # },
    }

```

4. Add to urls

```
    url(r'^admin/dynamic_raw_id/', include('dynamic_raw_id.urls')),
    url(r'^api/v1/aparnik/', include('aparnik.urls.api', namespace='aparnik-api')),
    url(r'^aparnik/', include('aparnik.urls.urls', namespace='aparnik')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
```

5. Add clock to procfile

6. Add line below to wsgi.py:

    from aparnik.clock import *

7. Add settings key:

    'LOGO_PROJECT_ICON' = 'https://cdn.aparnik.com/static/website/img/logo-persian.png' # لوگو
    'SERVER_NAME' = 'educationtest.aparnik.com' # آدرس سایت
    'SERVER_PORT' = '80' # پورت سایت
    'PRODUCT_WALLET_ID' = 168 # شارژ کیف پول
    'COURSE_LEVEL' = 2 # سطح دوره
    'INVITER_GIFT_CREDITS_PER_PURCHASE' = 0 # درصد اعتبار هدیه برای دعوت کننده به ازای هر خرید
    'INVITER_GIFT_CREDITS' = 20000 # اعتبار هدیه برای دعوت کننده در بدو قبول دعوت تومان
    'PRICE_FORMAT' = '%ic=t:%se=,:%cu=t:%gr=3:%tr=True:%abbr=True' # فرمت قیمت ها
    'PRICE_PRODUCT_FREE_DESCRIPTION' = 'Free' # عنوان کالاهای رایگان
    'PRICE_PRODUCT_SHARING_DESCRIPTION' = 'Shared' # عنوان کالاهایی که دعوت شده اند
    'PRICE_PRODUCT_BUY_DESCRIPTION' = 'Bought' # عنوان کالاهای خریداری شده

8. Add this line to url

    handler404 = 'aparnik.contrib.suit.views.handler404'
    handler500 = 'aparnik.contrib.suit.views.handler500'

9. Config `azbankgateways`

# notifications settings
NOTIFICATIONS_CHANNELS = {
    'websocket': 'aparnik.contrib.chats.channels.BroadCastWebSocketChannel'
}
more read notification/messaging in aparnik.contrib.messaging.readme

# run
celery -A chatire worker -l info
uwsgi --http :8081 --gevent 2 --module websocket --gevent-monkey-patch --master
