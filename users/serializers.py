from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

#yo serialization chai user create garna lai  banako ho
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ('phone_number', 'username', 'password', 'membership_type')
        extra_kwargs = {'username': {'required': False}}
    
    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            username=validated_data.get('username', ''),
            password=validated_data['password']
        )
        return user
# yo serialization chai user create vaisakya paxi ko general data ko lagi banako hi
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'username', 'membership_type', 
                 'membership_start_date', 'membership_expiry_date')
        read_only_fields = ('membership_start_date', 'membership_expiry_date')# read_only_field lah chai user lah json manipulate gara ra start or expiry data pathayo vani naliwoss vanara ho,ignore gardinxa