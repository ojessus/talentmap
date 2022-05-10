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
        return render_template('PermanenciaTotNeg.html', segment='Permanenciagp')
    elif current_user.username == 'gptijuana':
        return render_template('PermanenciagpHyuTij.html', segment='PermanenciagpHyuTij')
    elif current_user.username == 'gphermosillo':
        return render_template('PermanenciagpMerHer.html', segment='PermanenciagpgMerHer')
    elif current_user.username == 'gpbmw':
        return render_template('PermanenciagpBMWSal.html', segment='PermanenciagpgpBMWSal')
    elif current_user.username == 'claugto':
        return render_template('irh.html', segment='irh')
    elif current_user.username == 'lmision':
        return render_template('Permanencialm.html', segment='Permanencialm')
    elif current_user.username == 'gpmazatlan':
        return render_template('PermanenciagpCheMaz.html', segment='PermanenciagpCheMaz')
    elif current_user.username == 'gpculiacan':
        return render_template('PermanenciagpCheCul.html', segment='PermanenciagpCheCul')
    elif current_user.username == 'gpAutCul':
        return render_template('PermanenciagpAutCul.html', segment='PermanenciagpAutCul')
    elif current_user.username == 'gpAutMoc':
        return render_template('PermanenciagpAutMoc.html', segment='PermanenciagpAutMoc')
    elif current_user.username == 'gpAut':
        return render_template('PermanenciagpAutTot.html', segment='PermanenciagpAutTot')
    elif current_user.username == 'gpHyuCul':
        return render_template('PermanenciagpHyuCul.html', segment='PermanenciagpHyuCul')
    elif current_user.username == 'gpHyuCab':
        return render_template('PermanenciagpHyuCab.html', segment='PermanenciagpHyuCab')
    elif current_user.username == 'gpHyuTij':
        return render_template('PermanenciagpHyuTij.html', segment='PermanenciagpHyuTij')
    elif current_user.username == 'gpHyuMex':
        return render_template('PermanenciagpHyuMex.html', segment='PermanenciagpHyuMex')
    elif current_user.username == 'gpHyuMaz':
        return render_template('PermanenciagpHyuMaz.html', segment='PermanenciagpHyuMaz')
    elif current_user.username == 'gpHyu':
        return render_template('PermanenciagpHyuTot.html', segment='PermanenciagpHyuTot')
    elif current_user.username == 'gpToyZar':
        return render_template('PermanenciagpToyZar.html', segment='PermanenciagpToyZar')
    elif current_user.username == 'gpToyMoc':
        return render_template('PermanenciagpToyMoc.html', segment='PermanenciagpToyMoc')
    elif current_user.username == 'gpToyGua':
        return render_template('PermanenciagpToyGua.html', segment='PermanenciagpToyGua')
    elif current_user.username in ['gpToyCul','gpToyCua']:
        return render_template('PermanenciagpToyCul.html', segment='PermanenciagpToyCul')
    elif current_user.username == 'gpToyMaz':
        return render_template('PermanenciagpToyMaz.html', segment='PermanenciagpToyMaz')
    elif current_user.username == 'gpToy':
        return render_template('PermanenciagpToyTot.html', segment='PermanenciagpToyTot')
    elif current_user.username == 'gpKiaCab':
        return render_template('PermanenciagpKiaCab.html', segment='PermanenciagpKiaCab')
    elif current_user.username == 'gpKiaCdO':
        return render_template('PermanenciagpKiaCdO.html', segment='PermanenciagpKiaCdO')
    elif current_user.username == 'gpKiaCul':
        return render_template('PermanenciagpKiaCul.html', segment='PermanenciagpKiaCul')
    elif current_user.username == 'gpKiaHer':
        return render_template('PermanenciagpKiaHer.html', segment='PermanenciagpKiaHer')
    elif current_user.username == 'gpKiaLaP' :
        return render_template('PermanenciagpKiaLaP.html', segment='PermanenciagpKiaLaP')
    elif current_user.username == 'gpKiaMoc':
        return render_template('PermanenciagpKiaMoc.html', segment='PermanenciagpKiaMoc')
    elif current_user.username == 'gpKia':
        return render_template('PermanenciagpKiaTot.html', segment='PermanenciagpKiaTot')
    elif current_user.username == 'gpBmwCul':
        return render_template('PermanenciagpBMWCul.html', segment='PermanenciagpBMWCul')
    elif current_user.username == 'gpBmwMon':
        return render_template('PermanenciagpBMWMon.html', segment='PermanenciagpBMWMon')
    elif current_user.username == 'gpBmwSal':
        return render_template('PermanenciagpBMWSal.html', segment='PermanenciagpBMWSal')
    elif current_user.username == 'gpBmw':
        return render_template('PermanenciagpBMWTot.html', segment='PermanenciagpBMWTot')
    elif current_user.username == 'gpGmcCul':
        return render_template('PermanenciagpGMCCul.html', segment='PermanenciagpGMCCul')
    elif current_user.username == 'gpGmcMoc':
        return render_template('PermanenciagpGMCMoc.html', segment='PermanenciagpGMCMoc')
    elif current_user.username == 'gpGmcMaz':
        return render_template('PermanenciagpGMCMaz.html', segment='PermanenciagpGMCMaz')
    elif current_user.username == 'gpGmc':
        return render_template('PermanenciagpGMCTot.html', segment='PermanenciagpGMCTot')
    elif current_user.username == 'gpCheCul':
        return render_template('PermanenciagpCheCul.html', segment='PermanenciagpCheCul')
    elif current_user.username == 'gpCheMaz':
        return render_template('PermanenciagpCheMaz.html', segment='PermanenciagpCheMaz')
    elif current_user.username == 'gpCheHer':
        return render_template('PermanenciagpCheHer.html', segment='PermanenciagpCheHer')
    elif current_user.username == 'gpCheTot':
        return render_template('PermanenciagpCheTot.html', segment='PermanenciagpCheTot')
    elif current_user.username == 'gpMerHer':
        return render_template('PermanenciagpMerHer.html', segment='PermanenciagpMerHer')
    elif current_user.username == 'gpMerCul':
        return render_template('PermanenciagpMerCul.html', segment='PermanenciagpMerCul')
    elif current_user.username == 'gpMer':
        return render_template('PermanenciagpMerTot.html', segment='PermanenciagpMerTot')
    elif current_user.username == 'gpJagCul':
        return render_template('PermanenciagpJagCul.html', segment='PermanenciagpJagCul')
    elif current_user.username == 'gpCorCul':
        return render_template('PermanenciagpCorCul.html', segment='PermanenciagpCorCul')
    elif current_user.username == 'gpHinCul':
        return render_template('PermanenciagpHinCul.html', segment='PermanenciagpHinCul')
    elif current_user.username == 'gpMinCul':
        return render_template('PermanenciagpMinCul.html', segment='PermanenciagpMinCul')
    elif current_user.username in ['gpMinMon','gpMin']:
        return render_template('PermanenciagpMinMon.html', segment='PermanenciagpMinMon')
    elif current_user.username == 'gpPlaCul':
        return render_template('PermanenciagpPlaCul.html', segment='PermanenciagpPlaCul')
    elif current_user.username == 'gpMinTot':
        return render_template('PermanenciagpMinTot.html', segment='PermanenciagpMinTot')
    elif current_user.username == 'gpMar':
        return render_template('PermanenciaMarTot.html', segment='PermanenciagpMarTot')
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
