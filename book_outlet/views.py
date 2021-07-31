from django.shortcuts import get_object_or_404, render
from book_outlet.models import Books
from django.http import Http404
from django.db.models import Avg
# Create your views here.
def index(request):
    ''' 
    GET & FILTERS
    -------------
    get -> Fetches exactly 1 record for the condition. More than 1 records will lead to error.
    >>>Books.objects.get(title="some title")
    
    filter -> Fetches all records for the condition.
    >>>Books.objects.filter(rating=3) 
    
    rating is lower than or equal to 3
    >>>Books.objects.filter(rating__lte=3) 
        
    NOTE:   (i) You can have multiple conditions too (by default it searches under 'and' condition).
                >>>Books.objects.filter(rating__lte=3, title__icontains="book") icontains -> searches for book in title (case insensitive) 
                
            (ii) To implement 'or' functionality in filters,
                from django.db.models import Q
                >>>Books.objects.filter(Q(rating__lte=3) | Q(title__icontains="book"))
                
                Both 'or' and 'and' combined.
                >>>Books.objects.filter(Q(rating__lte=3) | Q(title__icontains="book", Q(price__lte=1000)))
                
                Wrapping in Q() for and is optional, but if it is not used, then the 'and' conditiion must come at last.
                >>>Books.objects.filter(Q(rating__lte=3) | Q(title__icontains="book", price__lte=1000)) #Success
                >>>Books.objects.filter( price__lte=1000, Q(rating__lte=3) | Q(title__icontains="book")) #Failure
    For more filters: https://docs.djangoproject.com/en/3.2/ref/models/querysets/#field-lookups
    '''
    
    allBooks = Books.objects.all().order_by("bookName") # order_by("-bookName") for descending order
    totalBooks = allBooks.count()
    avgRatingDict = allBooks.aggregate(Avg("rating"))
    averageRating = avgRatingDict["rating__avg"]
    
    # No books / rating has been added yet.
    if(averageRating == None):
        averageRating = 0
    """
    The aggregate returns a dictionary of values, since it can perform multiple operations.
    The value of the key "rating__avg" contains the value we need.
    """
    
    averageRatingFormatted = f"{averageRating: .1f}"
    
    context = {
        "allBooks": allBooks,
        "totalBooks": totalBooks,
        "averageRating": averageRatingFormatted,
        }
    return render(request, "book_outlet/index.html", context)

def book_details(request, slugUrl):
    try:
        selectedBook = Books.objects.get(slugField=slugUrl)
    except:
        raise Http404()
    
    """
    Alternatively, you can query the id as it is a PK.
    >>>selectedBook = Books.objects.get(pk=id) #'pk' identifies the id field
    
    Instead of try and catch like above you can alos use the below one-liner code(needs to be imported):
    >>>selectedBook = get_object_or_404(Books, bookName=bookTitle)
    """
    context = {"selectedBook": selectedBook}
    return render(request, 'book_outlet/book_details.html', context)