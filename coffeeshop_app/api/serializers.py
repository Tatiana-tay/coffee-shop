from rest_framework import serializers
from coffeeshop_app.models import (Item, Farm, FarmInfo, Barista, Review, FAQ,
                                   Gallery, Category, Size, Ingredient,
                                   ContactUs, About, MailCollector, 
                                   Nationality, CoffeeJourney)

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        
        
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
    # image = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    sizes = SizeSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    related_items = SimpleItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Item
        fields = '__all__'
        
    # def get_image(self, obj):
    #     if obj.image:
    #         return obj.image.url
    #     return None


class FarmInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)        # used to find existing rows
    _delete = serializers.BooleanField(required=False)   # custom flag for deletes
    # image = serializers.SerializerMethodField()

    class Meta:
        model = FarmInfo
        fields = '__all__'
        
    # def get_image(self, obj):
    #     if obj.image:
    #         return obj.image.url
    #     return None
    

class FarmSerializer(serializers.ModelSerializer):
    info_arr = FarmInfoSerializer(many=True)
    # image = serializers.SerializerMethodField()
    class Meta:
        model = Farm
        fields = '__all__'
        
    # def get_image(self, obj):
    #     if obj.image:
    #         return obj.image.url
    #     return None
    
    
    def create(self, validated_data):
        info_arr_data = validated_data.pop("info_arr", [])
        farm = Farm.objects.create(**validated_data)

        for item in info_arr_data:
            FarmInfo.objects.create(farm=farm, **{k: v for k, v in item.items() if k != "_delete"})
        return farm

    def update(self, instance, validated_data):
        info_arr_data = validated_data.pop("info_arr", None)

        # update farm fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if info_arr_data is not None:
            for item in info_arr_data:
                if "id" in item:
                    try:
                        info_obj = FarmInfo.objects.get(id=item["id"], farm=instance)
                    except FarmInfo.DoesNotExist:
                        continue

                    # check delete flag
                    if item.get("_delete", False):
                        info_obj.delete()
                        continue

                    # update fields
                    info_obj.text = item.get("text", info_obj.text)
                    if "image" in item:
                        info_obj.image = item["image"]
                    info_obj.save()
                else:
                    # create new
                    FarmInfo.objects.create(farm=instance, **{k: v for k, v in item.items() if k != "_delete"})

        return instance



class NationalitySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Nationality
        fields = '__all__'
        
    
    def create(self, validated_data):
        nationalities_data = validated_data.pop("nationalities", [])
        barista = Barista.objects.create(**validated_data)
        for nat in nationalities_data:
            Nationality.objects.create(barista=barista, **nat)
        return barista

    def update(self, instance, validated_data):
        nationalities_data = validated_data.pop("nationalities", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if nationalities_data is not None:
            existing_ids = [item["id"] for item in nationalities_data if "id" in item]
            instance.nationalities.exclude(id__in=existing_ids).delete()

            for item in nationalities_data:
                if "id" in item:
                    nat = Nationality.objects.get(id=item["id"], barista=instance)
                    nat.code = item.get("code", nat.code)
                    nat.name = item.get("name", nat.name)
                    nat.save()
                else:
                    Nationality.objects.create(barista=instance, **item)

        return instance



class BaristaSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()
    nationalities = NationalitySerializer(many=True)
    
    class Meta:
        model = Barista
        fields = '__all__'
        
    # def get_image(self, obj):
    #     if obj.image:
    #         return obj.image.url
    #     return None



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
        fields = ["photo", "description"]


class AboutSerializer(serializers.ModelSerializer):
    coffee_journey = CoffeeJourneySerializer(many=True)

    class Meta:
        model = About
        fields = ["our_story", "image", "coffee_journey"]

    def create(self, validated_data):
        journey_data = validated_data.pop("coffee_journey")
        about = About.objects.create(**validated_data)
        for journey in journey_data:
            CoffeeJourney.objects.create(about=about, **journey)
        return about

    def update(self, instance, validated_data):
        journey_data = validated_data.pop("coffee_journey", None)

        # update About fields
        instance.our_story = validated_data.get("our_story", instance.our_story)
        instance.image = validated_data.get("image", instance.image)
        instance.save()

        if journey_data is not None:
            # clear old journeys and replace with new
            instance.coffee_journey.all().delete()
            for journey in journey_data:
                CoffeeJourney.objects.create(about=instance, **journey)

        return instance

        
        
class MailCollectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailCollector
        fields = '__all__'