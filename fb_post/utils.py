from fb_post.models import *
from fb_post.Exception import *
from django.db.models import Q
from typing import (
    Dict,
    List,
    Tuple,
    Set,
    Deque,
    NamedTuple,
    IO,
    Pattern,
    Match,
    Text,
    Optional,
    Sequence,
    Iterable,
    Mapping,
    MutableMapping,
    Any,
)


# Task 2
def create_post(user_id: object, post_content: object) -> None:
    if not User.objects.filter(id=user_id).exists():
        raise InvalidUserException
    elif not post_content.strip():
        raise InvalidPostContent
    else:
        post = Post(content=post_content, posted_by_id=user_id)
        post.save()
        return post.id


# Task 3
def create_comment(user_id: object, post_id: object, comment_content: object) -> None:
    if not User.objects.filter(id=user_id).exists():
        raise InvalidUserException

    elif not Post.objects.filter(id=post_id).exists():
        raise InvalidPostException

    elif not comment_content.strip():
        raise InvalidCommentContent
    else:
        comment = Comment(content=comment_content, commented_by_id=user_id, post_id=post_id)
        comment.save()
        return comment.id


# Task 4
def reply_to_comment(user_id: object, comment_id: object, reply_content: object) -> None:
    if not User.objects.filter(id=user_id).exists():
        raise InvalidUserException

    elif not Comment.objects.filter(id=comment_id).exists():
        raise InvalidCommentException

    elif not reply_content.strip():
        raise InvalidCommentContent

    elif Comment.objects.filter(id=comment_id).exists():
        prev_comment = Comment.objects.filter(id=comment_id)
        reply_comment = Comment.objects.create(content=reply_content, commented_by_id=user_id,
                                               parent_comment_id=comment_id, post=prev_comment[0].post)
        reply_comment.save()
        return reply_comment.id


reaction_list = ['LOVE', 'WOW', 'LIT', 'LIKE', 'HAHA', 'THUMBS-UP', 'THUMBS-DOWN', 'ANGRY', 'SAD']


# Task 5
def react_to_post(user_id: object, post_id: object, reaction_type: object) -> None:
    reaction_by_user_id_in_given_post = Reaction.objects.filter(post_id=post_id).filter(reaction_by_id=user_id)

    if not User.objects.filter(id=user_id).exists():
        raise InvalidUserException

    elif not Post.objects.filter(id=post_id).exists():
        raise InvalidPostException

    elif reaction_type not in reaction_list:
        raise InvalidReactionContent

    elif not reaction_by_user_id_in_given_post.exists():
        reaction = Reaction.objects.create(post_id=post_id, reaction=reaction_type, reaction_by_id=user_id)
        reaction.save()

    else:
        if reaction_type == reaction_by_user_id_in_given_post[0].reaction:
            reaction_by_user_id_in_given_post[0].delete()

        else:
            reaction_by_user_id_in_given_post[0].reaction = reaction_choices(reaction_type)
            reaction_by_user_id_in_given_post[0].save()


# Task 6
def react_to_comment(user_id: object, comment_id: object, reaction_type: object) -> None:
    reaction_by_user_id_in_given_comment = Reaction.objects.filter(comment_id=comment_id).filter(reaction_by_id=user_id)

    if not User.objects.filter(id=user_id).exists():
        raise InvalidUserException

    elif not Comment.objects.filter(id=comment_id).exists():
        raise InvalidCommentException

    elif reaction_type not in reaction_list:
        raise InvalidReactionContent

    elif not reaction_by_user_id_in_given_comment.exists():
        reaction = Reaction.objects.create(comment_id=comment_id, reaction=reaction_type, reaction_by_id=user_id)
        reaction.save()

    else:
        if reaction_type == reaction_by_user_id_in_given_comment[0].reaction:
            reaction_by_user_id_in_given_comment[0].delete()

        else:
            reaction_by_user_id_in_given_comment[0].reaction = reaction_type
            reaction_by_user_id_in_given_comment[0].save()


# Task 7
def get_total_reaction_count() -> int:
    reaction_count = Reaction.objects.all().count()
    return reaction_count


# Task 8
def get_reaction_metrics(post_id: object) -> dict[str, int]:
    reactions = Reaction.objects.filter(post_id=post_id)
    wow = 0
    lit = 0
    haha = 0
    thumbs_up = 0
    thumbs_down = 0
    angry = 0
    like = 0
    sad = 0
    love = 0

    for reaction in reactions:
        if reaction.reaction == "LIKE":
            like += 1
        elif reaction.reaction == "WOW":
            wow += 1
        elif reaction.reaction == "LIT":
            lit += 1
        elif reaction.reaction == "HAHA":
            haha += 1
        elif reaction.reaction == "THUMBS-UP":
            thumbs_up += 1
        elif reaction.reaction == "THUMBS-DOWN":
            thumbs_down += 1
        elif reaction.reaction == "ANGRY":
            angry += 1
        elif reaction.reaction == "SAD":
            sad += 1
        elif reaction.reaction == "LOVE":
            love += 1

    reaction_metrices = {'LIKE': like,
                         'WOW': wow,
                         'LIT': lit,
                         'LOVE': love,
                         'HAHA': haha,
                         'THUMBS-UP': thumbs_up,
                         'THUMBS-DOWN': thumbs_down,
                         'ANGRY': angry,
                         'SAD': sad}

    return reaction_metrices


# Task 9
def delete_post(user_id: object, post_id: object) -> None:
    post = Post.objects.filter(posted_by=user_id).filter(id=post_id)
    post.delete()


# Task 10
def get_posts_with_more_positive_reactions() -> list[Any]:
    posts = Post.objects.all()
    post_id_list = []
    for post in posts:
        reaction_metrices = get_reaction_metrics(post.id)
        sum_of_positive_reactions = sum([reaction_metrices['LIT'],
                                         reaction_metrices['THUMBS-UP'],
                                         reaction_metrices['LOVE'],
                                         reaction_metrices['HAHA'],
                                         reaction_metrices['WOW']])

        sum_of_negative_reactions = sum([reaction_metrices['SAD'],
                                         reaction_metrices['ANGRY'],
                                         reaction_metrices['THUMBS-DOWN']])

        if sum_of_positive_reactions > sum_of_negative_reactions:
            post_id_list.append(post.id)

    return post_id_list


# Task 11

def get_posts_reacted_by_user(user_id: object) -> list[object]:
    posts = Post.objects.filter(posted_by_id=user_id)
    return list(posts)


# Task 12

def get_reactions_to_post(post_id: object) -> list[dict[str, Any]]:
    reactions = Reaction.objects.filter(post_id=post_id).select_related('reaction_by')
    reaction_list = []
    for reaction in reactions:
        reaction_dict = {"user_id": reaction.reaction_by_id,
                         "name": reaction.reaction_by.name,
                         "profile_pic": reaction.reaction_by.profile_pic,
                         "reaction": reaction.reaction
                         }
        reaction_list.append(reaction_dict)

    return reaction_list


# TAsk 13
def get_reaction(reactions: object, for_reaction_object_list: object) -> dict[Any, list[Any]]:
    reaction_type_dict = {}
    for objects in for_reaction_object_list:
        comment_reaction_type_list = []
        for reaction in reactions:
            if reaction.post == objects or reaction.comment == objects:
                comment_reaction_type_list.append(reaction.reaction)
        reaction_type_dict[objects] = comment_reaction_type_list

    return reaction_type_dict


def get_reply_comments_dict(comments: object, reply_comments: object, reaction_type_dict: object) -> dict[
    Any, list[dict[str, dict[str, Any] | dict[str, int | list[Any]] | Any]]]:
    reply_comments_dict = {}
    for comment in comments:
        reply_comments_list = []
        for reply_comment in reply_comments:
            if reply_comment.parent_comment == comment:
                comment_dict = {"comment_id": reply_comment.id,
                                "commenter": {"user_id": reply_comment.commented_by_id,
                                              "name": reply_comment.commented_by.name,
                                              "profile_pic": reply_comment.commented_by.profile_pic
                                              },
                                "commented_at": reply_comment.commented_at,
                                "comment_content": reply_comment.content,
                                "reactions": {"count": len(reaction_type_dict[reply_comment]),
                                              "type": list(set(reaction_type_dict[reply_comment])),
                                              }
                                }
                reply_comments_list.append(comment_dict)
        reply_comments_dict[comment] = reply_comments_list
    return reply_comments_dict


def get_comment_list(comments: object, reaction_type_dict: object, reply_comments_dict: object) -> list[
    dict[str, int | dict[str, int | list[Any]] | dict[str, Any] | Any]]:
    comments_list = []
    for comment in comments:
        comment_dict = {"comment_id": comment.id,
                        "commenter": {"user_id": comment.commented_by_id,
                                      "name": comment.commented_by.name,
                                      "profile_pic": comment.commented_by.profile_pic
                                      },
                        "commented_at": comment.commented_at,
                        "comment_content": comment.content,
                        "reactions": {"count": len(reaction_type_dict[comment]),
                                      "type": list(set(reaction_type_dict[comment])),
                                      },
                        "replies_count": len(reply_comments_dict[comment]),
                        "replies": reply_comments_dict[comment]
                        }
        comments_list.append(comment_dict)
    return comments_list


def get_post(post_id: object) -> dict[str, dict[str, Any] | dict[str, int | list[Any]] | list[
    dict[str, int | dict[str, int | list[Any]] | dict[str, Any] | Any]] | Any]:
    posts = Post.objects.filter(id=post_id).select_related('posted_by')
    post = posts[0]

    comments = Comment.objects.filter(post_id=post_id).filter(parent_comment__isnull=True).select_related(
        'commented_by')

    reply_comments = Comment.objects.filter(parent_comment__in=comments).select_related('commented_by',
                                                                                        'parent_comment')
    for_reaction_object_list = []
    for comment in comments:
        for_reaction_object_list.append(comment)
    for comment in reply_comments:
        for_reaction_object_list.append(comment)
    for post in posts:
        for_reaction_object_list.append(post)

    reactions = Reaction.objects.filter(Q(comment_id__in=comments.values_list('id', flat=True)) | Q(
        comment_id__in=reply_comments.values_list('id', flat=True)) | Q(post_id=post_id)).select_related('reaction_by',
                                                                                                         'comment',
                                                                                                         'post')

    reaction_type_dict = get_reaction(reactions, for_reaction_object_list)

    reply_comments_dict = get_reply_comments_dict(comments, reply_comments, reaction_type_dict)

    comments_list = get_comment_list(comments, reaction_type_dict, reply_comments_dict)

    post_dict = {"post_id": post_id,
                 "posted_by": {"name": post.posted_by.name,
                               "user_id": post.posted_by_id,
                               "profile_pic": post.posted_by.profile_pic},
                 "posted_at": post.posted_at,
                 "post_content": post.content,
                 "reactions": {"count": len(reaction_type_dict[post]),
                               "type": list(set(reaction_type_dict[post]))
                               },
                 "comments": comments_list

                 }

    return post_dict


# Task 14

def get_user_posts(user_id: object) -> list[dict[str, dict[str, Any] | dict[str, int | list[Any]] | list[
    dict[str, int | dict[str, int | list[Any]] | dict[str, Any] | Any]] | Any]]:
    if not User.objects.filter(id=user_id).exists():
        raise InvalidUserException
    else:
        posts = Post.objects.filter(posted_by_id=user_id)
        post_list = []
        for post in posts:
            post_list.append(get_post(post.id))
        return post_list


# Task 15
def get_replies_for_comment(comment_id: object) -> list[dict[str, dict[str, Any] | Any]]:
    reply_comments = Comment.objects.filter(id=comment_id).select_related('commented_by')
    replies_for_comment_list = []
    for comment in reply_comments:
        comment_dict = {"comment_id": comment.id,
                        "commenter": {"user_id": comment.commented_by_id,
                                      "name": comment.commented_by.name,
                                      "profile_pic": comment.commented_by.profile_pic},
                        "commented_at": comment.commented_at,
                        "comment_content": comment.content
                        }
        replies_for_comment_list.append(comment_dict)
    return replies_for_comment_list
