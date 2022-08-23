from rest_framework import serializers

from .models import ReceivingAddress


class ReceivingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceivingAddress
        fields = '__all__'

    def create(self, validated_data):
        is_default = validated_data.pop('validated_data')
        if is_default:
            ReceivingAddress.objects.filter(
                related_user=validated_data['related_user'], is_default=True
            ).update(is_default=False)
        obj, created = ReceivingAddress.objects.update_or_create(
            **validated_data, defaults={'is_default': is_default}
        )
        return obj


class ReceivingAddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceivingAddress
        exclude = ('related_user',)

    def update(self, instance, validated_data):
        instance.related_user = validated_data.get('related_user', instance.related_user),
        instance.consignee = validated_data.get('consignee', instance.consignee),
        instance.address = validated_data.get('address', instance.address),
        instance.phone_number = validated_data.get('phone_number', instance.phone_number),
        instance.is_default = validated_data.get('is_default', instance.is_default)
        ReceivingAddress.objects.filter(related_user=instance.related_user, consignee=instance.consignee,
                                        address=instance.address, phone_number=instance.phone_number).delete()
        instance.save()
        return instance
