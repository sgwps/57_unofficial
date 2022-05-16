from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from user_profile.models import User
from .models import Article
from .models import Comment
from .forms import CommentForm

# Create your views here.


class PublicationView(View):
    template_name = 'Publication.html'
    comment_form = CommentForm

    def get(self, request, *args, **kwargs):
        html_code = Article.objects.filter(pk=request.GET.get('id'))[0].content
        return render(
            request,
            PublicationView.template_name,
            {'content' : html_code, 'comment_form': PublicationView.comment_form()}
        )

    def post(self, request, *args, **kwargs):
        ctx = {
            'content': Article.objects.filter(pk=request.GET.get('id'))[0].content,
            'comment_form': PublicationView.comment_form()
        }
        comment_form = PublicationView.comment_form(request.POST)
        if comment_form.is_valid() and request.user.is_authenticated:
            form_data = comment_form.cleaned_data
            comment = Comment(
                content=form_data,
                user_id=request.user.id,
                article=Article.objects.filter(pk=request.GET.get('id'))[0]
            )
            comment.save()
            return render(request, PublicationView.template_name, ctx)
        return render(request, PublicationView.template_name, ctx)


class CommentsJsonListView(View):
    def get(self, *args, **kwargs):
        article_id = kwargs.get('article_id')
        upper = kwargs.get('num_comments')
        lower = upper - 10 if upper - 10 > 0 else 0
        comments = list(Comment.objects.filter(article=Article.objects.get(pk=article_id)).values())[lower:upper][::-1]
        data_comments = [{
            'user': User.objects.get(id=comment['user_id']).get_full_name(),
            'content': eval(comment['content'])['text']}
            for comment in comments]
        return JsonResponse({'data': data_comments}, safe=False)