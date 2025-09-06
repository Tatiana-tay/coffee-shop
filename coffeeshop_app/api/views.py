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


# class ReviewList(generics.ListAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['review_user__username', 'rate']

#     def get_queryset(self):
#         pk = self.kwargs['pk']
#         return Review.objects.filter(item=pk)


# class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
     
    

# class ReviewCreate(generics.CreateAPIView):
#     serializer_class = ReviewSerializer

#     def get_queryset(self):
#         return Review.objects.all()

#     def perform_create(self, serializer):
#         pk = self.kwargs.get("pk")
#         item = Item.objects.get(pk=pk)

#         email = serializer.validated_data["email"]  # take from request

#         # ✅ Check if this email already reviewed this item
#         if Review.objects.filter(item=item, email=email).exists():
#             raise ValidationError("This email has already reviewed this item!")

#         new_rating = serializer.validated_data["rate"]

#         # Update item ratings
#         item.total_rating += new_rating
#         item.number_rating += 1
#         item.avg_rating = item.total_rating / item.number_rating
#         item.save()

#         serializer.save(item=item)


            
            

# class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def perform_update(self, serializer):
#         instance = self.get_object()
#         item = instance.item

#         old_rating = instance.rate
#         new_rating = serializer.validated_data.get("rate", old_rating)

#         # Prevent email change
#         if "email" in serializer.validated_data and serializer.validated_data["email"] != instance.email:
#             raise ValidationError("You cannot change the email of a review.")

#         # Update item rating correctly
#         item.total_rating = item.total_rating - old_rating + new_rating
#         item.avg_rating = item.total_rating / item.number_rating
#         item.save()

#         serializer.save()

    # def perform_destroy(self, instance):
    #     item = instance.item

    #     # Adjust totals when deleting review
    #     item.total_rating -= instance.rate
    #     item.number_rating -= 1

    #     if item.number_rating > 0:
    #         item.avg_rating = item.total_rating / item.number_rating
    #     else:
    #         item.avg_rating = 0  # reset if no reviews left

    #     item.save()
    #     instance.delete()

        
        
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        item = Item.objects.get(pk=pk)

        email = serializer.validated_data["email"]
        new_rating = serializer.validated_data["rate"]

        # Check if this email already has a review for this item
        try:
            existing_review = Review.objects.get(item=item, email=email)

            # Adjust totals (subtract old, add new)
            item.total_rating = item.total_rating - existing_review.rate + new_rating
            item.avg_rating = item.total_rating / item.number_rating
            item.save()

            # ✅ Update the existing review instead of creating a new one
            existing_review.rate = new_rating
            existing_review.description = serializer.validated_data.get("description", existing_review.description)
            existing_review.save()

        except Review.DoesNotExist:
            # ✅ First time this email reviews this item → create new
            item.total_rating += new_rating
            item.number_rating += 1
            item.avg_rating = item.total_rating / item.number_rating
            item.save()

            serializer.save(item=item)
            
            
class ReviewDetail(generics.RetrieveDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_destroy(self, instance):
        item = instance.item

        # Adjust totals
        item.total_rating -= instance.rate
        item.number_rating -= 1
        item.avg_rating = item.total_rating / item.number_rating if item.number_rating > 0 else 0
        item.save()

        instance.delete()
        
        
        
class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email', 'rate']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(item=pk)
    
    
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

        # 3. Deterministically pick 3 items from this category
        items = list(Item.objects.filter(categories=todays_category))
        if not items:
            return Response(
                {"message": f"No items found in category '{todays_category.name}'."},
                status=404,
            )

        rng = random.Random(day_of_year + todays_category_id)  # stable per day
        rng.shuffle(items)  # shuffle deterministically
        todays_picks = items[:3]  # take the first 3 (or fewer if not enough items)

        # 4. Serialize result
        serializer = ItemSerializer(todays_picks, many=True, context={"request": request})
        return Response({
            "category": todays_category.name,
            "items": serializer.data
        })
