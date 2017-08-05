"""Views"""
from datetime import datetime
from django.contrib import messages

from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from genderwatch.models import Assembly, Verdict
from genderwatch.forms import VerdictForm, EventForm
# Create your views here.

class IndexView(TemplateView):
    """Startseite"""
    template_name = "genderwatch/index.html"

class AssemblyListView(LoginRequiredMixin, ListView):
    """
    Listet alle Verfügbaren Versammlungen o. ä. für den
    eingelogten User auf und leitet bei der Auswhal einer
    Versammlung auf die entsprechende GenderwatchInitView
    wetier.
    """
    model = Assembly

    def get_queryset(self):
        """Returns all assemblies that belong to the requesting user."""
        if self.request.user.is_superuser:
            return Assembly.objects.all()
        return Assembly.objects.filter(user=self.request.user)

class AssemblyDetailView(LoginRequiredMixin, DetailView):
    """Seite mit Startknopf, erstellt neue Wortmeldung bei POST request."""

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Assembly.objects.all()
        return Assembly.objects.filter(user=self.request.user)

class AssemblyStatView(LoginRequiredMixin, DetailView):
    """Seite mit Startknopf, erstellt neue Wortmeldung bei POST request."""
    template_name = "genderwatch/assembly_stat.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Assembly.objects.all()
        return Assembly.objects.filter(user=self.request.user)

def init_verdict(request, pk):
    """
    Erstellt eine neue Wortmeldung mit Zeitstempel jetzt
    und zeigt dann eine Form für die Informationen der
    Wortmeldung an.
    """
    assembly = get_object_or_404(Assembly, pk=pk)
    if ((not request.user in assembly.user.all()) or assembly.closed) and (not request.user.is_superuser):
        return HttpResponseForbidden()
    assembly.verdict_set.filter(end=None, user=request.user).update(end=datetime.now())
    verdict = Verdict.objects.create(assembly=assembly, user=request.user)
    verdict.save()
    request.session['verdict'] = verdict.pk
    return redirect('update-verdict')

def update_verdict(request):
    """
    Erhält einen POST request mit den Informationen für
    eine Wortmeldung, falls diese validiert werden kann, wird
    auf die Seite für die Unterbrüche weitergeleitet.
    """
    verdict = get_object_or_404(Verdict, pk=request.session['verdict'])
    form = VerdictForm()
    if request.POST:
        form = VerdictForm(request.POST, instance=verdict)
        if form.is_valid():
            verdict = form.save()
            messages.add_message(request, messages.INFO, 'Wortmeldung eröffnet.')
            return redirect('event-create')
    return render(request, 'genderwatch/verdict_update.html',
                  context={
                      'form':form,
                      'verdict': verdict,
                      'assembly': verdict.assembly
                  }
                 )


def event_create(request):
    """
    Bei GET wird die Seite mit den Knöpfen angezeigt.
    Bei POST:
    Diese Funktion fügt der laufenden Wortmeldung
    Unterbrüche usw. hinzu. Falls der Typ des Events
    STOP ist, wird die Wortmeldung abgeschlossen und wieder
    auf die GenderwatchInitView Seite weitergeleitet.
    """
    verdict = get_object_or_404(Verdict, pk=request.session['verdict'])
    positions = verdict.assembly.positions.split(',')
    def form_data(category, gender, position):
        return {
            'gender':gender,
            'category': category,
            'position':position,
        }
    initial = form_data('G+', verdict.gender, verdict.position)
    forms = {
        'glang': [EventForm(form_data('G+', verdict.gender, verdict.position),
                            button_text='Richtig gegendert'),
                  EventForm(form_data('G-', verdict.gender, verdict.position),
                           button_text='Falsch gegendert')],
        'interrupt': 
            [
            [EventForm(form_data('UB', g[0], p), button_text='{} {}'.format(g[1],p)) for g in Verdict.GENDERS]
                for p in positions
            ]
        ,
        'sexism': EventForm(form_data('SX', verdict.gender, verdict.position), 
                           button_text='Sexismus'),
        'end': EventForm(form_data('EX', verdict.gender, verdict.position),
                        button_text="Ende")
    }
    form = EventForm(initial=initial)

    if request.POST:
        form = EventForm(request.POST, initial=initial)
        if form.is_valid():
            event = form.save(commit=False)
            event.verdict = verdict
            event.save()
            if event.category == 'EX':
                event.verdict.end = datetime.now()
                event.verdict.save()
                messages.add_message(request, messages.INFO, 'Wortmeldung abgeschlossen.')
                del request.session['verdict']
                return redirect(event.verdict.assembly)
            messages.add_message(request, messages.INFO, '"{0}"@{1:%Y-%m-%d %H:%M:%S} gespeichert.'\
                                 .format(event.get_category_display(), event.time))
            form = EventForm(initial=initial)

    return render(request, 'genderwatch/event_create.html',
                  context={
                      'form': form,
                      'forms': forms,
                      'verdict': verdict,
                      'assembly': verdict.assembly
                  }
                 )
