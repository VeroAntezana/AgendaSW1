{
    'name': "Modulo Colegio",
    'summary': """
        Sistema de gestion de Colegios
    """,
    'description': """
 Agenda electronica
     """,
    'author': "Grupo15",
     'category': 'Sales/School/Industries',
     'version': '17.0.0.3',
    'depends': ['base','hr','web','calendar'],
    'data': [
       'security/school_security.xml',
        'security/ir.model.access.csv',
        'data/school_data.xml',
        'data/medical_info_data.xml',
        'views/school_menu.xml',
        'views/res_config_settings_views.xml',
        'views/res_company_views.xml',
        'views/resource_calendar_views.xml',
        'views/academic_year_views.xml',
        'views/classroom_views.xml',
        'views/res_partner_views.xml',
        'views/inscripciones.xml',
        'views/student_views.xml',
        'views/student_enrollment_views.xml',
         'views/teacher_views.xml',
        'views/course_views.xml',
        'views/materias_views.xml',
        'views/nivel_views.xml',
        'views/padre_views.xml',
        'views/pagos_views.xml',
        'views/comunicados_views.xml',
        'views/inscripcion_views.xml',
        'views/cursomateriaprofesoralumnos_views.xml',
        'views/notas_views.xml',
        'views/batch_views.xml',
        'views/section_views.xml',
        'views/subject_views.xml',
        'views/reunion_views.xml',
        
         
    ],
    'assets': {
        'web.assets_backend': [
            '/modulo_finalParcialSW/static/src/js/audio_recorder.js',
        ],
    },
    'demo': [
        'demo/base_demo.xml',
        'demo/course_demo.xml',
        'demo/student_demo.xml',
        'demo/teacher_demo.xml',
    ],
    'license': 'LGPL-3',
    'images': ['static/description/banner.gif'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
