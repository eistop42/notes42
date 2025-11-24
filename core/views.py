from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
from .models import Note, NoteCategory

from .forms import AddNoteForm, AddNoteModelForm

def main_old(request):

    note_form = AddNoteForm()

    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        title = request.POST.get('title')
        text = request.POST.get('text')
        image = request.FILES.get('image')

        category_id = request.POST.get('category')
        if category_id:
            category = NoteCategory.objects.get(id=category_id)
        else:
            category = None

        if title and text:
            note = Note.objects.create(title=title, text=text, category=category)

            if image:
                # сохраняем картинку
                fs = FileSystemStorage()
                image_file = fs.save(image.name, image)

                # присваиваем картинку заметке
                note.image = image_file
                note.save()

            return redirect('/')

    # получаем все заметки из базы
    notes = Note.objects.filter(status=Note.PUBLIC).order_by('-created_at')

    # получаем категорию для фильтрации
    category_id = request.GET.get('category')
    if category_id:
        notes = notes.filter(category_id=category_id)
        category_id = int(category_id)

    # получаем категории из базы
    categories = NoteCategory.objects.all()

    context = {'notes': notes,
               'categories': categories,
               'selected_category_id': category_id,
               'note_form': note_form
               }

    return render(request, 'main.html', context)

def main_old_form(request):

    note_form = AddNoteForm()

    if request.method == 'POST':

        note_form = AddNoteForm(request.POST, request.FILES)

        if note_form.is_valid():

            title = note_form.cleaned_data.get('title')
            text = note_form.cleaned_data.get('text')
            category = note_form.cleaned_data.get('category')

            note = Note.objects.create(title=title, text=text, category=category)

            image = note_form.cleaned_data.get('image')
            if image:
                # сохраняем картинку
                fs = FileSystemStorage()
                image_file = fs.save(image.name, image)

                # присваиваем картинку заметке
                note.image = image_file
                note.save()

            return redirect('/')

    # получаем все заметки из базы
    notes = Note.objects.filter(status=Note.PUBLIC).order_by('-created_at')

    # получаем категорию для фильтрации
    category_id = request.GET.get('category')
    if category_id:
        notes = notes.filter(category_id=category_id)
        category_id = int(category_id)

    # получаем категории из базы
    categories = NoteCategory.objects.all()

    context = {'notes': notes,
               'categories': categories,
               'selected_category_id': category_id,
               'note_form': note_form
               }

    return render(request, 'main.html', context)

def main(request):

    note_form = AddNoteModelForm()

    if request.method == 'POST':

        note_form = AddNoteModelForm(request.POST, request.FILES)

        if note_form.is_valid():
            note_form.save()
            return redirect('/')

    # получаем все заметки из базы
    notes = Note.objects.filter(status=Note.PUBLIC).order_by('-created_at')

    # получаем категорию для фильтрации
    category_id = request.GET.get('category')
    if category_id:
        notes = notes.filter(category_id=category_id)
        category_id = int(category_id)

    # получаем категории из базы
    categories = NoteCategory.objects.all()

    context = {'notes': notes,
               'categories': categories,
               'selected_category_id': category_id,
               'note_form': note_form
               }

    return render(request, 'main.html', context)


def delete_note(request, note_id):

    note = get_object_or_404(Note, id=note_id)
    note.delete()

    return redirect('/')

def archive_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    # поменять статус
    note.status = Note.ARCHIVE
    note.save()

    return redirect('/')


def publish_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    # публикуем
    note.status = Note.PUBLIC
    note.save()

    return redirect('/')


def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    context = {'note': note}
    return render(request, 'note_detail.html', context)


def archive_notes(request):

    notes = Note.objects.filter(status=Note.ARCHIVE)

    context = {'notes': notes}
    return render(request, 'archive_notes.html', context)

@login_required
def stat(request):
    from django.db.models import Count, Avg
    from django.db.models.functions import Length

    notes_count = Note.objects.count()
    archive_notes_count = Note.objects.filter(status=Note.ARCHIVE).count()
    categories = NoteCategory.objects.annotate(num_notes=Count('note'), avg_length=Avg(Length('note__text')))

    without_category = Note.objects.filter(category__isnull=True).count()

    context = {
        'notes_count': notes_count,
        'archive_notes_count': archive_notes_count,
        'categories': categories,
        'without_category': without_category
    }
    return render(request, 'stat.html', context)

@login_required
def bootstrap(request):

    return render(request, 'bootstrap.html')

def edit_note(request, note_id):

    note = get_object_or_404(Note, id=note_id)
    form = AddNoteModelForm(instance=note)

    if request.method == 'POST':
        form = AddNoteModelForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect(f'/notes/{note.id}')

    context = {'form': form}
    return render(request, 'edit_note.html', context)


class TestPage(TemplateView):
    template_name = 'test.html'
