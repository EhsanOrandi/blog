from django.contrib import messages

def make_published(modeladmin, request, queryset):
    queryset.update(draft = False)
    messages.add_message(request, messages.INFO, 'Selected stories published successfully.')
    
make_published.short_description = "Mark selected stories as published"

