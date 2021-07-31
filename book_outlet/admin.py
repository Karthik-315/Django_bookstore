from django.contrib import admin
from book_outlet.models import Books, Author, Address, Country

# Register your models here.

#Customise admin panel
class BooksAdmin(admin.ModelAdmin):
    # readonly_fields = ("slugField", ) # Makes the field read-only
    prepopulated_fields = {
        "slugField": ("bookName",),
    }
    # Since slugField is of type SlugField, it automatically slugifies the bookName value
    
    list_filter = ("author", "rating") # Enable filters base on values in the tuple.
    list_display = ("bookName", "author", "price") # Add more columns to the admin view

    """
        More config info at: https://docs.djangoproject.com/en/3.2/ref/contrib/admin/
    """
    
class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ("bookCount",)
    
    list_display = ("get_author_Name", "bookCount")
    
    def get_author_Name(self, obj: Author) -> str:
        return f"{obj.firstName} {obj.lastName}"
    
    get_author_Name.short_description = "Author Name"
    
class AddressAdmin(admin.ModelAdmin):
    list_display = ("get_address", "pincode")
    
    def get_address(self, obj: Address):
        return obj.full_address()
    
    get_address.short_description = "Location"
    
admin.site.register(Books, BooksAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Country)