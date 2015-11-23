# -*- coding: utf-8 -*-
# try something like
@auth.requires_login()
def index(): 
    response.title = "Sales"
    query = db(db.sale.id != 0)
    rows = query.select(db.sale.ALL, orderby =~ db.sale.created_on)
    return dict(sales=rows)


@auth.requires_login()
def detail():
    response.title = "Sale Detail"
    sale_id = request.args(0) or 0
    sale = db(db.sale.id==sale_id).select(db.sale.ALL).first()
    material = db(db.material.sale_id == sale_id).select(db.material.ALL)
    return dict(sale=sale, material=material)


@auth.requires_login()
def new():
    form = SQLFORM(db.sale)
    if form.process().accepted:
        session.flash = 'Sale recorded'
        return redirect(URL('raw_material', args=form.vars.id))
    elif form.errors:
        response.flash = 'Unable to process the request, please check the form'
    else:
        response.flash = 'Please fill out the form'
    return dict(form=form)

@auth.requires_login()
def raw_material():
    res = 0
    items = []
    costs = []
    if request.args:
        sale_id = int(request.args(0)) or 0
        if 'item[]' in request.vars and 'cost[]' in request.vars:
            if type( request.vars['item[]'] ) == type (items):
                items = request.vars['item[]']
                costs = request.vars['cost[]']
            else:
                items.append(str(request.vars['item[]']))
                costs.append(float(request.vars['cost[]']))
        for i, item in enumerate(items):
            if items[i] and costs[i] and costs[i] > 0:
                res = db.material.insert(sale_id=sale_id, item=items[i], price=float(costs[i]))
        if res:
            response.flash = 'Record updated'
            return( redirect( URL('index') ) )
    else:
        response.flash = 'Errors in form'
             
    return locals()

def rmt():
    return locals()

