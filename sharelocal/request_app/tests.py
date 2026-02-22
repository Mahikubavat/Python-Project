from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from items.models import Item
from core.models import Category
from .models import ItemRequest


class RequestViewTests(TestCase):
    def setUp(self):
        # create users and item
        self.owner = User.objects.create_user(username='owner', password='pass123')
        self.other = User.objects.create_user(username='other', password='pass456')
        self.category = Category.objects.create(name='Cat')
        self.item = Item.objects.create(
            owner=self.owner,
            title='ReqItem',
            description='Desc',
            category=self.category,
            item_type='Share',
            is_available=True
        )

    def test_block_second_request_if_pending(self):
        # user1 makes initial pending request
        self.client.login(username='other', password='pass456')
        url = reverse('create-request', args=[self.item.id])
        resp = self.client.post(url, follow=True)
        self.assertEqual(ItemRequest.objects.filter(requested_by=self.other, item=self.item).count(), 1)
        # second attempt; should show existing details and not create new
        resp2 = self.client.get(url)
        self.assertContains(resp2, 'Previous Request')
        self.assertContains(resp2, 'Status:')
        # posting again shouldn't create another
        resp3 = self.client.post(url, follow=True)
        self.assertEqual(ItemRequest.objects.filter(requested_by=self.other, item=self.item).count(), 1)

    def test_allow_new_request_after_accepted(self):
        self.client.login(username='other', password='pass456')
        url = reverse('create-request', args=[self.item.id])
        # first request
        self.client.post(url)
        req = ItemRequest.objects.get(requested_by=self.other, item=self.item)
        req.status = 'Accepted'
        req.save()
        # second request should create new entry
        resp = self.client.post(url, follow=True)
        self.assertEqual(ItemRequest.objects.filter(requested_by=self.other, item=self.item).count(), 2)
