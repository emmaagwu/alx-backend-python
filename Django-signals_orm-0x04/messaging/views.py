from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,  get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import Message
from django.views.decorators.cache import cache_page



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


@login_required
def thread_view(request, root_id):
    # fetch root message with its sender/receiver eagerly
    root = get_object_or_404(
        Message.objects.select_related("sender", "receiver"),
        pk=root_id,
    )

    # Handle posting a reply
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        parent_id = request.POST.get("parent_id")
        parent = None
        if parent_id:
            parent = get_object_or_404(
                Message.objects.select_related("sender", "receiver"), pk=parent_id
            )

        # Determine the receiver: reply goes to the author of the parent (unless it's self-reply)
        if parent:
            receiver = parent.sender if parent.sender != request.user else parent.receiver
        else:
            # If replying to the root directly, swap sender/receiver appropriately
            if root.sender == request.user:
                receiver = root.receiver
            else:
                receiver = root.sender

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent,
        )
        return redirect("messaging:thread", root_id=root_id)

    # ---- fetch entire thread recursively using ORM (breadth-first) ----
    all_messages = {root.id: root}
    queue = [root.id]

    while queue:
        current_level_ids = queue
        queue = []
        # get children of current level in one query with related fields
        children_qs = Message.objects.filter(parent_message_id__in=current_level_ids).select_related(
            "sender", "receiver"
        )
        for msg in children_qs:
            if msg.id not in all_messages:
                all_messages[msg.id] = msg
                queue.append(msg.id)

    # build parent -> [children] map
    children_map = {}
    for msg in all_messages.values():
        parent_id = msg.parent_message_id
        children_map.setdefault(parent_id, []).append(msg)

    # recursive tree builder
    def build_tree(message):
        return {
            "message": message,
            "replies": sorted(
                [build_tree(child) for child in children_map.get(message.id, [])],
                key=lambda node: node["message"].timestamp,
            ),
        }

    thread_tree = build_tree(root)

    return render(
        request,
        "messaging/threaded.html",
        {"thread": thread_tree, "root": root},
    )


@login_required
def inbox_unread(request):
    user = request.user
    # Use custom manager, only pull what you need: id, sender username, content, timestamp
    unread_qs = (
        Message.unread.unread_for_user(user)
        .select_related("sender")  # eager load sender to avoid extra query
        .only("id", "content", "timestamp", "sender__username")  # minimal fields
        .order_by("-timestamp")
    )

    return render(request, "messaging/inbox_unread.html", {"unread_messages": unread_qs})


@login_required
def mark_as_read(request, message_id):
    msg = get_object_or_404(Message, pk=message_id, receiver=request.user)
    if not msg.read:
        msg.read = True
        msg.save(update_fields=["read"])
    return redirect("messaging:inbox_unread")


@login_required
@cache_page(60)  # cache this view for 60 seconds
def conversation_list(request):
    """
    Basic inbox/conversation view showing all messages involving the user,
    cached for 60 seconds to reduce database hits.
    """
    user = request.user
    # Use ORM optimization
    messages_qs = (
        Message.objects.filter(receiver=user)
        .select_related("sender", "receiver", "parent_message")
        .order_by("-timestamp")
    )

    return render(
        request,
        "messaging/conversation_list.html",
        {"messages": messages_qs},
    )