import datetime
import random
from django.shortcuts import get_object_or_404
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
#from rest_framework.views import APIView
from rest_framework import generics, status
# from rest_framework import mixins
from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
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
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['region']
    search_fields = ['name']


class FAQVS(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class ContactUsVS(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    
    def list(self, request, *args, **kwargs):
        return Response(status=405)  # Method Not Allowed

    def destroy(self, request, *args, **kwargs):
        return Response(status=405)  # Method Not Allowed
    
    
# class AboutVS(viewsets.ModelViewSet):
#     queryset = About.objects.all()
#     serializer_class = AboutSerializer
#     parser_classes = (MultiPartParser, FormParser)
    
#     def list(self, request, *args, **kwargs):
#         return Response(status=405)  # Method Not Allowed

#     def destroy(self, request, *args, **kwargs):
#         return Response(status=405)  # Method Not Allowed



class AboutView(APIView):
    serializer_class = AboutSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        try:
            return About.objects.get()
        except About.DoesNotExist:
            raise NotFound("No About object found.")

    def get(self, request):
        about_instance = self.get_object()
        serializer = self.serializer_class(about_instance, context={"request": request})
        return Response(serializer.data)

    def put(self, request):
        about_instance = self.get_object()
        serializer = self.serializer_class(about_instance, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def post(self, request):
        if About.objects.exists():
            return Response({"message": "An About object already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        try:
            about_instance = self.get_object()
            about_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({"message": "No About object to delete."}, status=status.HTTP_404_NOT_FOUND)
    
    
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
    
    
    
    
    
class TodaysPickView(APIView):
    def get(self, request):
        category_ids = list(Category.objects.values_list("id", flat=True))
        if not category_ids:
            return Response({"message": "No categories found."}, status=404)

        today = datetime.date.today()
        day_of_year = today.timetuple().tm_yday
        year = today.year

        # 1. Deterministically shuffle categories for this year
        rng = random.Random(year)
        shuffled_ids = category_ids[:]
        rng.shuffle(shuffled_ids)

        # 2. Pick today's category
        todays_index = (day_of_year - 1) % len(shuffled_ids)
        todays_category_id = shuffled_ids[todays_index]

        try:
            todays_category = Category.objects.get(id=todays_category_id)
        except Category.DoesNotExist:
            return Response({"message": "Category not found."}, status=404)

        # 3. Deterministically pick an item from this category
        items = list(Item.objects.filter(categories=todays_category))
        if not items:
            return Response(
                {"message": f"No items found in category '{todays_category.name}'."},
                status=404,
            )

        rng = random.Random(day_of_year + todays_category_id)  # stable per day
        todays_pick = rng.choice(items)

        # 4. Serialize result
        serializer = ItemSerializer(todays_pick, context={"request": request})
        return Response(serializer.data)