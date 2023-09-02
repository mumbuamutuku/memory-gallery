from django.shortcuts import render, redirect, get_object_or_404
from .models import Album, Media
from .forms import AlbumForm, MediaForm

def album_list(request):
    """
    View function to display a list of all albums.

    Parameters:
    - request (HttpRequest): The request object that contains information about the current request.

    Returns:
    - Rendered HTML page displaying a list of albums.
    """

    # Retrieve all albums from database 
    albums = Album.objects.all()
    
    # Render the 'album_list.html' template with the list of albums
    return render(request, 'media_management_app/album_list.html', {'albums': albums})

def album_detail(request, album_id):
    """
    View function to display details of a specific album and its associated media files.

    Parameters:
    - request (HttpRequest): The request object that contains information about the current request.
    - album_id (int): The unique identifier of the album to be displayed.

    Returns:
    - Rendered HTML page displaying album details and associated media files.
    """
    
    # Retrieve the albums based on the provided album id
    album = get_object_or_404(Album, id=album_id)

    # Retrieve all media associated with the album
    media = media.objects.filter(album=album)

    # Render the 'album_detail.html' template with the album and media details
    return render(request, 'media_management_app/album_detail.html', {'album': album, 'media': media})

def create_album(request):
    """
    View function to handle the creation of a new album.

    Parameters:
    - request (HttpRequest): The request object that contains information about the current request.

    Returns:
    - If the form submission is successful, it redirects the user to the album detail page for the newly created album.
    Otherwise, it displays the form with validation errors.
    """

    if request.method == 'POST':
        # If the request method is POST, process the form data
        form = AlbumForm(request.POST)
        if form.is_valid():
            # If the form is valid, save the new album to the database
            album = form.save()
            return redirect('album_detail', album_id=album.id)
    else:
        # If the request method is GET, display the album creation form
        form = AlbumForm()

    # Render the 'create_album.html' template with the album creation form 
    return render(request, 'media_management_app/create_album', {'form': form})

def upload_media(request, album_id):
     """
     View function to handle the uploading of media files to a specific album.

     Parameters:
     - request (HttpRequest): The request object that contains information about the current request.
     - album_id (int): The unique identifier of the album to which the media files should be associated.

     Returns:
     - If the form submission is successful, it redirects the user to the album detail page for the associated album.
     Otherwise, it displays the form with validation errors.
     """
    
    # Retrieve the albums based on the album id
    album = get_object_or_404(Album, id=album_id)

    if request.method == 'POST':
        # If the request method is POST, process the form
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            # If the form is valid, save the uploaded media to the database, associating it with the album
            media = form.save(commit=False)
            media.album = album
            media.uploader = request.user
            media.save()
            return redirect('album_detail', album_id=album.id)
    else:
        # If the request method is GET, display the media upload form
        form = MediaForm()

    # Render the 'upload_media.html' template with the media upload form and album details
    return render(request, 'media_management_app/upload_media.html', {'form': form, 'album': album})
