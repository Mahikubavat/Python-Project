from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile
from .models import Item
from .forms import ItemForm
from core.models import Category


class ItemViewTests(TestCase):
    def setUp(self):
        # create an owner with profile
        self.owner = User.objects.create_user(username='owner', password='pass123', email='owner@example.com', first_name='Owner')
        UserProfile.objects.create(user=self.owner, phone='1234567890', location='Test City')
        self.other = User.objects.create_user(username='other', password='pass456', email='other@example.com')
        self.category = Category.objects.create(name='TestCat')
        self.item = Item.objects.create(
            owner=self.owner,
            title='Test Item',
            description='A test item',
            category=self.category,
            item_type='Share',
            price=100.00,  # nonzero to exercise currency display
            is_available=True
        )

    def test_item_detail_includes_contact_and_owner(self):
        url = reverse('item_detail', args=[self.item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # owner name present
        self.assertContains(response, 'Owner:')
        self.assertContains(response, 'Owner')
        # item type display should be give away text
        self.assertContains(response, 'Give Away')
        # phone number should NOT be shown directly
        self.assertNotContains(response, '1234567890')
        # email still present
        self.assertContains(response, 'owner@example.com')

    def test_request_button_in_detail_for_nonowner(self):
        self.client.login(username='other', password='pass456')
        url = reverse('item_detail', args=[self.item.id])
        response = self.client.get(url)
        self.assertContains(response, reverse('create-request', args=[self.item.id]))

    def test_request_button_in_list_card(self):
        self.client.login(username='other', password='pass456')
        url = reverse('item_list')
        response = self.client.get(url)
        self.assertContains(response, reverse('create-request', args=[self.item.id]))

    def test_currency_symbol_shown_and_price_rules(self):
        # when price is present currency symbol should be the rupee sign
        response = self.client.get(reverse('item_detail', args=[self.item.id]))
        self.assertContains(response, '₹')
        self.assertNotContains(response, '$')

    def test_form_validation_price_for_giveaway(self):
        # 'Share' type should clear price and not accept a value
        form_data = {
            'title': 'Test2',
            'description': 'desc',
            'category': self.category.id,
            'item_type': 'Share',
            'price': '100.00'
        }
        form = ItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)
        # selling requires price
        form_data['item_type'] = 'Sell'
        form_data['price'] = ''
        form2 = ItemForm(data=form_data)
        self.assertFalse(form2.is_valid())
        self.assertIn('price', form2.errors)
