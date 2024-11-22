from rest_framework import serializers
from .models import User, Franchisee


class FranchiseeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchisee
        fields = ['about', 'revenue', 'dealers', 'service_providers', 'type', 'status', 'verification_id', 'verificationid_number', 'community_name']





class userSerializer(serializers.ModelSerializer):

    franchasees = FranchiseeSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'is_franchisee', 'full_name', 'address', 'landmark', 'place',
            'pin_code', 'district', 'state', 'watsapp', 'email', 'phone_number',
            'country_code', 'franchasees', 'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        franchisee_data = validated_data.pop('franchasees', [])

        # Create the User instance
        user = User.objects.create_user(
            is_franchisee=validated_data['is_franchisee'],
            full_name=validated_data['full_name'],
            address=validated_data['address'],
            landmark=validated_data['landmark'],
            place=validated_data['place'],
            pin_code=validated_data['pin_code'],
            district=validated_data['district'],
            state=validated_data['state'],
            watsapp=validated_data['watsapp'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            country_code=validated_data['country_code'],
            password=validated_data['password'],
        )


        for franchisee in franchisee_data:
            Franchisee.objects.create(user=user, **franchisee)

        return user


