from rest_framework import serializers

from todolist.core.serializers import ProfileSerializer
from todolist.goals.models import GoalCategory, Goal, GoalComment, BaseModel


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user', 'is_deleted')
        fields = '__all__'


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')


class GoalCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=GoalCategory.objects.filter(is_deleted=False))
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise serializers.ValidationError('not allowed in deleted category')

        if value.user != self.context['request'].user:
            raise serializers.ValidationError('not owner of category')

        return value


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise serializers.ValidationError('not allowed in deleted category')

        if value.user != self.context['request'].user:
            raise serializers.ValidationError('not owner of category')

        return value


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    goal = serializers.PrimaryKeyRelatedField(queryset=Goal.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    text = serializers.CharField(max_length=1000)

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'text', 'goal')

    def validate_comment(self, value: GoalComment) -> GoalComment:
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('not owner of comment')

        return value


class GoalCommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=1000)

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'text', 'goal')

    def validate_comment(self, value: GoalComment) -> GoalComment:
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('not owner of comment')

        return value
