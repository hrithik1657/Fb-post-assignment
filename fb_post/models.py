from django.db import models
from django.utils import timezone
from django import forms


class User(models.Model):
    name = models.TextField(max_length=100)
    profile_pic = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    content = models.TextField(max_length=1000)
    posted_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.content


class Comment(models.Model):
    content = models.TextField(max_length=1000)
    commented_at = models.DateTimeField(auto_now=True)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


reaction_choices = (
    ('LOVE', 'LOVE'), ('LIT', 'LIT'), ('LIKE', 'LIKE'), ('WOW', 'WOW'), ('HAHA', 'HAHA'), ('THUMBS-UP', 'THUMBS-UP'),
    ('THUMBS-DOWN', 'THUMBS-DOWN'), ('SAD', 'SAD'), ('ANGRY', 'ANGRY'))


class Reaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    reaction = models.CharField(max_length=20, choices=reaction_choices)
    reaction_at = models.DateTimeField(auto_now=True)
    reaction_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.reaction
