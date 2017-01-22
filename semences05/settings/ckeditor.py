CKEDITOR_UPLOAD_PATH = 'ckeditor_uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'

CKEDITOR_CONFIGS = {

    'default': {
        'skin': 'moono',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_Full': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker', 'Undo', 'Redo'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'], ['Source'],
        ],
        'toolbar': 'Full',
        'height': 291,
        'width': 835,
        'filebrowserWindowWidth': 940,
        'filebrowserWindowHeight': 725,
    },
    'full': {
        'toolbar': [
            ['Undo', 'Redo',
             '-', 'Bold', 'Italic', 'Underline', 'NumberedList', 'BulletedList',
             '-', 'Outdent', 'Indent', 'Blockquote', 'CreateDiv',
             '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
             '-', 'TextColor', 'BGColor',
             '-', 'Maximize', 'ShowBlocks',  #'Image' ,
             '-', 'Cut', 'Copy', 'Paste', 'PasteText',
            ],
            ['-', 'SpecialChar',
             '-', 'Source',
            ],
            [
                '-', 'Styles', 'Format', 'Font', 'FontSize'
            ],
            [
                '-', 'BidiLtr', 'BidiRtl'
            ]
        ],
        'width': '100%',
        'height': '600px',
        'toolbarCanCollapse': False,
    },
    'restricted': {
        'toolbar': [
            [
                'Undo', 'Redo',
                '-', 'Bold', 'Italic', 'Underline',
                '-', 'Link', 'Unlink', 'Anchor',
                '-', 'NumberedList', 'BulletedList',
                '-', 'SpellChecker', 'Scayt',
                '-', 'Maximize',
                '-', 'Language',
            ]
        ],
        'height': '300px',
        'toolbarCanCollapse': False,
    },
    'disable': {
        'toolbar': [],
        'width': '100%',
        'height': '600px',
        'toolbarCanCollapse': False,
    },
}