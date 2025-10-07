from rest_framework import serializers
from .models import Member, MemberDocument
from authentication.models import User


class MemberSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    
    class Meta:
        model = Member
        fields = ['id', 'member_number', 'national_id', 'date_of_birth', 'address', 
                 'occupation', 'employer', 'monthly_income', 'next_of_kin_name', 
                 'next_of_kin_phone', 'next_of_kin_relationship', 'membership_fee_paid', 
                 'status', 'user_name', 'email', 'phone_number', 'registration_date']
        read_only_fields = ['id', 'member_number', 'registration_date']


class MemberRegistrationSerializer(serializers.ModelSerializer):
    # User fields
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Member
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'password',
                 'national_id', 'date_of_birth', 'address', 'occupation', 'employer', 
                 'monthly_income', 'next_of_kin_name', 'next_of_kin_phone', 'next_of_kin_relationship']

    def create(self, validated_data):
        # Extract user data
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'phone_number': validated_data.pop('phone_number'),
            'password': validated_data.pop('password'),
        }
        
        # Create user
        user = User.objects.create_user(**user_data)
        
        # Generate member number
        import random
        member_number = f"MEM{random.randint(100000, 999999)}"
        
        # Create member
        member = Member.objects.create(user=user, member_number=member_number, **validated_data)
        return member


class MemberDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberDocument
        fields = ['id', 'document_type', 'document_file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']