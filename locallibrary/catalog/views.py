from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BookInstance, Genre
import requests

def index(request):
    """View function for home page of site."""
    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()


    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)



from django.views import generic

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'   # your own name for the list as a template variable
    paginate_by = 10
    def get_queryset(self):
        return Book.objects.filter(title__icontains='thinking')[:5]
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

    
class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
    
class AuthorDetailView(generic.DetailView):
    model = Author




# def book_detail_view(request, primary_key):
#     try:
#         book = Book.objects.get(pk=primary_key)
#     except Book.DoesNotExist:
#         raise Http404('Book does not exist')

#     return render(request, 'catalog/book_detail.html', context={'book': book})


