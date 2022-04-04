# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from app.connectors.type_form import TYPE_FORM
from json2html import *
import app.home.utilsm as utm
import sys

talento = {
    (1, 1): 'Concern',
    (1, 2): 'Underachiever',
    (1, 3): 'Potential',
    (2, 1): 'Resource (Essential Contributor)',
    (2, 2): 'Resource (Critical Resource)',
    (2, 3): 'High Potential (High Adapter)',
    (3, 1): 'Resource (High Professional)',
    (3, 2): 'High Potential (High Achiever)',
    (3, 3): 'Asset'
}


@blueprint.route('/index')
@login_required
def index():
    if current_user.username == 'kam':
        return render_template('reporteskam.html', segment='reporteskam')
    elif current_user.username == 'grupoaxo':
        return render_template('reportesaxo.html', segment='reportesaxo')
    elif current_user.username == 'nestle':
        return render_template('reportesnestle.html', segment='reportesnestle')
    elif current_user.username == 'gbimbo':
        return render_template('reportes.html', segment='reportes')
    elif current_user.username == 'gpremier':
        return render_template('Permanenciagp.html', segment='Permanenciagp')
    elif current_user.username == 'gptijuana':
        return render_template('Permanenciagptj.html', segment='Permanenciagptj')
    elif current_user.username == 'gphermosillo':
        return render_template('Permanenciagpme.html', segment='Permanenciagpgpme')
    elif current_user.username == 'gpbmw':
        return render_template('Permanenciagpst.html', segment='Permanenciagpgpst')
    elif current_user.username == 'claugto':
        return render_template('irh.html', segment='irh')
    elif current_user.username == 'lmision':
        return render_template('Permanencialm.html', segment='Permanencialm')
    elif current_user.username == 'gpmazatlan':
        return render_template('Permanenciagpmaza.html', segment='Permanenciagpmaza')
    elif current_user.username == 'gpculiacan':
        return render_template('Permanenciagpchev.html', segment='Permanenciagpchev')
    elif current_user.username == 'autozone':
        return render_template('bi.html', segment='colaboracion')
    elif current_user.username == 'axoguest':
        return render_template('reclutamientoaxo.html', segment='reclutamientoaxo')
    elif current_user.username == 'borgwarner':
        return render_template('rotacionbw.html', segment='rotacionbw')
    else:
        return render_template('reportes.html', segment='reportes')


@blueprint.route("/nestle/<eval>/<ID>")
def models(eval, ID):
    value = utm.get_force(int(ID), eval)
    return render_template('page.html', page=value)


@blueprint.route("/nestlel/<eval>/<ID>")
def modelsl(eval, ID):
    value = utm.get_forcel(int(ID), eval)
    return render_template('page.html', page=value)


@blueprint.route("/radar/<eval>/<ID>")
def radar(eval, ID):
    value = utm.get_radar(int(ID), eval)
    return render_template('page.html', page=value)


@blueprint.route("/forop/<eval>/<ID>/<tipo>")
def forop(eval, ID, tipo):
    value = utm.get_fortalsb(int(ID), eval)
    if tipo == 'f':
        return render_template('page.html', page=value['fortalezas'])
    else:
        return render_template('page.html', page=value['oportunidades'])


@blueprint.route("/foropl/<eval>/<ID>/<tipo>")
def foropl(eval, ID, tipo):
    value = utm.get_fortalslb(int(ID), eval)
    if tipo == 'f':
        return render_template('page.html', page=value['fortalezas'])
    else:
        return render_template('page.html', page=value['oportunidades'])


@blueprint.route("/indsu/<eval>/<ID>")
def indsu(eval, ID):
    value = utm.get_is(int(ID), eval)
    return render_template('page.html', page=value)


@blueprint.route("/simulador/<ID>")
def simulador(ID):
    talent = talento[(utm.get_evTt(int(ID), 'PotencialT'), utm.get_evTt(int(ID), 'DesempeñoT'))]
    nombree = utm.get_name(ID) 
    return render_template('simulador.html',nombre=nombree, ID=ID, ita=utm.get_it(int(ID)), pot=utm.get_ev(int(ID), 'Potencial'), des=utm.get_ev(int(ID), 'Desempeño'), tray=utm.get_trayect(ID), tal=talent)


@blueprint.route("/simuladorl/<ID>")
def simuladorl(ID):
    talent = talento[(utm.get_evTl(int(ID), 'PotencialT'), utm.get_evTl(int(ID), 'DesempeñoT'))]
    nombree = utm.get_name(ID) 
    return render_template('simuladorl.html',nombre=nombree,ID=ID, ita=utm.get_itl(int(ID)), pot=utm.get_evl(int(ID), 'Potencial'), des=utm.get_evl(int(ID), 'Desempeño'), tray=utm.get_trayect(ID), tal=talent)


@blueprint.route("/top")
def topr():
    return render_template('top.html', rh=utm.get_rh(), comer=utm.get_comercial())


@blueprint.route('/<template>')
@login_required
def route_template(template):

    # try:
    if not template.endswith('.html'):
        template += '.html'

    # Detect the current page
    segment = get_segment(request)
    context = get_context(request)
    context['segment'] = segment
    # Serve the file (if exists) from app/templates/FILE.html
    return render_template(template, **context)

    # except TemplateNotFound:
    #     return render_template('page-404.html'), 404
    #
    # except:
    #     return render_template('page-500.html'), 500

# Helper - Extract current page name from request


def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None


def get_context(request):
    def encuestas_context():
        tq = TYPE_FORM()
        enclist = tq.tfquery("/forms", {'page_size': 50})
        tableraw = [{'Titulo': item['title'],
                    'Ultima Actualizacion':item['last_updated_at'],
                     'Url':item['_links']['display']
                     }
                    for item in enclist['data']['items'] if item['settings']['is_public']]
        table = json2html.convert(json=tableraw, table_attributes='class="table table-striped"')
        return {'table': table.replace('<thead>', '<thead class=" text-primary">')}
    context = {'encuestas.html': encuestas_context}
    try:
        segment = request.path.split('/')[-1]
        res = context[segment]()
        return res
    except:
        return {}
