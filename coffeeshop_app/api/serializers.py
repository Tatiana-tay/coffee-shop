from rest_framework import serializers
from coffeeshop_app.models import Item, Farm, Barista, Review, FAQ, Gallery


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        

class ItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Item
        fields = '__all__'
        
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = '__all__'


class BaristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barista
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'





