from django.db.models import Q
from django.shortcuts import render , redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from .models import UniCollection, Link
from .forms import UniCollectionForm, CollectionAddForm, UniCollectionEditForm, CollectionPasswordAdd
from django.views import View
from django.contrib.auth.hashers import check_password
from django.contrib import messages
import json


class Home(View):
    template = 'home.html'

    def get(self, request):
        sort = request.GET.get('sort')

        context = {}
        context['form'] = UniCollectionForm()
        context["page_name"] = "home"
        
        collection = UniCollection.objects.filter(public = 0)
        if sort == "oldest":
            collection = UniCollection.objects.filter(public = 0).order_by('created')

        context["links"] = collection
        return render(request, self.template, context)
    
    def post(self, request):
        context = {}
        context['form'] = UniCollectionForm()
        collection_form = UniCollectionForm(request.POST)
        if collection_form.is_valid():
            shortened_object = collection_form.save()
            new_url = request.build_absolute_uri('/c/') + shortened_object.short_url
            link = collection_form.cleaned_data['collection_url']
            msg = "Your new collection is succesfully created. Go ahead & click on the lock icon in the top right menu and create a password so, that you can add new links."
            messages.success(request, msg)
            return redirect(new_url + "?u=" + link)

        context['errors'] = collection_form.errors
        return render(request, self.template, context)


class CollectionView(View):
    template = 'collection.html'

    def get(self, request, collection_link):
        context = {}
        sort = request.GET.get('sort')

        inst = get_object_or_404(UniCollection, short_url = collection_link)

        # if UniCollection.objects.get(short_url = collection_link).password == "":
        context["pp_form"] = CollectionPasswordAdd()

        context['form'] = CollectionAddForm()
        context["coll_form"] = UniCollectionEditForm(instance = inst)
        context["form"].fields["url"].initial = request.GET.get("u")
        context["visibility"] = UniCollection.objects.get(short_url = collection_link).public

        if 'q' in request.GET:
            item = request.GET.get('q')

            links = UniCollection.objects.get(short_url = collection_link).link_set.filter(Q(title__icontains=item) | Q(host_name__icontains=item))
            if sort == "oldest":
                links = UniCollection.objects.get(short_url = collection_link).link_set.filter(Q(title__icontains=item) | Q(host_name__icontains=item)).order_by('created')
            
            context["links"] = links
            context["count"] = links.count()
            context["link_id"] = collection_link
            context["page_name"] = "collection"
            context["description"] = UniCollection.objects.get(short_url = collection_link).description
            context["search_text"] = request.GET.get("q")
            return render(request, self.template, context)


        links = UniCollection.objects.get(short_url = collection_link).link_set.all()
        if sort == "oldest":
            links = UniCollection.objects.get(short_url = collection_link).link_set.all().order_by('created')

        context["links"] = links
        context["count"] = links.count()
        context["link_id"] = collection_link
        context["page_name"] = "collection"
        context["description"] = UniCollection.objects.get(short_url = collection_link).description
        return render(request, self.template, context)

    def post(self, request, collection_link):
        context = {}
        context['form'] = CollectionAddForm()
        form = CollectionAddForm(request.POST)
        if form.is_valid():
            uni = get_object_or_404(UniCollection, short_url= collection_link)
            form.instance.collection = uni
            form_object = form.save()
            return redirect("/c/" + collection_link)

        return HttpResponse(form.errors)

# View for adding collection details.
class EditCollectionName(View):
    def post(self, request, collection_link):
        instance = get_object_or_404(UniCollection, short_url = collection_link)
        coll_form = UniCollectionEditForm(request.POST or None, instance=instance)
        if coll_form.is_valid():
            coll_form.save()
            return redirect("/c/" + collection_link)
        return HttpResponse(coll_form.errors)

# View for setting up the collection password.
class SetCollectionPassword(View):
    def post(self, request, collection_link):
        instance = get_object_or_404(UniCollection, short_url = collection_link)
        pp_form = CollectionPasswordAdd(request.POST or None, instance = instance)
        if pp_form.is_valid():
            x = pp_form.cleaned_data.get('password')

            encrypted = UniCollection.objects.get(short_url = collection_link).password
            if not encrypted == None:
                if check_password(x, encrypted):
                    msg = "Congrats! You unlocked this collection try adding new links."
                    messages.success(request, msg)
                    return redirect("/c/" + collection_link)
                else:
                    msg = "Your password for this collection is incorrect, please try again!"
                    messages.warning(request, msg)
                    return redirect("/c/" + collection_link)

            msg = "Password is successfully created!"
            messages.success(request, msg)
            pp_form.save()
            return redirect("/c/" + collection_link)
        return HttpResponse(pp_form.errors)


class HowToUse(View):
    def get(self, request):
        template = "howtouse.html"
        return render(request, template)


class AboutUs(View):
    def get(self, request):
        template = "aboutus.html"
        return render(request, template)

# View for making the collection public or private
class SwitchVisibilty(View):
    def post(self, request, collection_link):
        if request.method=='POST':
            obj = UniCollection.objects.get(short_url = collection_link)
            raw = json.loads(request.body)
            if raw['data'] == 0 or raw['data'] == 1:
                obj.public = raw['data']
                obj.save()
                return JsonResponse({'status':'Success', 'msg': 'save successfully'})
        else:
            return JsonResponse({'status':'Fail', 'msg':'Not a valid request'})