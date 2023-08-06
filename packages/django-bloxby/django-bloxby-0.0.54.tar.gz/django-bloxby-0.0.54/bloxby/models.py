import io
from json import JSONDecodeError

import magic
import requests
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models

from bloxby.managers import UserBridgeManager
from bloxby.functions import Bloxby
from bloxby.utils import replace_links, extract_zip

bloxby = Bloxby()


class UserBridge(models.Model):
    """You can create this at post_save of PurchasedPackage or something similar, a model that represents that the user
    has purchased a package, and delete it also at post_delete"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bloxby_id = models.IntegerField(blank=True, null=True)
    autologin_token = models.CharField(max_length=20, blank=True, null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = UserBridgeManager()

    def __str__(self):
        return f'{self.user.email} - {self.bloxby_id}'

    class Site:
        def __init__(self, sites_id, users_id, sites_name, sitethumb, sites_lastupdate_on):
            self.sites_id = sites_id
            self.users_id = users_id
            self.sites_name = sites_name
            self.sitethumb = sitethumb
            self.sites_lastupdate_on = sites_lastupdate_on

    @property
    def dashboard_url(self):
        if self.active:
            url = settings.BLOXBY_BUILDER['url']
            token = self.autologin_token
            hash_string = bloxby.generate_login_hash()
            if not token:
                token = self.create(self.user).autologin_token
            return f"{url}/auth/alogin/?token={token}&hash={hash_string}"
        return '#'

    def delete(self, using=None, keep_parents=False):
        bloxby.Users.update(self.bloxby_id, status='Inactive')
        self.active = False
        self.save()

    @classmethod
    def create_remote(cls, user, package_id, user_bridge):
        data, success = bloxby.Users.create(
            user.first_name, user.last_name, user.email, bloxby.generate_random_password(), package_id
        )
        if success:
            user_bridge.bloxby_id = data['data']['user']['id']
            user_bridge.autologin_token = data['data']['user']['auto_login_token']
            user_bridge.save()
        return data, success

    @classmethod
    def create(cls, user, package_id=None):
        if not package_id:
            package_id = settings.BLOXBY_BUILDER['default_package_id']
        """
        Package_id is the bloxby package id not the internal one
        Simply call UserBridge.create(package_id, user);
        """
        # Check if user already exists in bloxby
        existings = cls.objects.everything().filter(user=user)
        if existings.exists():
            obj = existings.first()
            obj.active = True
            obj.save()
            new = obj
            exists_remote = True
            if obj.bloxby_id:
                data, is_success = bloxby.Users.update(obj.bloxby_id, status='Active')
                if 'does not belong to a valid user' in str(data):
                    exists_remote = False
            else:
                exists_remote = False
            if not exists_remote:
                cls.create_remote(user, package_id, obj)
        else:
            # Check if email already exists there
            new = cls.objects.create(user=user, override=True)
            data, success = cls.create_remote(user, package_id, new)
            if not success:
                if 'email already used' in str(data):
                    # Hack to find the user again. Not efficient but we have to work with what we have
                    bloxby_users, _ = bloxby.Users.all()
                    for bu in bloxby_users:
                        if user.email in bu['email']:
                            new.bloxby_id = bu['id']
                            new.autologin_token = bu['auto_login_token']
                            new.save()
                            break
        return new

    def user_templates(self):
        base_url = settings.BLOXBY_BUILDER.get('custom_api_url', 'http://159.65.79.47:3000')
        response = requests.get(f'{base_url}/{self.autologin_token}/templates')
        sites = []
        try:
            json_data = response.json()
        except JSONDecodeError:
            json_data = []
        if json_data and isinstance(json_data, list):
            for temp in response.json():
                sites.append(
                    self.Site(
                        temp['sites_id'],
                        temp['users_id'],
                        temp['sites_name'],
                        f'{settings.BLOXBY_BUILDER["url"]}/{temp["sitethumb"]}',
                        temp['sites_lastupdate_on']
                    )
                )
        return sites

    def save_site_from_remote(self, site_id, target, obj_id=None):
        Template.objects.filter(owner=self.user, obj_id=obj_id, target=target, remote_id=site_id).delete()
        template = Template.objects.create(owner=self.user, obj_id=obj_id, target=target, remote_id=site_id)
        base_url = settings.BLOXBY_BUILDER.get('custom_api_url', 'http://159.65.79.47:3000')
        response = requests.get(f'{base_url}/{site_id}/export')
        site_archive = io.BytesIO(response.content)
        unzipped = extract_zip(site_archive)
        for key, file in unzipped.items():
            content_type = magic.from_buffer(file, True)
            file = SimpleUploadedFile(key.split('/')[-1], file, content_type)
            if key.endswith('.html'):
                Page.objects.create(
                    template=template, name=key, html=file, is_built=False
                )
            else:
                TemplateAsset.objects.create(template=template, initial_path=key, file=file)


class Template(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    preview = models.FileField(upload_to='sc', null=True, blank=True)
    target = models.CharField(max_length=100)
    obj_id = models.IntegerField(null=True, blank=True)
    remote_id = models.IntegerField(null=True, blank=True, help_text='ID of the template on the remote server.')

    @property
    def index_page(self):
        index_page = self.page_set.filter(name__endswith='index.html')
        if index_page.exists():
            return index_page.first()
        return None


class Page(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    html = models.FileField(upload_to='template-pages', null=True, blank=True, max_length=500)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, null=True, blank=True)
    is_built = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def process(self):
        replace_links(self)
        self.is_built = True
        self.save()

    def render(self):
        if not self.is_built:
            # The processing should only execute once for each page, and that is at first request
            self.process()
        return self.html.read()

    def absolute_url(self, base_path='/'):
        return f'{base_path}?page={self.name}'


class TemplateAsset(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    initial_path = models.CharField(max_length=300, help_text='This is the initial path in the html tag')
    file = models.FileField(upload_to='template-assets', max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.initial_path} - {self.file.url}'
