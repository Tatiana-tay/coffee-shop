from django.shortcuts import get_object_or_404
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
#from rest_framework.views import APIView
from rest_framework import generics, status
# from rest_framework import mixins
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
#import django_filters.rest_framework
from coffeeshop_app.api.filters import PriceCategoryFilter
from coffeeshop_app.models import (Item, Barista, Farm, FAQ, Review, Category, Size, Ingredient,
                                   ContactUs, About, MailCollector, Gallery)
from coffeeshop_app.api.serializers import (ItemSerializer, ListItemSerializer, BaristaSerializer, 
                                            FarmSerializer, FAQSerializer, ReviewSerializer, 
                                            CategorySerializer, SizeSerializer, IngredientSerializer,
                                            ContactUsSerializer, AboutSerializer,
                                            MailCollectorSerializer, GallerySerializer)


class ItemVS(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PriceCategoryFilter
    search_fields = ['name']
    ordering_fields = ['avg_rating', 'price']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ListItemSerializer
        return ItemSerializer
    

class CategoryVS(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
class SizeVS(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
  
    
class IngredientVS(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    

class BaristaVS(viewsets.ModelViewSet):
    queryset = Barista.objects.all()
    serializer_class = BaristaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['experience_years']
    search_fields = ['name']
    
    
class FarmVS(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['region']
    search_fields = ['name']


class FAQVS(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class ContactUsVS(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    
    
class AboutVS(viewsets.ModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    
    
class MailCollectorVS(viewsets.ModelViewSet):
    queryset = MailCollector.objects.all()
    serializer_class = MailCollectorSerializer
    
    
class GalleryVS(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        item = Item.objects.get(pk=pk)

        #review_user = self.request.user
        # review_queryset = Review.objects.filter(item=item, review_user=review_user)

        # if review_queryset.exists():
        #     raise ValidationError("You have already reviewed this movie!")
        
        review_user = self.request.user
        new_rating = serializer.validated_data['rate']

        # Update total and count
        item.total_rating += new_rating
        item.number_rating += 1

        # Update avg_rating
        item.avg_rating = item.total_rating / item.number_rating
        item.save()

        serializer.save(item=item, review_user=review_user)


class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'rate']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(item=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer