import datetime
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User, Group

# Create your models here.
GENDERS = (
    ('m', 'Männer*'),
    ('f', 'Frauen*'),
    ('a', 'Andere'),
)

POSITIONS = (
    ('GL', "Geschäftsleitung"),
    ('PR', "Präsidium"),
    ('VS', "Vorstand"),
    ('BA', "Basis"),
    ('DG', "Delegierte"),
    ('GA', "Gäst*innen"),
    ('PO', "Podium"),
    ('NR', "Nationalrat"),
    ('BR', "Bundesrat"),
    ('SR', "Ständerat"),
    ('KR', "Kantonsrat"),
    ('GR', "Grossrat"),
    ('LR', "Landrat"),
    ('RR', "Regierungsrat"),
    ('STR', "Stadtrat"),
    ('GER', "Gemeinderat"),
    ('ER', "Einwohnerrat"),
)

def get_position_display(short):
    for position in POSITIONS:
        if short == position[0]:
            return position[1]
    return '--'


class Assembly(models.Model):
    """
    Versammlungen, Workshops usw.
    """
    CATEGORIES = (
        ('DV', 'Delegiertenversammlung'),
        ('SEKO', "Sektionskonferenz"),
        ('JV', "Jahresversammlung"),
        ('BV', "Bildungsveranstaltung"),
        ('VV', "Vollversammlung"),
        ('MV', "Mitgliederversammlung"),
        ('GRS', "Grossratssitzung"),
        ('KRS', "Kantonsratssitzung"),
        ('NRS', "Nationalratssitzung"),
        ('SRS', "Ständeratssitzung"),
        ('STRS', "Stadtratssitzung"),
        ('GERS', "Gemeinderatssitzung"),
        ('ERS', "Einwohnerratssitzung"),
    )

    category = models.CharField(max_length=10, choices=CATEGORIES, verbose_name="Kategorie")
    title = models.CharField(max_length=100, verbose_name="Titel")
    location = models.CharField(max_length=100, verbose_name="Ort")
    date = models.DateField()
    user = models.ManyToManyField(User, verbose_name="Prtokollierende")
    closed = models.BooleanField(default=False)
    positions = models.CharField(max_length=100, default='GL,DG', verbose_name="Positionen")
    topics = models.TextField(default="Begrüssung\nTraktandum 1", verbose_name="Themen")

    def get_topics(self):
        return [(slugify(t), t) for t in self.topics.strip().split('\n')]

    def get_absolute_url(self):
        """
        Return url to this object
        """
        from django.urls import reverse
        return reverse('assembly-detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

    def short_summary(self):
        for gender in GENDERS:
            durations = [verdict.duration() for verdict in self.verdict_set.filter(gender=gender[0])]
            duration = sum(durations, datetime.timedelta())
            hours = int(duration.total_seconds()/3600)
            minutes = int(duration.total_seconds() % 3600 / 60)
            seconds = int(duration.total_seconds() % 60)

            yield (gender, '{:0>2}:{:0>2}:{:0>2}'.format(hours, minutes, seconds), len(durations))

    def gender_count(self, gender):
        return self.verdict_set.filter(gender=gender).count()

    def gender_time(self, gender):
        durations = [verdict.duration() for verdict in self.verdict_set.filter(gender=gender)]
        duration = sum(durations, datetime.timedelta())
        return duration.total_seconds()/60

    def time_graph(self):
        import plotly.offline as py
        import plotly.graph_objs as go

        x = list(g[1] for g in GENDERS)
        data = []
        for position in set(self.verdict_set.values_list('position', flat=True)):
            y = list(sum((v.duration() for v in self.verdict_set.filter(gender=g[0], position=position)),\
                         datetime.timedelta()).total_seconds()/60 for g in GENDERS)

            data.append(go.Bar(
                x=x,
                y=y,
                name=get_position_display(position)
            ))

        layout = go.Layout(
            title=str(int(sum((v.duration() for v in self.verdict_set.all()), datetime.timedelta()).\
                    total_seconds()/60))+ " Min. Redezeit",
            barmode='stack',
            yaxis = dict(
                title="Minuten"
            ),
        )
        fig = go.Figure(data=data, layout=layout)
        print(data)
        return py.plot(fig, include_plotlyjs=False, output_type="div")

    def count_graph(self):
        import plotly.offline as py
        import plotly.graph_objs as go

        x = list(g[1] for g in GENDERS)
        data = []
        for position in set(self.verdict_set.values_list('position', flat=True)):
            y = list(self.verdict_set.filter(gender=g[0], position=position).count() for g in GENDERS)

            data.append(go.Bar(
                x=x,
                y=y,
                name=get_position_display(position)
            ))

        layout = go.Layout(
            barmode='stack',
            title=str(self.verdict_set.count()) + " Wortmeldungen",
        )
        fig = go.Figure(data=data, layout=layout)
        print(data)
        return py.plot(fig, include_plotlyjs=False, output_type="div")

    def count_category(self, gender, category):
        return self.verdict_set.filter(category=category, gender=gender).count()

    def category_count_chart(self):
        import plotly.offline as py
        import plotly.graph_objs as go
        data = []

        for gender in GENDERS:
            x = list((v[1] for v in self.get_topics()))
            y = list((self.count_category(gender[0], c[0]) for c in self.get_topics()))
            trace = go.Bar(
                x=x,
                y=y,
                name=gender[1],
            )
            data.append(trace)

        layout = go.Layout(
            title="Anzahl Wortmeldungen pro Kategorie",
            yaxis = dict(
                title="#"
            ),
            xaxis = dict(
                title="Kategorie"
            ),
            barmode="group"
        )
        fig = go.Figure(data=data, layout=layout)
        return py.plot(fig, include_plotlyjs=False, output_type="div")

    def time_category(self, gender, category):
        durations = (v.duration() for v in self.verdict_set.filter(category=category, gender=gender))
        duration = sum(durations, datetime.timedelta())
        return duration.total_seconds()/60


    def category_time_chart(self):
        import plotly.offline as py
        import plotly.graph_objs as go
        data = []

        for gender in GENDERS:
            x = list((v[1] for v in self.get_topics()))
            y = list((self.time_category(gender[0], c[0]) for c in self.get_topics()))
            trace = go.Bar(
                x=x,
                y=y,
                name=gender[1],
            )
            data.append(trace)

        layout = go.Layout(
            title="Redezeit pro Kategorie",
            yaxis = dict(
                title="Minuten"
            ),
            xaxis = dict(
                title="Kategorie"
            ),
            barmode="group"
        )
        fig = go.Figure(data=data, layout=layout)
        return py.plot(fig, include_plotlyjs=False, output_type="div")

    def position_count_chart(self):
        import plotly.offline as py
        import plotly.graph_objs as go
        data = []
        labels = []
        values = []
        for position in self.verdict_set.values_list('position', flat=True):
            for gender in GENDERS:
                value = self.verdict_set.filter(gender=gender[0], position=position).count()
                if value > 0:
                    values.append(value)
                    labels.append('{} {}'.format(position, gender[1]))

        trace = go.Pie(
            labels=labels,
            values=values,
        )
        data.append(trace)

        layout = go.Layout(
            title=str(self.verdict_set.count()) + " Wortmeldungen",
        )
        fig = go.Figure(data=data, layout=layout)
        return py.plot(fig, include_plotlyjs=False, output_type="div")

    def position_time_chart(self):
        import plotly.offline as py
        import plotly.graph_objs as go
        labels = []
        values = []
        for position in self.verdict_set.values_list('position', flat=True):
            for gender in GENDERS:
                value = sum((v.duration() for v in self.verdict_set.filter(gender=gender[0],
                                                                           position=position)), datetime.timedelta()).total_seconds()/60
                if value > 0:
                    values.append(value)
                    labels.append('{} {}'.format(position, gender[1]))

        trace = go.Pie(
            labels=labels,
            values=values,
        )
        layout = go.Layout(
            title=str(int(sum((v.duration() for v in self.verdict_set.all()), datetime.timedelta()).\
                    total_seconds()/60))+ " Min. Redezeit",
        )
        fig = go.Figure(data=[trace], layout=layout)
        return py.plot(fig, include_plotlyjs=False, output_type="div")

    def gender_graph(self):
        import plotly.offline as py
        import plotly.graph_objs as go
        from plotly import tools
        fig = {
            'data': [],
            'layout': {'title': 'Gendergerechte Sprache',
                       'showlegend': False,
                       "annotations": []
                      }
        }
        data = []
        domains = [
            {'x':[0,1/3.],'y':[0,1]}, 
            {'x':[1./3,2./3],'y':[0,1]}, 
            {'x':[2./3,1],'y':[0,1]}, 
        ]

        for i, gender in enumerate(Verdict.GENDERS):
            gp = Event.objects.filter(gender=gender[0],\
                                                 verdict__assembly=self, category='G+').count()
            gm =             Event.objects.filter(gender=gender[0],\
                                                 verdict__assembly=self, category='G-').count()

            fig['data'].append(
                go.Pie(
                    labels=['Richtig', 'Falsch'],
                    marker={'colors': ['rgb(0,255,0)',
                                       'rgb(255,0,0)']
                           },
                    values=[gp,gm],
                    name=gender[1],
                    domain = domains[i],
                ),
            )
            fig['layout']['annotations'].append(
                {
                    "font": {
                        "size": 14
                    },
                    "showarrow": False,
                    "text": gender[1]+ ' ({}:{})'.format(gp,gm),
                    "x": domains[i]['x'][0],
                    "y": 1
                },
            )
        return py.plot(fig, include_plotlyjs=False, output_type="div")

    def interruptions_graph(self):
        import plotly.offline as py
        import plotly.graph_objs as go
        data = []
        x = [g[1] for g in GENDERS]

        for gender1 in GENDERS:
            y = []
            for gender2 in GENDERS:
                y.append(
                    Event.objects.filter(
                        verdict__assembly=self,
                        gender=gender1[0],
                        verdict__gender=gender2[0],
                        category='UB',
                    ).count()
                )
            data.append(
                go.Bar(
                    x=x,
                    y=y,
                    name='Durch '+gender1[1]
                )
            )
        
        layout = go.Layout(
            title="Unterbrechungen",
        )
        fig = go.Figure(data=data, layout=layout)
        return py.plot(fig, include_plotlyjs=False, output_type="div")
                
    def sexism_graph(self):
        import plotly.offline as py
        import plotly.graph_objs as go
        data = [
            go.Bar(
                x=[g[1] for g in GENDERS],
                y=[Event.objects.filter(
                    verdict__assembly=self,
                    category='SX',
                    gender=g[0]).count() for g in GENDERS],
            )
        ]
        
        layout = go.Layout(
            title="Sexismus",
        )
        fig = go.Figure(data=data, layout=layout)
        return py.plot(fig, include_plotlyjs=False, output_type="div")



    class Meta:
        """Meta"""
        verbose_name = "Versammlung"
        verbose_name_plural = "Versammlungen"
        ordering = ['date']

class Verdict(models.Model):
    """
    Einzelne Wortmeldungen
    """
    CATEGORIES = (
        ('FE', "Feminismus"),
        ('DI', "Digitalisierung"),
        ('VE', "Venezuela"),
        ('99', "99%-Initiative"),
        ('MI', 'Migration'),
        ('OR', 'Organisatorisch'),
        ('WI', 'Wirtschaft'),
        ('FI', 'Finanzen'),
        ('UW', 'Umwelt'),
        ('CA', 'Care'),
        ('AR', 'Arbeit'),
        ('ST', 'Staat'),
    )
    POSITIONS = POSITIONS
    GENDERS = GENDERS

    start = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=2, choices=GENDERS, verbose_name="Gender", blank=True)
    position = models.CharField(max_length=2, choices=POSITIONS,
                                verbose_name="Position", blank=True)
    category = models.CharField(max_length=140,
                                verbose_name="Kategorie", blank=True)
    assembly = models.ForeignKey(Assembly, verbose_name="Versammlung")
    end = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, verbose_name="protokolliert von")

    def get_category_name(self):
        for topic in self.assembly.get_topics():
            if topic[0] == self.category:
                return topic[1]
        return  'Keine Kategorie'

    def duration(self):
        if self.end:
            return self.end - self.start
        return datetime.timedelta(0)

    def get_absolute_url(self):
        return self.assembly.get_absolute_url()

    class Meta:
        """Meta"""
        verbose_name = "Wortmeldung"
        ordering = ['start']


class Event(models.Model):
    """
    Unterübrüche, Gendern
    """
    CATEGORIES = (
        ('G+', 'Richtig gegendert'),
        ('G-', 'Falsch gegendert'),
        ('UB', 'Unterbrechung'),
        ('SX', 'Sexismus'),
        ('EX', 'Ende')
    )
    GENDERS = GENDERS
    POSITIONS = POSITIONS

    category = models.CharField(max_length=3, choices=CATEGORIES, verbose_name="Kategorie")
    gender = models.CharField(max_length=2, choices=GENDERS, verbose_name="Gender")
    position = models.CharField(max_length=2, choices=POSITIONS, verbose_name="Position")
    time = models.DateTimeField(auto_now_add=True)
    verdict = models.ForeignKey(Verdict, verbose_name="Wortmeldung")


    class Meta:
        """Meta"""
        verbose_name = "Ereignis"
        ordering = ['time']

class Participant(models.Model):
    gender = models.CharField(max_length=2, choices=GENDERS, verbose_name="Gender")
    count = models.PositiveSmallIntegerField(verbose_name="Anzahl")
    assembly = models.ForeignKey(Assembly)

    class Meta:
        """
        Meta
        """
        ordering = ['count']
