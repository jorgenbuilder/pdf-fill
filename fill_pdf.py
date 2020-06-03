# https://bostata.com/how-to-populate-fillable-pdfs-with-python/

import datetime
import os
import pdfrw

TIMESTAMP = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
PDF_TEMPLATE_PATH = 'template.pdf'
PDF_OUTPUT_PATH = f'output/{TIMESTAMP}.pdf'

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

CONTEXT = {
    'aia_number': '1252135213451235',
    'individuals_name': 'Jean-Marc Skopek',
    'date_issued': datetime.datetime.now().strftime('%Y-%m-%d'),
}

def fill_pdf(in_path, out_path, context):
    template = pdfrw.PdfReader(in_path)
    annotations = template.pages[0][ANNOT_KEY]
    for annotation in annotations:
        if annotation[ANNOT_FIELD_KEY]:
            key = annotation[ANNOT_FIELD_KEY][1:-1]
            if key in context.keys():
                annotation.update(
                    pdfrw.PdfDict(V=f'{context[key]}')
                )
    pdfrw.PdfWriter().write(out_path, template)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Fill a certificate PDF.')
    parser.add_argument('-n', '--name', default='Jean-Marc Skopek')
    parser.add_argument('-d', '--date', default=datetime.datetime.now().strftime('%Y-%m-%d'))
    parser.add_argument('-a', '--aia', default='1252135213451235')
    args = parser.parse_args()
    CONTEXT['aia_number'] = args.aia
    CONTEXT['individuals_name'] = args.name
    CONTEXT['date_issued'] = args.date
    fill_pdf(PDF_TEMPLATE_PATH, PDF_OUTPUT_PATH, CONTEXT)
