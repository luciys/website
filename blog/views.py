from django.core.urlresolvers import get_resolver
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response

from django.template import RequestContext
from account_manager.models import User
from blog.forms import CommentForm, NewPostForm, SearchForm
from blog.models import Post, Comment, Tag, Rating
import website

def posts(request, username=None):
    try:
        template = 'blog/posts.html'
        args = {}
        if username is None:
            required_posts = Post.objects.filter(visible=True)
        else:
            user = User.objects.get(username=username)
            if request.user.username == username:
                required_posts = Post.objects.filter(user=user)
            else:
                required_posts = Post.objects.filter(user=user, visible=True)

        if len(required_posts) == 0:
            args.update({'empty': True})
        else:
            args.update({'posts': required_posts})

        args.update({'user': request.user})
    except:
        raise Http404()

    return render_to_response(template, args)


def post(request, username, post_id):
    try:
        template = 'blog/post.html'
        args = {}
        required_post = Post.objects.get(id=post_id)

        if not required_post.visible and required_post.user != request.user:
            raise Http404()

        args.update({'post': required_post})
        args.update({'comments': Comment.objects.filter(post=post_id)})

        if request.method == 'POST':
            form = CommentForm(request.POST)

            if form.is_valid():
                Comment(post=Post.objects.get(id=post_id),
                        user=User.objects.get(username=request.user.username),
                        body=form.cleaned_data['body']).save()

                return HttpResponseRedirect('/' + username + '/post' + post_id)
        else:
            form = CommentForm()

        args.update({'form': form})
    except:
        raise Http404()

    return render_to_response(template, args, context_instance=RequestContext(request))


def add_post(request):
    try:
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')

        template = 'blog/add-post.html'
        args = {}

        if request.method == 'POST':
            form = NewPostForm(request.POST)
            if form.is_valid():
                visible = True if form.cleaned_data['visible'] == 'public' else False
                new_post = Post(user=request.user,
                                title=form.cleaned_data['title'],
                                body=form.cleaned_data['body'],
                                visible=visible,)
                new_post.save()

                tags = form.cleaned_data['tags'].split()
                existing_tags = [tag.tag for tag in Tag.objects.all()]
                for tag in tags:
                    if tag not in existing_tags:
                        new_tag = Tag(tag=tag)
                        existing_tags.append(tag)
                        new_tag.save()
                    else:
                        new_tag = Tag.objects.get(tag__contains=tag)

                    new_post.tag.add(new_tag)

                return HttpResponseRedirect('/' + request.user.username + '/post' + str(new_post.id))
        else:
            form = NewPostForm()

        args.update({'form': form})
    except Exception as e:
        e = str(e)
        raise Http404(e)

    return render_to_response(template, args, context_instance=RequestContext(request))


def search(request, search_request=None, type_request=None):
    try:
        template = 'blog/search.html'
        args = {}

        if request.method == 'POST':
            form = SearchForm(request.POST)

            if form.is_valid():
                request_type = form.cleaned_data['request_type']
                request_value = form.cleaned_data['request']
                if request_type == 'tag':
                    existing_tags = [t.tag for t in Tag.objects.all()]
                    tags = [tag for tag in request_value.split() if tag in existing_tags]
                    list_post = []

                    for post in Post.objects.filter(visible=True):
                        post_tags = [t.tag for t in post.tag.all()]

                        if all(tag in post_tags for tag in tags):
                            list_post.append(post)

                    args.update({'posts': list_post})

                elif request_type == 'user':
                    args.update({'posts': Post.objects.filter(visible=True,
                                                              user=User.objects.get(username=request_value))})

                elif request_type == 'post':
                    args.update({'posts': Post.objects.filter(visible=True, title=request_value)})
        else:
            form = SearchForm()

        args.update({'user': request.user})
        args.update({'form': form})
    except:
        raise Http404()
    return render_to_response(template, args)


def change_rating(request, username=None, post_id=None, rating=None):
    try:
        pass
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')

        post = Post.objects.get(id=post_id)

        if post.user != request.user:
            try:
                user_rating = Rating.objects.get(user=request.user, post=post)
            except:
                new_rating = Rating(value=rating, user=request.user, post=post)
                new_rating.save()
                if rating is True:
                    post.rating += 1
                else:
                    post.rating -= 1
                post.save()
            else:
                if user_rating.value != rating:
                    user_rating.value = rating
                    user_rating.save()
                    if rating is True:
                        post.rating += 2

                    else:
                        post.rating -= 2
                        pass
                    post.save()

    except:
        raise Http404()
    if username is not None and post_id is not None:
        return HttpResponseRedirect('/' + username + '/post' + post_id)
    else:
        return HttpResponseRedirect('/')





















