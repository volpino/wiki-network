#from django.db import models
from django.db.models import *


class WikiRunData(Model):
    lang = CharField(max_length=3, blank=False)
    date = CharField(max_length=8, blank=False)
    
    # --details
    nodes_number = IntegerField(blank=True, null=True)
    edges_number = IntegerField(blank=True, null=True)
    nodes_with_out_edges_number = IntegerField(blank=True, null=True)
    nodes_with_in_edges_number = IntegerField(blank=True, null=True)
    max_weights_on_edges = CharField(max_length=100, blank=True, null=True)
    reciprocity = FloatField(blank=True, null=True)
    #average_weight = FloatField(blank=True, null=True)
    
    # --density
    density = FloatField(blank=True, null=True)
    
    length_of_5_max_clusters = CharField(max_length=100, blank=True, null=True)
    
    # --distance
    average_distance_in_the_giant_component = FloatField(blank=True, null=True)
    average_hops_in_the_giant_component = FloatField(blank=True, null=True)
    
    # --efficiency
    efficiency = FloatField(blank=True, null=True)
    
    # --power-law
    alpha_exp_of_the_power_law = FloatField(blank=True, null=True)
    
    created = DateTimeField(auto_now_add = True)
    modified = DateTimeField(auto_now = True)
    
    def __unicode__(self):
        return "%s, %s" % (self.lang, self.date)
    
    
class WikiRunGroupData(Model):
    wikirun = ForeignKey(WikiRunData)
    lang = CharField(max_length=3, blank=False)
    date = CharField(max_length=8, blank=False)
    group = CharField(max_length=20, blank=False)
    nodes_number = IntegerField(blank=True, null=True)

    # --degree
    mean_IN_degree_no_weights = FloatField(blank=True, null=True)
    mean_OUT_degree_no_weights = FloatField(blank=True, null=True)
    max_IN_degrees_no_weights = CharField(max_length=100, blank=True)
    max_OUT_degrees_no_weights = CharField(max_length=100, blank=True)
    stddev_IN_degree_no_weights = FloatField(blank=True, null=True)
    stddev_OUT_degree_no_weights = FloatField(blank=True, null=True)
    
    # --density
    density = FloatField(blank=True, null=True)
    
    # --reciprocity
    reciprocity = FloatField(blank=True, null=True)    
    
    # --centrality
    average_betweenness = FloatField(blank=True, null=True)
    stddev_betweenness = FloatField(blank=True, null=True)
    max_betweenness = CharField(max_length=100, blank=True)

    average_pagerank = FloatField(blank=True, null=True)
    stddev_pagerank = FloatField(blank=True, null=True)
    max_pagerank = CharField(max_length=100, blank=True)    
    
    average_IN_degree_centrality_weighted = FloatField(blank=True, null=True)
    stddev_IN_degree_centrality_weighted = FloatField(blank=True, null=True)
    max_IN_degrees_centrality_weighted = CharField(max_length=100, blank=True)
    
    average_OUT_degree_centrality_weighted = FloatField(blank=True, null=True)
    stddev_OUT_degree_centrality_weighted = FloatField(blank=True, null=True)
    max_OUT_degrees_centrality_weighted = CharField(max_length=100, blank=True)
    
    # --power-law
    alpha_exp_IN_degree_distribution = FloatField(blank=True, null=True)
    
    created = DateTimeField(auto_now_add = True)
    modified = DateTimeField(auto_now = True)
    
    def __unicode__(self):
        return "%s-%s created on: %s" % (self.lang, self.date, self.created.isoformat())
    
    
class WikiStat(Model):
    lang = CharField(max_length=20, blank=False)
    
    ## {u'articles': 119816, u'jobs': 11, u'users': 24920, u'admins': 15, u'edits': 2493575, u'activeusers': 477, u'images': 12693, u'pages': 264348}
    articles = IntegerField(blank=True, null=True)
    jobs = IntegerField(blank=True, null=True)
    users = IntegerField(blank=True, null=True)
    admins = IntegerField(blank=True, null=True)
    edits = IntegerField(blank=True, null=True)
    activeusers = IntegerField(blank=True, null=True)
    images = IntegerField(blank=True, null=True)
    pages = IntegerField(blank=True, null=True)
    
    created = DateTimeField(auto_now_add = True)
    modified = DateTimeField(auto_now = True)
    
    
    def __unicode__(self):
        return "%s, stats of %s" % (self.lang, self.created.isoformat())
    
    
class WikiLang(Model):
    lang = CharField(max_length=20, primary_key=True)
    
    lang_group = CharField(max_length=20, blank=True, null=True)

    created = DateTimeField(auto_now_add = True)
    modified = DateTimeField(auto_now = True)
    
    def __unicode__(self):
        return self.lang
    
    
class BigWikiStat(Model):
    rank = IntegerField(blank=True, null=True)
    _id = IntegerField(blank=True, null=True)
    name = CharField(max_length=200)
    total = IntegerField(blank=True, null=True)
    good = IntegerField(blank=True, null=True)
    edits = IntegerField(blank=True, null=True)
    views = IntegerField(blank=True, null=True)
    admins = IntegerField(blank=True, null=True)
    users = IntegerField(blank=True, null=True)
    images = IntegerField(blank=True, null=True)
    ratio = FloatField(blank=True, null=True)
    type = CharField(max_length=50, blank=True, null=True)
    url = CharField(max_length=200, blank=True, null=True)
    ts = DateTimeField()
    
    created = DateTimeField(auto_now_add = True)
    modified = DateTimeField(auto_now = True)
    
class CeleryRun(Model):
    #celery related
    name = CharField(max_length=36)
    hide = BooleanField(default=False)
    
    #wiki related
    lang = CharField(max_length=20, blank=False)
    
    created = DateTimeField(auto_now_add = True)
    modified = DateTimeField(auto_now = True)