from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.generic.base import View
from django.core.paginator import Paginator
from pastebin.models import Post

from .forms import PasteForm

from .models import CodePaste

def getPosts(request, selected_page=1):
    # get all posts in sorted order
    posts = Post.objects.all().order_by('-pub_date')

    # add pagination
    pages = Paginator(posts, 5)

    try:
        returned_page = pages.page(selected_page)
    except EmptyPage:
        returned_page = pages.page(pages.num_pages)

    # display all the posts
    return render_to_response('posts.html', {'posts':returned_page.object_list, 'page':returned_page})

def getPost(request, postSlug):

    # get specified post
    post = Post.objects.filter(slug=postSlug)

    # display specified post
    return render_to_response('single.html', {'posts':post})

def postarchive(request):
    posts = Post.objects.all().order_by('-pub_date')

    return render_to_response('archive.html', {'posts':posts})

class FormIndex(View):
    form_class = PasteForm
    initial = {'name': 'name', 'language': 'language'}
    template_name = 'djpaste/create.html'
    payload = {'form': 'form'}

    def get(self, request, *args, **kwargs):

        try:
            self.initial['language'] = request.session['language']
            self.initial['name'] = request.session['name']
        except KeyError:
            self.initial['language'] = ''
            self.initial['name'] = ''
        form = self.form_class(initial=self.initial)
        self.payload['form'] = form

        return render_to_response('djpaste/create.html', self.payload, RequestContext(request))

    def post(self, request, *args, **kwargs):

        if request.method == "POST":

            form = self.form_class(request.POST)
            if(form.is_valid()):
               # try:
                    paste = form.save()
                    request.session['language'] = form.cleaned_data['language']
                    request.session['name'] = form.cleaned_data['name']
                    return HttpResponseRedirect(paste.get_absolute_url())
                   # return redirect('/')
                #except:
                 #   pass
            else:
                form = self.form_class()

#            return render_to_response('djpaste/create.html',
#                    { form: PasteForm() },
#                    context_instance = RequestContext(request))
#            return HttpResponseRedirect(paste.get_absolute_url())
            return render_to_response('djpaste/error.html', RequestContext(request))

index = FormIndex.as_view()

class PasteDetails(View):
    def get(self, request, id):
        paste = get_object_or_404(CodePaste, id = id)
        payload = {'paste':paste}
        return render_to_response('djpaste/details.html', payload, RequestContext(request))

paste_details = PasteDetails.as_view()

class Plain(View):
    def get(self, request, id):
        paste = get_object_or_404(CodePaste, id = id)
        return HttpResponse(paste.text, mimetype="text/plain")

plain = Plain.as_view()

class Html(View):
    def get(self, request, id):
        paste = get_object_or_404(CodePaste, id = id)
        return HttpResponse(paste.htmld_text, mimetype= "text/plain")

html = Html.as_view()

