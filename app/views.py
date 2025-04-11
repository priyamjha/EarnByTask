from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm, AndroidAppForm
from .models import CustomUser, AndroidApp,  Category, Subcategory, TaskSubmission
from django.http import JsonResponse
import csv
import random
from django.conf import settings


# Create your views here.


# Define the CSV file path
JOKE_CSV_PATH = settings.BASE_DIR / "onelinefun.csv"

@login_required
def show_joke(request):
    user = request.user

    # Check if the user has enough points
    if user.points < 20:
        messages.warning(request, "You don't have enough points to see a joke.")
        return redirect('user_dashboard')

    # Read jokes from CSV file
    try:
        with open(JOKE_CSV_PATH, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            jokes = list(reader)
    except FileNotFoundError:
        messages.warning(request, "Jokes file not found.")
        return redirect('user_dashboard')

    if not jokes:
        messages.warning(request, "No jokes available.")
        return redirect('user_dashboard')

    # Pick a random joke
    joke = random.choice(jokes)["Joke"]

    # Deduct 20 points
    user.points -= 20
    user.save()

    return render(request, "joke.html", {"joke": joke, "user": user})



@login_required
def view_points(request):
    """Show the granted points of the logged-in user."""
    user = request.user
    return render(request, 'points.html', {'user': user})



@login_required
def view_tasks(request):
    """Show the apps where the logged-in user has submitted images."""
    user_submissions = TaskSubmission.objects.filter(user=request.user)

    return render(request, 'tasks.html', {'user_submissions': user_submissions})



@login_required
def submit_task(request, app_id):
    app = AndroidApp.objects.get(id=app_id)

    # Check if user already submitted
    existing_submission = TaskSubmission.objects.filter(user=request.user, app=app).first()

    if request.method == "POST":
        if existing_submission:
            messages.warning(request, "You have already submitted an image for this task.")
            return redirect("user_dashboard")

        image = request.FILES.get("image")
        if not image:
            messages.error(request, "Please upload an image.")
            return redirect("submit_task", app_id=app.id)

        TaskSubmission.objects.create(user=request.user, app=app, image=image)
        messages.success(request, "Task submitted successfully! Wait for admin approval.")
        return redirect("user_dashboard")

    return render(request, "submit_task.html", {"app": app, "existing_submission": existing_submission})





@login_required
def update_app(request, app_id):
    app = AndroidApp.objects.get(id=app_id)

    if request.user.user_type != 'admin':
        messages.warning(request, "You are not authorized to update apps.")
        return redirect('admin_dashboard')

    if request.method == 'POST':
        form = AndroidAppForm(request.POST, request.FILES, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, "App updated successfully.")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Error updating app. Please check the form.")
    else:
        form = AndroidAppForm(instance=app)

    return render(request, 'update_app.html', {'form': form, 'app': app})



@login_required
def add_app(request):
    if request.user.user_type != 'admin':
        messages.warning(request, 'You are not authorized to add apps.')
        return redirect('admin_dashboard')

    if request.method == 'POST':
        form = AndroidAppForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'App added successfully.')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Error adding app. Please check the form.')
    else:
        form = AndroidAppForm()

    return render(request, 'add_app.html', {'form': form})

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)


@login_required
def user_dashboard(request):
    if request.user.user_type == 'user':
        apps = AndroidApp.objects.all()  # Fetch all apps
        return render(request, 'user_dashboard.html', {'apps': apps})
    else:
        messages.warning(request, 'You are not authorized to view this page.')
        return redirect('login')




@login_required
def admin_dashboard(request):
    if request.user.user_type != 'admin':
        messages.warning(request, 'You are not authorized.')
        return redirect('login')

    apps = AndroidApp.objects.all()
    submissions = TaskSubmission.objects.filter(is_confirmed=False)

    if request.method == "POST":
        submission_id = request.POST.get("submission_id")
        action = request.POST.get("action")

        try:
            submission = TaskSubmission.objects.get(id=submission_id)

            if action == "approve":
                submission.is_confirmed = True
                submission.save()

                # Grant points to the user
                submission.user.points += submission.app.points
                submission.user.save()

                messages.success(request, f"Approved submission for {submission.user.username}.")
            elif action == "reject":
                submission.delete()
                messages.info(request, f"Rejected submission for {submission.user.username}.")

        except TaskSubmission.DoesNotExist:
            messages.error(request, "Submission not found.")

        return redirect("admin_dashboard")

    return render(request, 'admin_dashboard.html', {'submissions': submissions, 'apps': apps})






def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='app.backends.MyCustomBackend')
            messages.success(request, 'Registration successful.')
            return redirect('login')  # Redirect to login or another page as needed
        else:
            # Show detailed error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.warning(request, error)
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})




def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Logged in successfully.')
                if user.user_type == 'user':
                    return redirect('user_dashboard')
                elif user.user_type == 'admin':
                    return redirect('admin_dashboard')
            else:
                messages.warning(request, 'Invalid credentials.')
        else:
            for error in form.non_field_errors():
                    messages.warning(request, error)
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})




def logout(request):
    auth_logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('login')


