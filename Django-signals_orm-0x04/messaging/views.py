from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib import messages

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        # Log out first so session is cleared
        logout(request)
        user.delete()  # triggers post_delete signal
        messages.success(request, "Your account and all related data have been deleted.")
        return redirect("home")  # adjust to your landing page or login

    # GET -> show a confirmation prompt
    return render(request, "messaging/confirm_delete.html")
