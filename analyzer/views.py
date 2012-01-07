import simplejson
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from analyzer.models import Statement, Purchase
from analyzer.forms import StatementForm

@login_required
def index(request):
    statements = Statement.objects.statements_for_user(request.user)    
    return render_to_response(
        'analyzer/statement_list.html',
        {'statements': statements},
        context_instance=RequestContext(request)
        )

@login_required
def add_statement(request):
    if request.POST:
        form = StatementForm(request.POST, request.FILES)
        if form.is_valid():
            statement = form.save(commit=False)
            statement.created_by = request.user
            statement.save()
            Purchase.objects.from_file(request.FILES['statement_file'], statement)
            return HttpResponseRedirect(reverse('analyzer.views.index'))
        else:
            return render_to_response(
                'analyzer/add_statement.html',
                {'form': form},
                context_instance=RequestContext(request)
                )
    else:
        form = StatementForm()
        return render_to_response(
            'analyzer/add_statement.html',
            {'form': form},
            context_instance=RequestContext(request)
            )

@login_required        
def delete_statement(request, id):
    statement = get_object_or_404(Statement, id=id)
    statement.delete()
    return HttpResponseRedirect(reverse('analyzer.views.index'))

@login_required    
def purchases(request):
    statements = Statement.objects.statements_for_user(request.user)
    purchases = Purchase.objects.filter(statement__in=statements)

    return HttpResponse(simplejson.dumps(
            [
                {
                    'title': p.title, 
                    'purchase_date': p.purchase_date.strftime("%Y-%m-%d"),
                    'amount': long(p.amount)
                    } for p in purchases
                ]
            ), 'application/javascript')
                        
    
