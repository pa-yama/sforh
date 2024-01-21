from rest_framework import serializers
from .models import Post, Comment


'''class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('post_id', 'user', 'title', 'tag', 'text_probrem', 'text_solution', 'reference_url', 'insert_timestamp', 'update_timestamp')
'''
    
class PostSerializer(serializers.Serializer):
    post_id = serializers.CharField(max_length=None, min_length=None)#allow_blank=False , trim_whitespace=True
    title = serializers.CharField(max_length=None, min_length=None)
    tag = serializers.CharField(max_length=None, min_length=None)
    text_probrem = serializers.CharField(max_length=None, min_length=None)
    text_solution = serializers.CharField(max_length=None, min_length=None)
    reference_url = serializers.CharField(max_length=None, min_length=None)
    user = serializers.CharField(max_length=None, min_length=None)
    insert_timestamp = serializers.CharField(max_length=None, min_length=None)
    update_timestamp = serializers.CharField(max_length=None, min_length=None)




class DetailSerializer(serializers.Serializer):
    class Meta:
        model = Post
        fields = ('post_id', 'user', 'title', 'tag', 'text_probrem', 'text_solution', 'reference_url', 'insert_timestamp', 'update_timestamp')

class CommentListSerializer(serializers.Serializer):
    #commentテーブル
    class Meta:
        model = Comment
        fields = ('comment_id', 'post', 'user', 'text_comment', 'insert_timestamp', 'update_timestamp')
    
    #コメントテーブル外の情報
    poscomment_idt_id = serializers.CharField(max_length=None, min_length=None)#allow_blank=False , trim_whitespace=True
    reaction_id = serializers.CharField(max_length=None, min_length=None)
    isAlreadyGood = serializers.BooleanField()

    


class DetailPySerializer(serializers.Serializer):
    post_id = serializers.CharField(max_length=None, min_length=None)#allow_blank=False , trim_whitespace=True
    title = serializers.CharField(max_length=None, min_length=None)
    tag = serializers.CharField(max_length=None, min_length=None)
    text_probrem = serializers.CharField(max_length=None, min_length=None)
    name = serializers.CharField(max_length=None, min_length=None)
    isActiveEdit = serializers.BooleanField()
    #commentListObj = serializers.CharField(max_length=None, min_length=None)
    commentCount = serializers.CharField(max_length=None, min_length=None)
    #isAlreadyGood = serializers.BooleanField()
    #reaction_id = serializers.CharField(max_length=None, min_length=None)
    #reactionCount = serializers.CharField(max_length=None, min_length=None)
    
    
    #class Meta:
    #    list_serializer_class = CommentListSerializer
    #commentListObj = serializers.CharField(max_length=None, min_length=None)
    
    
    



