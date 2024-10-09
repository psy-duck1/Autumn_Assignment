from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class OrganizationRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationRole
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class AssignmentRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentRole
        fields = '__all__'

class TeamAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamAssignment
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

class SubmissionAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionAttachment
        fields = '__all__'

class SubmissionScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionScore
        fields = '__all__'

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class NotificationSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSetting
        fields = '__all__'

# Nested Serializers for more detailed representations

class UserDetailSerializer(UserSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['roles']

class TeamDetailSerializer(TeamSerializer):
    members = UserSerializer(many=True, read_only=True)
    
    class Meta(TeamSerializer.Meta):
        fields = TeamSerializer.Meta.fields + ['members']

class AssignmentDetailSerializer(AssignmentSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    submissions = SubmissionSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta(AssignmentSerializer.Meta):
        fields = AssignmentSerializer.Meta.fields + ['subtasks', 'submissions', 'comments']

class SubmissionDetailSerializer(SubmissionSerializer):
    attachments = SubmissionAttachmentSerializer(many=True, read_only=True)
    score = SubmissionScoreSerializer(read_only=True)
    
    class Meta(SubmissionSerializer.Meta):
        fields = SubmissionSerializer.Meta.fields + ['attachments', 'score']

class OrganizationDetailSerializer(OrganizationSerializer):
    teams = TeamSerializer(many=True, read_only=True)
    assignments = AssignmentSerializer(many=True, read_only=True)
    
    class Meta(OrganizationSerializer.Meta):
        fields = OrganizationSerializer.Meta.fields + ['teams', 'assignments']