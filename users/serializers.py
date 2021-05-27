from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from visit.models import Visit

class UserSerializer(serializers.ModelSerializer):
    visits = serializers.ReadOnlyField()
    faculty = serializers.ReadOnlyField()
    department = serializers.StringRelatedField()
    img = serializers.StringRelatedField()

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "hu_id",
            "email",
            "user_name",
            "visits",
            "visits_no",
            "gender",
            "address",
            "img",
            "country",
            "last_login_str",
            "faculty",
            "department",
        ]

        extra_kwargs = {"faculty": {"read_only"}}


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "gender", "email", "user_name"]

        depth = 1


class StudentSerializersWithHU(UsersSerializer):
    class Meta:
        fields = UsersSerializer.Meta.fields + ["hu_id"]
        model = UsersSerializer.Meta.model


class StudenSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        depth = 1
        fields = (
            "id",
            "user_name",
            "email",
            "phone",
            "password",
            "gender",
            # 'visits',
            "hu_id",
            "address",
            "country",
            "last_login",
        )

        extra_kwargs = {"password": {"write_only": True}}

        # TODO::create user throught api serializer
        def create(self, validated_data):
            return get_user_model().objects.create_user(**validated_data)


class StudentLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )
        if not user:
            raise serializers.ValidationError(
                "Invalid credentianls", code="authentication"
            )

        attrs["user"] = user

        return attrs


class SupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "user_name",
            "email",
            "first",
            "last",
            "phone",
            "gender",
            "country",
            "password",
            "address",
        )

        model = get_user_model()

        depth = 1
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"},
                "min_length": 6,
            },
            "address": {"allow_null": True},
        }

    def get_queryset(self):
        return get_user_model().objects.filter(is_staff=True).all()

    def create(self, validated_data):
        return get_user_model().objects.create_staff_only(
            email=validated_data["email"],
            password=validated_data["password"],
            phone=validated_data["phone"],
            first=validated_data["first"],
            last=validated_data["last"],
            gender=validated_data["gender"],
            is_staff=True,
        )

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        return super().update(instance, validated_data)


class SuperAdminSerializer(StudenSerializer):
    pass

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        validated_data["is_staff"] = True

        return get_user_model().objects.create_super_admin(**validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        return super().update(instance, validated_data)

class RemoveVisitUserSerializer(serializers.Serializer):
    token = serializers.CharField()
    csrf = serializers.CharField()
    visit = serializers.PrimaryKeyRelatedField(queryset=Visit.objects.all())
