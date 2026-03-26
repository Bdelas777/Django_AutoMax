from django.shortcuts import redirect, render
from django.shortcuts import render
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View

from main.models import Listing, LikedListing
from .forms import UserForm, ProfileForm, LocationForm
# Create your views here.


def main_view(request):
    return render(request, "views/main.html", {"name": "AutoMax"})

def landing_page(request):
    return render(request, 'views/main.html')

@login_required
def home_view(request):
    listings = Listing.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=listings)
    user_liked_listings = LikedListing.objects.filter(
        profile=request.user.profile).values_list('listing')
    liked_listings_ids = [l[0] for l in user_liked_listings]
    context = {
        'listing_filter': listing_filter,
        'liked_listings_ids': liked_listings_ids,
    }
    return render(request, "views/home.html", context)

@login_required
def list_view(request):
    if request.method == 'POST':
        try:
            listing_form = ListingForm(request.POST, request.FILES)
            location_form = LocationForm(request.POST, )
            if listing_form.is_valid() and location_form.is_valid():
                listing = listing_form.save(commit=False)
                listing_location = location_form.save()
                listing.seller = request.user.profile
                listing.location = listing_location
                listing.save()
                messages.info(
                    request, f'{listing.model} Listing Posted Successfully!')
                return redirect('home')
            else:
                raise Exception()
        except Exception as e:
            print(e)
            messages.error(
                request, 'An error occured while posting the listing.')
    elif request.method == 'GET':
        listing_form = ListingForm()
        location_form = LocationForm()
    return render(request, 'views/list.html', {'listing_form': listing_form, 'location_form': location_form, })

@login_required
def listing_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        return render(request, 'views/listing.html', {'listing': listing, })
    except Exception as e:
        messages.error(request, f'Invalid UID {id} was provided for listing.')
        return redirect('home')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):

    def get(self, request):
        user_listings = Listing.objects.filter(seller=request.user.profile)
        user_liked_listings = LikedListing.objects.filter(
            profile=request.user.profile).all()
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        location_form = LocationForm(instance=request.user.profile.location)
        return render(request, 'views/profile.html', {'user_form': user_form,
                                                      'profile_form': profile_form,
                                                      'location_form': location_form,
                                                      'user_listings': user_listings,
                                                      'user_liked_listings': user_liked_listings, })

    def post(self, request):
        user_listings = Listing.objects.filter(seller=request.user.profile)
        user_liked_listings = LikedListing.objects.filter(
            profile=request.user.profile).all()
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        location_form = LocationForm(
            request.POST, instance=request.user.profile.location)
        if user_form.is_valid() and profile_form.is_valid() and location_form.is_valid():
            user_form.save()
            profile_form.save()
            location_form.save()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Error Updating Profile!')
        return render(request, 'views/profile.html', {'user_form': user_form,
                                                      'profile_form': profile_form,
                                                      'location_form': location_form,
                                                      'user_listings': user_listings,
                                                      'user_liked_listings': user_liked_listings, })