# accounts/serializers.py
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser, Employee, Employer, Admin, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']  # Include user_type
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user is None:
            raise serializers.ValidationError("Invalid username/password")
        return user


class EmployeeSerializer(serializers.ModelSerializer):
    # user = UserSerializer(required=True)
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=False)

    class Meta:
        model = Employee
        fields = ['date_of_birth', 'gender', 'phone_number', 'city_name', 'biography', 'user', 'latitude', 'longitude']


class EmployerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=False)

    class Meta:
        model = Employer
        fields = ['vat_number', 'company_name', 'street_name', 'house_number',
                  'city', 'postal_code', 'coordinates', 'website', 'biography', 'user']


class AdminSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=False)

    class Meta:
        model = Admin
        fields = ['full_name', 'user']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['employee', 'employer', 'anonymous_name', 'rating', 'comment', 'reviewer_type']

    def validate(self, attrs):
        # Ensure either employee or anonymous_name is provided
        if not attrs.get('employee') and not attrs.get('anonymous_name'):
            raise serializers.ValidationError("Either an employee or an anonymous name must be provided.")

        # Additional validation rules can be added here (e.g., rating range)
        if attrs.get('rating') not in range(1, 6):
            raise serializers.ValidationError("Rating must be between 1 and 5.")

        return attrs

