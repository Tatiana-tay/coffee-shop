from django.urls import path, include
from rest_framework.routers import DefaultRouter
from coffeeshop_app.api.views import (ItemVS, BaristaVS, FarmVS, FAQVS,
                                      ReviewCreate, ReviewList, ReviewDetail,
                                      ContactUsVS, AboutView, CategoryVS, SizeVS,
                                      IngredientVS, MailCollectorVS, GalleryVS, TodaysPickView)



router = DefaultRouter()
router.register('item', ItemVS, basename='item-vs')
router.register('category', CategoryVS, basename='category-vs')
router.register('size', SizeVS, basename='size-vs')
router.register('ingredient', IngredientVS, basename='ingredient-vs')
router.register('barista', BaristaVS, basename='barista-vs')
router.register('farm', FarmVS, basename='farm-vs')
router.register('faq', FAQVS, basename='faq-vs')
router.register('contactus', ContactUsVS, basename='contactus-vs')
router.register('mailcollector', MailCollectorVS, basename='mailcollector-vs')
router.register('gallery', GalleryVS, basename='gallery-vs')


urlpatterns = [
    path('', include(router.urls)),
    
    path("todays-pick/", TodaysPickView.as_view(), name="todays-pick"),
    path('about/', AboutView.as_view(), name='about'),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
]
