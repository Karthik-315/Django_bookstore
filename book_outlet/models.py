from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

# Many to many rel.
class Country(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=2)
    
    """
    Add countries to Country model.
    >>> c1 = Country.objects.all()[0]
    >>> c2 = Country.objects.all()[1]
    Get book  
    >>> book = Books.objects.all()[1]  
    >>> book
    <Books: Some goodbook>
    Use 'add' (only for many to many) method to add countries to a book. Since there can be multiple countries in which a book can be 
    published, add is used to add to the list.
    >>> book.publishedCountry.add(c1)     
    >>> book.publishedCountry.add(c2) 
    Display all countries
    >>> book.publishedCountry.all()
    <QuerySet [<Country: England>, <Country: Germany>]>
    
    Inverse querying:
    >>> book2 = Books.objects.all()[3]
    >>> book2.publishedCountry.add(c1)
    >>> c1
        <Country: England>
    Since this returns a list of books per country, we use _set
    >>> c1.books_set.all()
    (or, if you have a related_name added)
    >>> c1.countiesPublished.all()
    """
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Country"

# One to one rel. with the author
class Address(models.Model):
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    pincode = models.CharField(max_length=6)
    
    def full_address(self):
        return f"{self.city}, {self.country}"
        
    def __str__(self):
        return self.full_address()
    
    class Meta:
        verbose_name_plural = "Addresses"
    """
    Add address to Author as below
    >>> jkr = Author.objects.get(firstName="J.K") 
    >>> jkr.address = Address.objects.all()[1] 
    >>> jkr.address
        <Address: London, England>
    
    You can also do the reverse and access Author for an address
    >>> Address.objects.all()[1].author 
        <Author: J.K Rowling>
    Another way of doing this (variable assignment):
    >>> londonAddr = Address.objects.all()[1] 
    >>> londonAddr.author
        <Author: J.K Rowling>
    """ 
       
class Author(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    bookCount = models.IntegerField(default=0, verbose_name="Book Count")
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        authorName = f"{self.firstName} {self.lastName}"
        return authorName
        
    """
    Access values in Books model by:
    >>> jkr = Author.objects.get(firstName="J.K") 
    >>> jkr.books_set.all() # Syntax: jkr.[Modal name]_set.all()
        <QuerySet [<Books: The Legend Of Rocketman>, <Books: The art of dying>]>
    [Modal name] can be custom defined using the parameter 'related_name' as below in the related model.
    >>> jkr.AuthoredBooks.all() # No need to include '_set' for custom related_name
    All other methods can also be used on the above
    >>> jkr.AuthoredBooks.get(bookName__icontains = "hagrid")
    """

    
class Books(models.Model):
    bookName = models.CharField(max_length=70)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name="AuthoredBooks") # One to many relation
    price = models.DecimalField(max_digits=7, decimal_places=2) # Max value -> 99999.99
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, 
                                validators=[
                                    MinValueValidator(0), 
                                    MaxValueValidator(5),
                                    ])
    slugField = models.SlugField(default="", null=False, db_index=True, blank=True) # harry-potter-1
    """ blank is set to  True, so that he admin panel, slug field can be left empty (which will be automatically generated in the save process).
    Editable is set to False, to make it not appear in admin panel.
    Enable index to make searches faster """
    
    publishedCountry = models.ManyToManyField(Country, related_name="countiesPublished")
    """ """
    
    def __str__(self):
        return self.bookName
    
    def get_absolute_url(self):
        return reverse("book_details_page", args=[self.slugField])
    
    # Update book count for respective author
    def updateBookCount(self, author):
        print("UPDATING book count for the author")
        obj = author
        obj.bookCount = Author.objects.get(firstName=obj.firstName, lastName=obj.lastName).AuthoredBooks.count()
        print("Author: ", obj.firstName)
        print("Object count: ", obj.bookCount)
        obj.save()
    
    def save(self, *args, **kwargs):
        print("Saving book")
        super().save(*args, **kwargs)
        self.updateBookCount(self.author)
        
    def update(self, *args, **kwargs):
        print("Deleting book")
        super().update(*args, **kwargs)
        self.updateBookCount(self.author)
    
    # Override save method to auto-set slug
    # Removing the save-override as admin configuration handles this now.    
    """
        def save(self, *args, **kwargs):
        self.slugField = slugify(self.bookName)
        super().save(*args, **kwargs) # Django's build in save method is called. 
    """
        
    class Meta:
        verbose_name_plural = "Books"
