from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import FilmWork, Roles

class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']


    @staticmethod
    def choice_persons(role):
        return ArrayAgg(
            'persons__full_name',
            distinct=True,
            filter=Q(personfilmwork__role=role)
        )

    def get_queryset(self):
        queryset = self.model.objects.values().annotate(
            genres=ArrayAgg(
                "genres__name",
                distinct=True
            ),
            actors=self.choice_persons(Roles.ACTOR),
            directors=self.choice_persons(Roles.DIRECTOR),
            writers=self.choice_persons(Roles.WRITER),
        )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)

class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50
    
    def get_context_data(self, *, object_list=None, **kwargs):
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            self.get_queryset(),
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

     def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        context = queryset.get(id=self.kwargs['pk'])
        return context