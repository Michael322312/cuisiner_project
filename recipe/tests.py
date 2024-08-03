from django.test import TestCase, override_settings
from recipe.models import Recipe, Product
from user_system.models import CustomUser

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class MainPageTest(TestCase):
    def test_main_menu(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class RecipeListTest(TestCase):
    def test_reclist_menu(self):
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, 200)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class RecipeCreateTest(TestCase):
    def test_main_menu(self):
        CustomUser.objects.create(username='username', password='1234')
        self.user = CustomUser.objects.first()
        login = self.client.login(username='username', password='1234')

        Recipe.objects.create(
            author = self.user,
            title='title',
            url_yt_video='youtube.com',
            introduction='intro',
            recipe_text='text',
            is_dividible=True
        )
        recipe=Recipe.objects.first()

        response = self.client.get(f'/recipes/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(recipe.author, 'username')
        self.assertEqual(recipe.url_yt_video, 'youtube.com')
        self.assertEqual(recipe.introduction, 'intro')
        self.assertEqual(recipe.recipe_text, 'text')

        self.assertTrue(recipe.is_dividible)
        
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class RecipeCreateTest(TestCase):
    def test_main_menu(self):
        CustomUser.objects.create(username='username', password='1234')
        self.user = CustomUser.objects.first()
        recipe = Recipe(
            author = self.user,
            title='title',
            url_yt_video='youtube.com',
            introduction='intro',
            recipe_text='text',
            is_dividible=True
        )
        recipe.save()
        response = self.client.get(f'/recipes/{recipe.id}')

        self.assertEqual(Recipe.objects.count(), 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(recipe.author, 'username')
        self.assertEqual(recipe.url_yt_video, 'youtube.com')
        self.assertEqual(recipe.introduction, 'intro')
        self.assertEqual(recipe.recipe_text, 'text')

        self.assertTrue(recipe.is_dividible)