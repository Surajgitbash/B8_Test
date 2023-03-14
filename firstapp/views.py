from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Book

# Create your views here.

@csrf_exempt
@login_required
def home(request):  # http request
    if request.method == "POST":
        data = request.POST
        print(data)
        # print(request.POST.getlist("cars")) # get- for single value, getlist for multiple values
        bid = data.get("book_id")
        name = data.get("book_name")
        qty = data.get("book_qty")
        price = data.get("book_price")
        author = data.get("book_author")
        is_pub = data.get("book_is_pub")    # Yes, No
        # print(request.POST)

        # print(name, qty, price, author, is_pub) 
        if is_pub == "Yes":
            is_pub = True
        else:
            is_pub = False 
        if not bid:
            Book.objects.create(name=name, qty=qty, price=price, author=author, is_published=is_pub)
        else:
            book_obj = Book.objects.get(id=bid)
            book_obj.name = name
            book_obj.qty = qty
            book_obj.price = price
            book_obj.author = author
            book_obj.is_published = is_pub
            book_obj.save()

        # return redirect("home_page") 
        return HttpResponse("Success")
    elif request.method == "GET":
        # print(request.GET)       # get query params
        return render(request, "old_home.html")     # context={"all_books": Book.objects.all()}) 

@login_required
def show_books(request):
    return render(request, "show_books.html", {"books" : Book.objects.filter(is_active=True)})
 
@login_required
def update_book(request, id):
    book_obj = Book.objects.get(id=id)
    return render(request, "home.html", context={"single_book": book_obj})
    
@login_required
def delete_book(request, pk):   ### Hard delete database se conected
    Book.objects.get(id=pk).delete()
    return redirect("all_active_books")

@login_required
def soft_delete_book(request, pk):   ### soft delete 
    book_obj = Book.objects.get(id=pk)
    book_obj.is_active = False
    book_obj.save()
    return redirect("all_inactive_books")


@login_required
def show_inactive_books(request):
    return render(request, "show_books.html", {"books" : Book.objects.filter(is_active=False), "inactive": True}) # paramiter chatch karana hai  

@login_required  
def restore_book(request, pk):
    book_obj = Book.objects.get(id=pk)
    book_obj.is_active = True
    book_obj.sava()
    return redirect("all_active_books")


## 
# Boostrap 
#     - css framework
#     - types -- inline, internal, external(link copy, static file)
#     - table
#     - buttons
#     - select - dropdown 

#########################   21  /   12  /   2022    #########################################
# #--------------------------- Forms in django --------------------------------

from .forms import BookForm
# from django.contrib.auth.forms import UserCreationForm


# def book_form(request): 
#     return render(request, "book_form.html", {"form": Book()})


@login_required 
def book_form(request): 
    form = BookForm()
    if request.method == 'POST':
        print(request.POST)

        form = BookForm(data=request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            form.save()     # database save 
            return HttpResponse("Successfull Registrered!!!")
    else:
        context = {'form': form}    
        return render(request, "book_form.html",context=context )
    
# simpleisbetterthancomplex

def sibtc(request):
    return render(request, "sibtc.html", {"form": ()})

########################## Class Based views #####################################
# ---------------------- 24 / 12 / 2022 -----------------------------------------
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    # print("in index function")
    book_list = Book.objects.all()
    page = request.GET.get('page', 1)
    print(page) 
    paginator = Paginator(book_list, 3)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return render(request, 'index.html', { 'books': books })

# ---------------------------------------------------------------------------------------------
# --------- class Based Views ----------------------#

# from django.views import View

# class NewView(View):
#     def get(self, request):
#         # views logic will place the here 
#         return HttpResponse('get response')

#     def post(self, request):
#         return HttpResponse('post response')

#     def put(self, request): # update
#         return HttpResponse('put response')

#     def patch(self, request):   # partial info update
#         return HttpResponse('patch response')

#     def delete(self, request):  # delete karata hai     
#         return HttpResponse('delete response')

# ---------------------------------------------------------------------------------------

########## CRUD #########################

from django.views.generic.edit import CreateView

class BookCreate(CreateView):   # get / post 2 request ko handled karta hai 
    model = Book
    fields = '__all__'
    # redirect = "BookCreate"     
    success_url = "/cbv-create-book/"   # is se bhi ho jayega record    # reverse_lazy('BookCreate')   

# --------------------------------------------------------------------------------------------------

from django.views.generic.list import ListView  
  
class BookRetrieve(ListView):  
    model = Book  
    context_object_name = "all_books"
    # http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']   
    # queryset = Book.objects.filter(is_active=0)

# def get_queryset(self):
#     print("in method")
#     return Book.objects.filter(is_active=0)

# -----------------------------------------------------------------------------

from django.views.generic.detail import DetailView

class BookDetail(DetailView):
    model = Book 
# -----------------------------------------------------------------------------

from django.views.generic.edit import UpdateView

class BookUpdate(UpdateView):
    model = Book 
    fields = "__all__"
    success_url = "/cbv-create-book/"   # is se bhi ho jayega record    

# -----------------------------------------------------------------------------

from django.views.generic import TemplateView

class Tempalat(TemplateView):
    template_name = "home.html"



def create_csv(request):
    pass   

from django.http import HttpResponse
import csv

def create_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['name','qty', 'price', 'author', 'is_published', 'is_active'])

    books = Book.objects.all().values_list('name','qty', 'price', 'author', 'is_published', 'is_active')
    for book in books:
        writer.writerow(book)

    return response
