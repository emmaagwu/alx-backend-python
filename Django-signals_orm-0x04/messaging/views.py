from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages



def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("messaging:delete_account")  # or wherever
    else:
        form = UserCreationForm()
    return render(request, "messaging/signup.html", {"form": form})

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        # Log out first so session is cleared
        logout(request)
        user.delete()  # triggers post_delete signal
        messages.success(request, "Your account and all related data have been deleted.")
        return redirect("/login")  # adjust to your landing page or login

    # GET -> show a confirmation prompt
    return render(request, "messaging/confirm_delete.html")
