from authApp.models.user import User
from authApp.models.account import Account
from rest_framework import serializers
from .accountSerializer import AccountSerializer


class UserSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'name', 'email', 'account', ]

    def create(self, validate_data):
        accountData = validate_data.pop('account')
        userInstance = User.objects.create(**validate_data)
        Account.objects.create(user=userInstance, **accountData)
        return userInstance

    def to_representation(self, obj):
        user = User.objects.get(id=obj.id)
        account = Account.objects.get(user=obj.id)
        return {
            "id": user.id,
            "username":user.username,
            "name":user.name,
            "email":user.email,
            "account":{
                "id": account.id,
                "balance":account.balance,
                "lastChangeDate":account.lastChangeDate,
                "isActive":account.isActive,
            } 

        }
