from rest_framework import serializers
from .models import UserShift
from schedule.serializers import LocationSerializer, ShiftSerializer, ShiftWriteSerializer
from users.serializers import UserSerializer, UserSerializerByName
from schedule.models import Location, Shift
from users.models import CustomUser


class UserShiftReadSerializer(serializers.Serializer):
    shift = ShiftSerializer()
    shift_user = UserSerializer()
    checked_in = serializers.CharField(max_length=2, min_length=2)
    date = serializers.DateField()

    def create(self, validated_data):
        """
        Create a new serialized shift given validated data
        """
        return Shift.objects.create(**validated_data)


class UserShiftWriteSerializer(serializers.Serializer):
    """
    UserShift write ops
    """
    user_id = serializers.IntegerField(write_only=True)
    shift_id = serializers.IntegerField(write_only=True)
    checked_in = serializers.CharField(max_length=2, min_length=2)
    date = serializers.DateField()
    shift_user = UserSerializer(required=False)
    shift = ShiftSerializer(required=False)

    def create(self, validated_data):
        uid = validated_data.get('user_id')
        sid = validated_data.get('shift_id')
        user = CustomUser.objects.get(pk=uid)
        shift = Shift.objects.get(pk=sid)
        return UserShift.objects.create(
            shift=shift,
            shift_user=user,
            checked_in=validated_data.get('checked_in'),
            date=validated_data.get('date')
        )

    def update(self, instance, validated_data):
        instance.shift = Shift.objects.get(pk=validated_data.get('shift_id'))
        instance.shift_user = CustomUser.objects.get(pk=validated_data.get('user_id'))
        instance.checked_in = validated_data.get('checked_in', instance.checked_in)
        instance.date = validated_data.get('date', instance.date)


class CheckInSerializer(serializers.Serializer):
    user_id = serializers.CharField(read_only=True)
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    checked_in = serializers.CharField(max_length=2, min_length=2)

    def create(self, validated_data):
        uname = validated_data.get('user_id')
        lat = validated_data.get('lat')
        lon = validated_data.get('lon')
        status = validated_data.get('checked_in')

        try:
            user = CustomUser.objects.get(username=uname)
        except CustomUser.DoesNotExist:
            user = None
        
        if  not user:
            raise serializers.ValidationError("User with that id does not exist.")
        
        # logic for validating stuff goes here
        #
        #
        #
        #

        user_shiftlist = UserShift.objects.filter(shift_user__username=uname)
        if not user_shiftlist:
            return user_shiftlist
        
        first_possible_shift = user_shiftlist[0]

        return UserShift.objects.create(
            shift=first_possible_shift.shift,
            shift_user=user,
            checked_in=status,
            date=first_possible_shift.date
        )

    def update(self, instance, validated_data):
        uid = validated_data.get('user_id')
        lat = validated_data.get('lat')
        lon = validated_data.get('lon')
        status = validated_data.get('checked_in')
        # user = self.request.user

        # possible_shifts = UserShift.objects.filter(shift_user=user)

        user = CustomUser.objects.get(id=uid)
        first_possible_shift = UserShift.objects.filter(shift_user=user)[:1].get()

        instance.shift = first_possible_shift.shift
        instance.shift_user = first_possible_shift.shift_user
        instance.checked_in = validated_data.get('checked_in', instance.checked_in)
        date = first_possible_shift.date


        instance.save()

        return instance
        # possible_shifts.filter(shift__location__lat__gte=)