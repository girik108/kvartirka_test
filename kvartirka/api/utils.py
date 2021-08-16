from api.models import TreeComment
from api.serializers import CommentSerializer

def test(node):
    if node.get_children_count() == 0:
        return CommentSerializer(node).data
        

root_comment = TreeComment.objects.get(pk=3)


# def factorial(n):
#     if n == 0:
#         return 1
#     else:
#         return n * factorial(n - 1)