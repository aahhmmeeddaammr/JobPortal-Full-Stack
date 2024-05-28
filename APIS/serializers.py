from rest_framework import serializers

from Site.models import Job,User,Skills,ApplayIn,Category,Location

class Jobserializers(serializers.ModelSerializer):
    class Meta:
        model=Job
        fields='__all__'

class Categoryserializers(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'


class Locationserializers(serializers.ModelSerializer):
    class Meta:
        model=Location
        fields='__all__'

class Userserializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class Skillserializers(serializers.ModelSerializer):
    class Meta:
        model=Skills
        fields='__all__'

class ApplayInserializers(serializers.ModelSerializer):
    class Meta:
        model=ApplayIn
        fields='__all__'