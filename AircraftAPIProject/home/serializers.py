from dataclasses import fields
import profile
from django.contrib.auth.models import User
from rest_framework import serializers,validators
from .models import *

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','first_name','email')

        extra_kwargs ={
            "password":{
                "required":True,
                "write_only":True,},
            "username":{
                "required":True,
                "validators":[
                    validators.UniqueValidator(
                        User.objects.all(),"Username Already Taken."
                    )
                ]
            },
            "email":{
                "required":True,
                "validators":[
                    validators.UniqueValidator(
                        User.objects.all(),"A user with that Email already exists."
                    )
                ]
            },
        }
    def create(self, validated_data):
        username = validated_data.get('username')
        first_name = validated_data.get('first_name')
        password = validated_data.get('password')
        email = validated_data.get('email')

        user = User.objects.create(
            username=username,
            first_name=first_name,
            password=password,
            email=email,
        )
        password= user.set_password(validated_data['password']),
        user.save()
        return user


class taskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 
        'CreateBy',
        'Task_name',
        'Zone',
        'Task_Detail',
        'Assign',
        'DueDate',
        'Create_Date',
        'Update_Date',
        'Update_By',
        'Task_Performed',
        'Reviewed',
        'Update_By_ID',
        ) 


class mechanicSerializer(serializers.ModelSerializer):
    profile = serializers.SlugRelatedField(
    read_only=True,
    slug_field='position'
    )
    class Meta:
        model = User
        fields = ('first_name',
        'profile',
        )   

class planner_updateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
        'Task_Detail',
        'Assign',
        'DueDate',
        'Update_Date',
        'Update_By',
        'Task_Performed',
        'Reviewed',
        'Update_By_ID',
        ) 
    

class mechanic_updateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
        'Update_Date',
        'Update_By',
        'Task_Performed',
        'Update_By_ID',
        )            
