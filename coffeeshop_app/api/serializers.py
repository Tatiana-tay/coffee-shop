from rest_framework import serializers
from coffeeshop_app.models import (Item, Farm, FarmInfo, Barista, Review, FAQ,
                                   Gallery, Category, Size, Ingredient,
                                   ContactUs, About, MailCollector, CoffeeJourney)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "user_name", "email", "rate", "description", "created", "update", "item"]
        read_only_fields = ["id", "created", "update", "item"]

    
        
        
        
class IdNameRelatedField(serializers.PrimaryKeyRelatedField):
    """A field that accepts IDs for input, but returns {id, name} on output."""

    def to_representation(self, value):
        return {"id": value.id, "name": value.name}

        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'
        

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class SimpleItemSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'image', 'avg_rating', 'categories']  # Just basic info

    # def get_image(self, obj):
    #     if obj.image:
    #         return obj.image.url
    #     return None

class ListItemSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    sizes = SizeSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        exclude = ['related_items']

    # def get_image(self, obj):
    #     if obj.image:
    #         return obj.image.url
    #     return None




class ItemSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    categories = IdNameRelatedField(queryset=Category.objects.all(), many=True)
    sizes = IdNameRelatedField(queryset=Size.objects.all(), many=True)
    ingredients = IdNameRelatedField(queryset=Ingredient.objects.all(), many=True)
    related_items = SimpleItemSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "image",
            "price",
            "avg_rating",
            "number_rating",
            "total_rating",
            "description",
            "origin_story",
            "reviews",
            "categories",
            "sizes",
            "ingredients",
            "related_items",
        ]

        
    # def get_image(self, obj):
    #     if obj.image:
    #         return obj.image.url
    #     return None


# class FarmInfoSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(required=False)        # used to find existing rows
#     _delete = serializers.BooleanField(required=False)   # custom flag for deletes
#     # image = serializers.SerializerMethodField()

#     class Meta:
#         model = FarmInfo
#         fields = '__all__'
        
#     # def get_image(self, obj):
#     #     if obj.image:
#     #         return obj.image.url
#     #     return None
    

# class FarmSerializer(serializers.ModelSerializer):
#     info_arr = FarmInfoSerializer(many=True)
#     # image = serializers.SerializerMethodField()
#     class Meta:
#         model = Farm
#         fields = '__all__'
        
#     # def get_image(self, obj):
#     #     if obj.image:
#     #         return obj.image.url
#     #     return None
    
    
#     def create(self, validated_data):
#         info_arr_data = validated_data.pop("info_arr", [])
#         farm = Farm.objects.create(**validated_data)

#         for item in info_arr_data:
#             FarmInfo.objects.create(farm=farm, **{k: v for k, v in item.items() if k != "_delete"})
#         return farm

#     def update(self, instance, validated_data):
#         info_arr_data = validated_data.pop("info_arr", None)

#         # update farm fields
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()

#         if info_arr_data is not None:
#             for item in info_arr_data:
#                 if "id" in item:
#                     try:
#                         info_obj = FarmInfo.objects.get(id=item["id"], farm=instance)
#                     except FarmInfo.DoesNotExist:
#                         continue

#                     # check delete flag
#                     if item.get("_delete", False):
#                         info_obj.delete()
#                         continue

#                     # update fields
#                     info_obj.text = item.get("text", info_obj.text)
#                     if "image" in item:
#                         info_obj.image = item["image"]
#                     info_obj.save()
#                 else:
#                     # create new
#                     FarmInfo.objects.create(farm=instance, **{k: v for k, v in item.items() if k != "_delete"})

#         return instance



class FarmInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmInfo
        fields = ["text", "image"]


class FarmSerializer(serializers.ModelSerializer):
    info_arr = FarmInfoSerializer(many=True)  # nested input

    class Meta:
        model = Farm
        fields = [
            "id",
            "name",
            "image",
            "area",
            "height",
            "temperature",
            "region",
            "map_url",
            "ground_info_img",
            "description",
            "info_arr",         
        ]

    def create(self, validated_data):
        info_data = validated_data.pop("info_arr", [])
        farm = Farm.objects.create(**validated_data)

        for info in info_data:
            FarmInfo.objects.create(farm=farm, **info)

        return farm

    def update(self, instance, validated_data):
        info_data = validated_data.pop("info_arr", None)

        # Update farm itself
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # If info_arr is passed, replace old with new
        if info_data is not None:
            instance.info_arr.all().delete()
            for info in info_data:
                FarmInfo.objects.create(farm=instance, **info)

        return instance



# class NationalitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Nationality
#         fields = ["code", "name"]

# class BaristaSerializer(serializers.ModelSerializer):
#     nationality = NationalitySerializer(many=True)

#     class Meta:
#         model = Barista
#         fields = [
#             "id", "name", "image", "age", "position", "experience_years",
#             "description", "nationality",
#         ]

#     def create(self, validated_data):
#         nationality_data = validated_data.pop("nationality", [])
#         barista = Barista.objects.create(**validated_data)
#         for nationality in nationality_data:
#             Nationality.objects.create(barista=barista, **nationality)
#         return barista

#     def update(self, instance, validated_data):
#         nationality_data = validated_data.pop("nationality", None)
        
#         # Update Barista instance
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()

#         # Update or replace Nationality instances
#         if nationality_data is not None:
#             instance.nationality.all().delete()
#             for nationality in nationality_data:
#                 Nationality.objects.create(barista=instance, **nationality)

#         return instance


class BaristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barista
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()
    class Meta:
        model = Gallery
        fields = '__all__'
        
    # def get_image(self, obj):
    #     if obj.image:
    #         return obj.image.url
    #     return None


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'
        
        
class CoffeeJourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoffeeJourney
        fields = ["title", "description"]

class AboutSerializer(serializers.ModelSerializer):
    coffee_journey = CoffeeJourneySerializer(many=True)

    class Meta:
        model = About
        fields = [
            "id", "our_story", "image", "coffee_journey",
        ]

    def create(self, validated_data):
        journey_data = validated_data.pop("coffee_journey", [])
        about = About.objects.create(**validated_data)
        for journey in journey_data:
            CoffeeJourney.objects.create(about=about, **journey)
        return about

    def update(self, instance, validated_data):
        journey_data = validated_data.pop("coffee_journey", None)
        
        # Update About instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or replace CoffeeJourney instances
        if journey_data is not None:
            instance.coffee_journey.all().delete()
            for journey in journey_data:
                CoffeeJourney.objects.create(about=instance, **journey)

        return instance

        
        
class MailCollectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailCollector
        fields = '__all__'