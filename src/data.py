"""Shared facts used by every language. Edit numbers here, not in content files."""

DOMAIN = 'amalficoastboatguide.com'
SITE_NAME = 'Amalfi Coast Boat Guide'
GYG_PID = 'EQTZMZ9'
VIATOR_PID = 'P00328677'
VIATOR_MCID = '42383'
WHATSAPP = '393938552086'
INDEXNOW_KEY = 'dfd8f96f3ff4b6bc65b66af6b3e8a2e7'
# Fill these in for the privacy page (GDPR asks for the data controller's identity).
OWNER_NAME = 'amalficoastboatguide.com'
OWNER_EMAIL = ''

# Coordinates are approximate. Keys starting with "w_" are sea waypoints so the
# drawn line stays on water; they have no label.
STOPS = {
    'positano': {'lat': 40.6276, 'lng': 14.4852},
    'amalfi': {'lat': 40.6327, 'lng': 14.6030},
    'sorrento': {'lat': 40.6297, 'lng': 14.3762},
    'capri_port': {'lat': 40.5570, 'lng': 14.2380},
    'li_galli': {'lat': 40.5821, 'lng': 14.4297},
    'nerano': {'lat': 40.5830, 'lng': 14.3535},
    'campanella': {'lat': 40.5675, 'lng': 14.3240},
    'faraglioni': {'lat': 40.5468, 'lng': 14.2612},
    'marina_piccola': {'lat': 40.5430, 'lng': 14.2390},
    'punta_carena': {'lat': 40.5345, 'lng': 14.1960},
    'grotto': {'lat': 40.5614, 'lng': 14.2052},
    'praiano': {'lat': 40.6085, 'lng': 14.5265},
    'furore': {'lat': 40.6185, 'lng': 14.5505},
    'emerald': {'lat': 40.6160, 'lng': 14.5615},
    'atrani': {'lat': 40.6345, 'lng': 14.6095},
    'w_massa': {'lat': 40.6080, 'lng': 14.3200},
    'w_campanella': {'lat': 40.5640, 'lng': 14.3150},
    'w_nerano': {'lat': 40.5750, 'lng': 14.3700},
    'w_capri_s': {'lat': 40.5345, 'lng': 14.2250},
    'w_capri_w': {'lat': 40.5520, 'lng': 14.1880},
    'w_capri_n': {'lat': 40.5640, 'lng': 14.2200},
    'w_capri_e': {'lat': 40.5540, 'lng': 14.2700},
    'w_praiano': {'lat': 40.6020, 'lng': 14.5250},
    'w_conca': {'lat': 40.6120, 'lng': 14.5700},
    'w_positano': {'lat': 40.6150, 'lng': 14.4900},
}

# Editorial criteria and weights (must sum to 1).
CRITERIA = [('scenery', .30), ('value', .25), ('efficiency', .20), ('comfort', .15), ('family', .10)]


def overall(t):
    return sum(t['scores'][c] * w for c, w in CRITERIA)


TOURS = [
    {'id': 'capri-positano', 'from': ['positano'], 'private': False, 'capri': True, 'grotto': True, 'kids': False,
     'hours': (7, 8), 'price': (95, 170, 'pp'), 'q': 'Capri boat tour from Positano',
     'route': ['positano', 'li_galli', 'w_nerano', 'campanella', 'w_capri_e', 'faraglioni', 'marina_piccola', 'w_capri_s',
               'punta_carena', 'w_capri_w', 'grotto', 'w_capri_n', 'capri_port', 'w_campanella', 'w_nerano', 'positano'],
     'scores': {'scenery': 9.5, 'value': 8.5, 'efficiency': 9.0, 'comfort': 7.5, 'family': 7.0},
     'related': ['private-capri', 'capri-amalfi', 'sunset-positano']},
    {'id': 'capri-amalfi', 'from': ['amalfi'], 'private': False, 'capri': True, 'grotto': True, 'kids': False,
     'hours': (8, 9), 'price': (100, 180, 'pp'), 'q': 'Capri boat tour from Amalfi',
     'route': ['amalfi', 'w_conca', 'w_praiano', 'w_positano', 'li_galli', 'w_nerano', 'campanella', 'w_capri_e', 'faraglioni',
               'marina_piccola', 'w_capri_s', 'punta_carena', 'w_capri_w', 'grotto', 'w_capri_n', 'capri_port',
               'w_campanella', 'w_nerano', 'w_positano', 'w_praiano', 'w_conca', 'amalfi'],
     'scores': {'scenery': 9.5, 'value': 8.0, 'efficiency': 7.5, 'comfort': 7.0, 'family': 6.5},
     'related': ['capri-positano', 'private-capri', 'private-coast']},
    {'id': 'capri-sorrento', 'from': ['sorrento'], 'private': False, 'capri': True, 'grotto': True, 'kids': False,
     'hours': (7, 8), 'price': (80, 150, 'pp'), 'q': 'Capri boat tour from Sorrento',
     'route': ['sorrento', 'w_massa', 'w_campanella', 'w_capri_e', 'faraglioni', 'marina_piccola', 'w_capri_s', 'punta_carena',
               'w_capri_w', 'grotto', 'w_capri_n', 'capri_port', 'w_massa', 'sorrento'],
     'scores': {'scenery': 9.0, 'value': 8.5, 'efficiency': 8.5, 'comfort': 7.5, 'family': 7.5},
     'related': ['coast-sorrento', 'private-capri', 'capri-island']},
    {'id': 'coast-sorrento', 'from': ['sorrento'], 'private': False, 'capri': False, 'grotto': False, 'kids': False,
     'hours': (7, 8), 'price': (90, 160, 'pp'), 'q': 'Amalfi Coast boat tour from Sorrento',
     'route': ['sorrento', 'w_massa', 'w_campanella', 'nerano', 'li_galli', 'positano', 'w_positano', 'w_praiano', 'furore',
               'w_conca', 'amalfi', 'w_conca', 'w_praiano', 'w_positano', 'w_nerano', 'w_campanella', 'w_massa', 'sorrento'],
     'scores': {'scenery': 9.0, 'value': 8.0, 'efficiency': 7.5, 'comfort': 7.5, 'family': 7.0},
     'related': ['capri-sorrento', 'private-coast', 'capri-positano']},
    {'id': 'private-capri', 'from': ['positano', 'amalfi', 'sorrento'], 'private': True, 'capri': True, 'grotto': True,
     'kids': True, 'hours': (6, 8), 'price': (900, 2200, 'boat'), 'q': 'private boat tour Capri',
     'route': ['positano', 'li_galli', 'w_nerano', 'campanella', 'w_capri_e', 'faraglioni', 'marina_piccola', 'w_capri_s',
               'punta_carena', 'w_capri_w', 'grotto', 'w_capri_n', 'capri_port', 'w_campanella', 'nerano', 'positano'],
     'scores': {'scenery': 10.0, 'value': 6.5, 'efficiency': 9.0, 'comfort': 9.5, 'family': 9.5},
     'related': ['private-coast', 'capri-positano', 'sunset-positano']},
    {'id': 'private-coast', 'from': ['positano', 'amalfi'], 'private': True, 'capri': False, 'grotto': False, 'kids': True,
     'hours': (3, 8), 'price': (450, 1500, 'boat'), 'q': 'private boat tour Amalfi Coast',
     'route': ['amalfi', 'atrani', 'amalfi', 'w_conca', 'emerald', 'furore', 'praiano', 'w_praiano', 'w_positano', 'positano',
               'li_galli', 'w_positano', 'w_praiano', 'w_conca', 'amalfi'],
     'scores': {'scenery': 9.0, 'value': 7.0, 'efficiency': 8.5, 'comfort': 9.5, 'family': 9.5},
     'related': ['private-capri', 'sunset-positano', 'coast-sorrento']},
    {'id': 'sunset-positano', 'from': ['positano'], 'private': False, 'capri': False, 'grotto': False, 'kids': True,
     'hours': (2, 3), 'price': (50, 95, 'pp'), 'q': 'Positano sunset boat tour',
     'route': ['positano', 'li_galli', 'w_positano', 'positano'],
     'scores': {'scenery': 8.5, 'value': 8.0, 'efficiency': 9.5, 'comfort': 8.0, 'family': 8.0},
     'related': ['private-coast', 'capri-positano', 'private-capri']},
    {'id': 'capri-island', 'from': ['capri_port'], 'private': False, 'capri': True, 'grotto': True, 'kids': True,
     'hours': (1, 2), 'price': (20, 45, 'pp'), 'q': 'Capri island boat tour Blue Grotto',
     'route': ['capri_port', 'w_capri_e', 'faraglioni', 'marina_piccola', 'w_capri_s', 'punta_carena', 'w_capri_w', 'grotto',
               'w_capri_n', 'capri_port'],
     'scores': {'scenery': 8.5, 'value': 9.5, 'efficiency': 9.0, 'comfort': 6.0, 'family': 7.5},
     'related': ['capri-sorrento', 'capri-positano', 'private-capri']},
]

GUIDES = [
    {'id': 'private-vs-group', 'tours': ['private-capri', 'private-coast', 'capri-positano', 'capri-sorrento'],
     'q': 'Amalfi Coast private boat tour'},
    {'id': 'from-positano', 'tours': ['capri-positano', 'sunset-positano', 'private-capri', 'private-coast'],
     'q': 'boat tour from Positano'},
    {'id': 'from-amalfi', 'tours': ['capri-amalfi', 'private-coast', 'private-capri'],
     'q': 'boat tour from Amalfi'},
    {'id': 'from-sorrento', 'tours': ['capri-sorrento', 'coast-sorrento', 'private-capri'],
     'q': 'boat tour from Sorrento'},
    {'id': 'capri-blue-grotto', 'tours': ['capri-island', 'capri-positano', 'capri-sorrento', 'private-capri'],
     'q': 'Capri Blue Grotto boat tour'},
    {'id': 'with-kids', 'tours': ['private-coast', 'sunset-positano', 'capri-island', 'private-capri'],
     'q': 'Amalfi Coast family boat tour'},
    {'id': 'prices', 'tours': ['capri-island', 'capri-sorrento', 'capri-positano', 'private-capri'],
     'q': 'Amalfi Coast boat tour'},
    {'id': 'best-time', 'tours': ['capri-positano', 'sunset-positano', 'private-coast'],
     'q': 'Amalfi Coast boat tour'},
]

# ---- Partners -------------------------------------------------------------
# Order of the booking buttons: the first gets the main "Book now" button.
# Put first the partner that earns you more per visitor (check EPC in your dashboards).
PARTNER_ORDER = ['gyg', 'viator']
# One "Book now" button per tour; which partner gets each tour (change freely).
TOUR_PARTNER = {
    'capri-positano': 'gyg',
    'capri-amalfi': 'viator',
    'capri-sorrento': 'gyg',
    'coast-sorrento': 'viator',
    'private-capri': 'gyg',
    'private-coast': 'viator',
    'sunset-positano': 'gyg',
    'capri-island': 'viator',
}
PARTNER_NAME = {'gyg': 'GetYourGuide', 'viator': 'Viator'}

# Optional: specific GetYourGuide activity IDs to show in the widget for a tour
# (the number in the GYG URL, e.g. ...-t123456/ -> '123456'). Comma separated.
# If empty, the widget searches with the tour's query.
GYG_TOUR_IDS = {
    # 'capri-positano': '123456,234567,345678',
}

# Optional: Viator widget embed code from the Viator Partner dashboard
# (Tools > Widgets). Key 'default' is used on every tour/guide page unless a
# tour id has its own. Paste the full HTML snippet Viator gives you.
VIATOR_WIDGETS = {
    # One block per language. 'default' shows on every page with live options in that
    # language; a tour id key overrides it on that tour page.
    'en': {'default': '<div data-vi-partner-id="P00328677" data-vi-widget-ref="W-2aa607f5-f50e-4595-aed6-86e2a62fa0f1"></div><script async src="https://www.viator.com/orion/partner/widget.js"></script>'},
    'it': {'default': '<div data-vi-partner-id="P00328677" data-vi-widget-ref="W-14437f37-c210-4363-b253-47881c1a5709"></div><script async src="https://www.viator.com/orion/partner/widget.js"></script>'},
    'es': {'default': '<div data-vi-partner-id="P00328677" data-vi-widget-ref="W-80fa1213-c9fc-4d18-bd26-00529b0d8a6a"></div><script async src="https://www.viator.com/orion/partner/widget.js"></script>'},
    'de': {'default': '<div data-vi-partner-id="P00328677" data-vi-widget-ref="W-17bfbc85-4dda-44ac-94df-bc8ba852f8ba"></div><script async src="https://www.viator.com/orion/partner/widget.js"></script>'},
    'fr': {'default': '<div data-vi-partner-id="P00328677" data-vi-widget-ref="W-6e601a2a-03a9-4d7f-b39d-f33110fa03d3"></div><script async src="https://www.viator.com/orion/partner/widget.js"></script>'},
}

# ---- Photos ----------------------------------------------------------------
# Each entry: {'src': 'img/file.jpg' (put the file in src/assets/img/) or a full
# https URL (e.g. images.unsplash.com/...), 'credit': 'Photographer', 'link': 'source page'}.
# Missing photos fall back to a coloured placeholder.
IMAGES = {
    'hero': {'src': 'img/positano-from-the-boat.webp', 'credit': 'Ahmet Yuksek / Unsplash', 'link': 'https://unsplash.com/photos/dis_sHK2oQM'},
    'tours': {
        'capri-positano': {'src': 'img/positano-gozzo.webp', 'credit': 'Louise Krause / Unsplash', 'link': 'https://unsplash.com/photos/5ennCEKDiRQ'},
        'capri-amalfi': {'src': 'img/amalfi-beach.webp', 'credit': 'Chalo Gallardo / Unsplash', 'link': 'https://unsplash.com/photos/DSOMIJFfLIM'},
        'capri-sorrento': {'src': 'img/capri-harbour-ferry.webp', 'credit': 'Richard Stachmann / Unsplash', 'link': 'https://unsplash.com/photos/7TA6gBMy21s'},
        'coast-sorrento': {'src': 'img/positano-from-the-boat.webp', 'credit': 'Ahmet Yuksek / Unsplash', 'link': 'https://unsplash.com/photos/dis_sHK2oQM'},
        'private-capri': {'src': 'img/capri-marina-grande-boats.webp', 'credit': 'Ian Badenhorst / Unsplash', 'link': 'https://unsplash.com/photos/PlyP_eFY6jk'},
        'private-coast': {'src': 'img/amalfi-beach.webp', 'credit': 'Chalo Gallardo / Unsplash', 'link': 'https://unsplash.com/photos/DSOMIJFfLIM'},
        'sunset-positano': {'src': 'img/positano-gozzo.webp', 'credit': 'Louise Krause / Unsplash', 'link': 'https://unsplash.com/photos/5ennCEKDiRQ'},
        'capri-island': {'src': 'img/capri-marina-grande.webp', 'credit': 'Julia Worthington / Unsplash', 'link': 'https://unsplash.com/photos/qsZzCxorDF4'},
    },
}
